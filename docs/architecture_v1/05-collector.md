# 기술 설계 문서 — Dependency Collector (`collector/`)

> 관련 자료: `CONTRIBUTING.md` §3(스키마 계약)

## 1. 모듈 구조 (제안)

```
collector/
├── cli.py                     # 진입점 (python -m collector --repo <path|url>)
├── config.py                  # 타임아웃, 캐시 경로, 요청 간격(rate limit) 등 설정값
├── errors.py                  # 공통 예외 클래스 + 에러 코드 enum
├── parsers/
│   ├── manifest_parser.py     # requirements*.txt(글롭)/pyproject.toml(PEP 621·poetry·PDM 문법 모두)/Pipfile/setup.cfg/environment.yml(conda) → requirements-parser, dparse, PyYAML. setup.py는 실행 없이 ast.parse()로 setup() 호출의 install_requires 키워드 인자만 정적 추출(동적 계산은 미지원으로 인정)
│   ├── lock_parser.py         # poetry.lock/Pipfile.lock/requirements-lock.txt → 전이 의존성까지 포함한 정확한 고정 버전 추출(있으면 매니페스트의 범위 버전보다 우선)
│   ├── import_scanner.py      # pipreqs 래퍼(get_all_imports 직접 호출, 표준 라이브러리 제외는 pipreqs에 위임) + 로컬 모듈 제외는 R1 자체 로직(상대 import 무조건 제외, 절대 import는 저장소 내 파일/폴더명 매칭)
│   ├── dockerfile_parser.py   # Dockerfile FROM/RUN pip install/COPY 추출 (dockerfile-parse 라이브러리)
│   └── integration_detector.py # LangChain/MCP 탐지 (import AST 스캔 + mcp.json류 설정파일 탐색)
├── pypi_client.py             # PyPI JSON API 클라이언트 (ETag 캐시, 재시도/백오프)
├── vuln_client.py             # OSV 배치 쿼리 (PyPI 응답에 취약점 정보가 없을 때 보완)
├── sbom_generator.py          # cyclonedx-py 서브프로세스 호출 래퍼
├── merger.py                  # 파서별 결과 병합·중복 제거 → 최종 스키마 조립
├── output_writer.py           # schemas/collector_output.schema.json으로 검증 후 파일 출력
└── tests/
```

## 2. 실행 순서

1. **저장소 확보/검증** — 로컬 경로 또는 git URL. 접근 불가(비공개/삭제/인증필요)면 초기 단계에서 즉시 `status: "failed"`로 중단(뒤 단계 낭비 방지).
2. **매니페스트 파싱** — `requirements*.txt`(글롭 패턴 — `requirements-dev.txt`, `requirements/*.txt` 등 변형 이름·경로 포함) / `pyproject.toml`(PEP 621 표준 `[project.dependencies]`와 poetry `[tool.poetry.dependencies]`, PDM `[tool.pdm]` 문법 모두 지원) / `Pipfile` / `setup.cfg`(`[options] install_requires`) / `environment.yml`(conda — `dependencies:` 리스트 + 그 안의 `- pip:` 하위 섹션)를 찾아 `requirements-parser`, `dparse`, `PyYAML`로 파싱. conda 환경은 AI/ML 계열 에이전트 저장소(torch 등 바이너리 의존성)에서 pip 대신 쓰이는 경우가 실제로 흔해 포함. conda 패키지명이 PyPI와 다른 흔한 사례(`pytorch`→`torch`, `opencv`→`opencv-python` 등)는 최소 하드코딩 매핑 테이블로 두고, 매핑에 없으면 conda 이름 그대로 PyPI 조회 시도 → 실패 시 기존 `PYPI_NOT_FOUND`로 자연스럽게 처리(완전한 매핑을 목표로 하지 않음). 여러 매니페스트가 동시에 있으면 우선순위를 정해 하나를 고르지 않고 **둘 다 파싱해서 `declared_in`에 파일명을 모두 기록**하고, 버전이 서로 다르면 그 사실만 그대로 표시(어느 쪽이 맞는지 R1이 판단하지 않음). 없으면 건너뛰고 3번에 전적으로 의존.
   - **버전 표기 처리**: `pkg==1.0`(정확한 핀)은 그대로 사용. `pkg>=1.0,<2.0`(범위)은 2.5단계 락파일에서 고정 버전을 찾지 못하면 `version: null` + 원본 범위 문자열을 `version_spec`에 보존. `pkg[extra]==1.0`은 이름을 `pkg`로 취급. `pkg @ git+https://...`(VCS 소스)는 PyPI 조회 대상에서 제외하고 `resolution_status: "vcs_source"`로 구분. `-e ./local_pkg`(로컬 editable)는 의존성 목록에서 제외(저장소 자체 코드이므로). 환경 마커(`; python_version >= "3.8"`)는 무시.
2.5. **락파일 파싱** — `poetry.lock`/`Pipfile.lock`/`requirements-lock.txt` 등이 있으면 전이 의존성까지 포함해 정확히 고정된 버전을 추출. 2번에서 범위 버전(`version: null`)으로 남은 항목에 우선 적용해 채움.
2.6. **범위 버전 보완 조회(deps.dev)** — 락파일이 없어서 여전히 `version: null`인 항목(범위 표기, 무선언, Dockerfile 무버전 등 VCS 소스 제외 전부)은 [deps.dev API](https://docs.deps.dev/api/v3/)(무료, 인증 불필요, Google이 전이 의존성까지 고려해 미리 resolve해둔 결과를 원격으로 조회 — 우리 쪽에서 코드 실행 없음)로 보완 시도. 성공하면 `version`이 아니라 별도 필드 `version_hint`에 채움("확정 사실"인 `version`과는 명확히 분리 — R1이 판단한 게 아니라 참고용 추정치임을 명시). wheel 없이 sdist만 배포된 패키지는 deps.dev도 실패할 수 있음(공식 문서에 명시된 한계) — 이 경우 그대로 `version: null`, `version_hint: null`로 남기고 다음 단계로 진행. rate limit이 공개 문서화가 안 돼 있어 구체적인 초당 호출 수를 임의로 정하지 않는다(모르는 걸 아는 것처럼 숫자로 못박는 게 더 위험). 대신 **circuit breaker**: 429/5xx가 연속 N회(예: 3회) 발생하면 이번 실행(run) 동안은 deps.dev 호출 자체를 중단하고 나머지 후보는 전부 `version_hint: null`로 남긴 채 다음 단계로 진행. 캐시(문서상 명시적으로 허용됨)는 그대로 적용.
3. **임포트 스캔** — `pipreqs.get_all_imports()`를 라이브러리로 직접 호출해 실제 import 스캔(표준 라이브러리 제외는 pipreqs 자체 로직에 위임). **로컬 모듈 제외는 R1이 직접 판단**: ① 상대 import(`from . import x`, `from .tools import x`)는 정의상 항상 로컬이므로 검사 없이 제외, ② 절대 import는 맨 앞 이름이 저장소 안에 `<이름>.py` 파일이나 `<이름>/__init__.py`가 있는 폴더로 존재하면 로컬로 판단해 제외(`src/` 레이아웃 대비 저장소 루트와 `src/` 둘 다 검색). 이후 매니페스트/락파일 결과와 비교 → "선언됨/실제사용/양쪽" 태그를 붙여 후보 의존성 목록 확정.
4. **Dockerfile 파싱** (있는 경우) — `FROM` 베이스 이미지, `RUN pip install ...`, `COPY requirements*.txt` 패턴을 `dockerfile-parse`로 추출해 후보 목록에 합침. 베이스 이미지의 OS 패키지(apt 등)는 이번 스코프에서는 이름만 기록하고 PyPI 매칭은 하지 않음.
   - **manifest와 버전이 다를 때**: 락파일과 달리 우선순위를 주지 않는다. 멀티스테이지 빌드/`ARG` 버전 주입/베이스 이미지 기존 설치본 등 정적 파싱만으로는 확신할 수 없는 변수가 많아, Dockerfile 실행 순서를 시뮬레이션해 "최종 승자"를 억지로 추정하지 않는다. `source`에 `"dockerfile"`을 추가하고, manifest 버전과 다르면 다르다는 사실만 그대로 기록한다(2단계 다중 매니페스트 처리와 동일한 원칙).
5. **외부 연동 탐지** — 두 가지 방식을 병행한다.
   - **스캔 대상 파일 범위**: 저장소 내 `.py` 파일 전체를 대상으로 하되, `.gitignore`에 걸리는 경로는 제외하고, **거기에 더해 `.venv/`, `venv/`, `env/`, `site-packages/`, `vendor/`, `.tox/`, `dist-packages/` 같은 서드파티/가상환경 디렉터리 이름은 `.gitignore` 여부와 무관하게 항상 제외**한다(일부 ML 저장소는 가상환경을 통째로 커밋하는 경우가 있어 `.gitignore`만 믿으면 안 됨). 이 제외를 안 하면 `langchain` 라이브러리 자체의 소스 코드를 스캔해서 라이브러리 내부 호출을 "이 저장소가 쓰는 것"으로 오탐하게 됨.
   - **심볼 테이블 구성**: `ast.parse()`로 파일별 심볼 테이블(로컬 이름→정규화된 원본 모듈 경로, alias 포함)을 구성한다. `from X import Y as Z`, `import X as Y` 후 `Y.attr(...)`(속성 접근 호출) 둘 다 이 테이블로 역추적. **`from X import *`(star import)**: 대상 모듈 X가 추적 대상 모듈(`langchain`/`langchain_community`/`langchain_experimental`/`langchain_mcp_adapters`/`mcp`) 계열이면, 그 파일 안에서 카테고리 매핑 테이블에 있는 이름으로 호출되는 게 보일 때 "그 star import에서 왔을 수 있다"고 보고 탐지하되 `via_star_import: true` 플래그를 붙여 일반 매칭과 신뢰도를 구분한다(모듈을 실제로 열어보지 않는 한 100% 확신은 불가능하므로).
   - **카테고리 매핑 시 import 출처 검증**: 클래스 이름만으로 매칭하되(정확한 모듈 경로 강제는 패키지 분리 이슈 때문에 안 함 — 아래 참고), **그 이름이 심볼 테이블상 추적 대상 모듈 계열(`langchain*`/`mcp`)에서 온 것인지는 반드시 확인**한다. 이 확인이 없으면 `from mycompany.utils import ShellTool`처럼 전혀 무관한 동명 클래스도 오탐하게 됨.
   - **(a) 설정 파일 탐색**: 저장소 내 `mcp.json`/`claude_desktop_config.json` 류(`mcpServers` 최상위 키 형태 — `{"mcpServers": {"<name>": {"command"|"url": ..., "transport"?: ...}}}`) 탐색. `command` 있으면 `transport: "stdio"`, `url`만 있으면 명시된 `transport` 또는 기본 `"http_sse"`. 이 래퍼 형식이 아닌 변형 포맷은 v1 미지원.
   - **(b) 코드 내 인라인 설정 탐지(AST)**: `MultiServerMCPClient(...)` 호출을 위 심볼 테이블로 탐지(설정 파일 없이 코드에 직접 넘기는 게 LangChain MCP 통합에서 더 흔한 패턴이라 (a)만으로는 놓침). 호출 자체가 발견되면 어떤 함수(헬퍼/래퍼 포함)에 중첩돼 있어도 파일 전체 순회로 잡히므로 `confidence: "instantiated"`는 그대로 유지됨 — 래퍼로 감싸도 이 판정 자체는 안 깨짐. **한 파일에 호출이 여러 번 있으면 하나로 합치거나 덮어쓰지 않고 각각을 별도 항목으로 전부 기록**(리터럴인 것 하나, 동적인 것 하나 있어도 둘 다 유지 — 정보를 안 버린다는 원칙).
     - **인자 추출**: `ast.literal_eval`은 인자 중 `os.getenv()` 같은 비리터럴이 하나라도 섞이면 전체가 실패하므로 쓰지 않는다. 대신 `ast.Dict` 노드를 직접 순회해 **값이 리터럴인 key만 개별 추출**하고, 동적 값(함수 호출 등)은 해당 항목만 `"<dynamic>"`으로 표시(전체 실패 대신 부분 추출). 인자가 딕셔너리 리터럴이 아니라 변수 이름(`MultiServerMCPClient(CONFIG)`)이면, 바로 포기하지 않고 **같은 렉시컬 스코프 안에서만** 그 이름에 대한 `Assign` 노드를 한 단계 역추적한다 — 호출을 감싸는 가장 가까운 함수/클래스/모듈 본문 범위로 한정하고, 그 범위 밖(다른 함수 등)에 있는 동명 변수는 스코프가 다르므로 후보에서 제외한다(단순 "파일 내 첫 Assign"으로 찾으면 무관한 동명 변수를 잘못 가져다 쓸 위험이 있음 — 값을 못 찾는 것보다 틀린 값을 확신 있게 내놓는 게 더 나쁨). 그 스코프 안에서도 재할당이 여러 번이거나 조건 분기로 값이 갈리면 모호하므로 동적으로 처리. 그래도 못 찾으면 "mcp 연동이 있다"는 사실(confidence: instantiated)만 유지한 채 세부 값은 비움.
   - **성능**: `ast.parse()` 전에 파일 내용에 대상 키워드(`langchain_mcp_adapters`, `MultiServerMCPClient`, `langchain`, `mcp` 등)가 문자열로라도 존재하는지 먼저 정규식/문자열 매칭으로 걸러내는 2단계(사전 필터링 → AST 파싱) 방식을 쓴다. 대상 저장소가 커도 관련 없는 파일에 AST 파싱 비용을 쓰지 않기 위함 — R1의 다른 AST 기반 단계(import 스캔, setup.py 정적 파싱)에도 동일 원칙 적용.
   - **제외 경로**: `tests/`, `test/`, `examples/`, `benchmarks/` 류 디렉터리는 기본적으로 탐지 대상에서 제외한다. 테스트/샘플 코드의 mock 설정은 신뢰도가 낮은 신호가 아니라 애초에 신호가 아니므로, 등급을 매기기보다 걸러내는 쪽을 택함.
   - **확장성**: 카테고리 매핑(아래 표)과 MCP 클라이언트 탐지 대상을 코드에 하드코딩하지 않고 `{모듈, 클래스/함수명, 카테고리}` 형태의 선언적 규칙 테이블로 구조화한다. 향후 FastMCP·LlamaIndex MCP 같은 다른 Python MCP 프레임워크를 지원할 때 규칙 테이블에 행만 추가하면 되도록. JS/TS SDK 등 비Python 생태계는 범위 밖(R1은 PyPI 전용 — npm 락파일 제외 결정과 동일 원칙).
   - **LangChain 내장 툴 식별**: 위 심볼 테이블+import 출처 검증을 거쳐 `ast.Call` 노드까지 확인해 실제 인스턴스화가 보이면 `confidence: "instantiated"`, import만 있고 인스턴스화가 안 보이면 `confidence: "import_only"`로 구분(신뢰도만 낮추고 버리지 않음). `mcp`/`langchain_mcp_adapters` 모듈은 특정 클래스 구분 없이 import 자체로 "mcp" 연동 태깅. **한계**: 클래스를 다른 파일로 넘겨 나중에 호출하는 크로스파일 패턴은 추적하지 않음(가벼운 정적 스캐너 스코프 밖으로 인정).
   - **카테고리 매핑 테이블**(초기 목록, 완전한 목록을 목표로 하지 않음 — 매핑에 없는 클래스는 태깅하지 않음): `shell` — `ShellTool`/`PythonREPLTool`/`PythonAstREPLTool`. `network` — `RequestsGetTool`/`RequestsPostTool`/`TavilySearchResults`/`DuckDuckGoSearchRun`/`SerpAPIWrapper` 계열/`WikipediaQueryRun`. `filesystem` — `ReadFileTool`/`WriteFileTool`/`ListDirectoryTool`/`CopyFileTool`/`DeleteFileTool`/`MoveFileTool`/`FileSearchTool`. 정확한 모듈 경로(`langchain.tools` vs `langchain_community.tools` 등)는 강제하지 않고 클래스 이름으로만 매칭하되(패키지 분리 이슈 회피), 위 "import 출처 검증"으로 무관한 동명 클래스는 걸러냄.
   - 탐지 결과를 어떤 패키지가 유발했는지 패키지 단위로도 매핑(예: `langchain` → `["shell", "mcp"]`). 설정파일 파싱 실패는 해당 파일만 스킵하고 `errors[]`에 기록(파이프라인 계속). 원격 MCP 서버처럼 실제 접속이 불가능한 경우도 설정에 선언된 사실만 기록하고 실제 연결은 시도하지 않는다(정적 탐지 범위). **주의**: 이 탐지 결과가 최종적으로 채워야 할 `agent.permissions[].type` enum 자체는 R4(Attack Path Engine)가 정의하기로 되어 있어(§확정 사항 1 참고), R1은 "무엇을 탐지할 수 있는가"까지만 설계하고 enum 확정은 R4와 별도 조율한다.
6. **PyPI 메타데이터 조회** — 이름만으로도 `GET /pypi/<name>/json` 호출 가능(버전 없어도 최신 기준 정보가 옴 — license/latest_version/maintainer_count 등은 `version`이 `null`인 패키지도 정상 수집됨). ETag 캐시 사용, 클라이언트 자체 요청 간격 제한(기본 5 req/s 토큰버킷 — PyPI는 공식적으로 하드 레이트리밋은 없지만 예의상 자체 제한). `vulnerabilities` 필드 우선 사용.
7. **취약점 보완 조회** — PyPI 응답에 `vulnerabilities`가 비어있는 패키지만 모아 OSV `/v1/querybatch`로 보완 조회. **`version`(또는 2.6단계의 `version_hint`)이 있으면 그 버전으로 매칭해 조회**, 정확히 그 버전에 해당하는 취약점만 받음. 둘 다 없는 경우(순수 `unresolved`)엔 **패키지 이름만으로 조회**해 "역사상 이 패키지에 있었던 모든 취약점"을 받되, 각 항목에 `version_matched: false`를 붙여 "이 설치본에 실제로 해당하는지 확인 안 됨"을 명시한다. `version_hint`로 매칭한 경우도 확정 사실이 아니므로 `version_matched: "estimated"`로 구분해 완전한 확신(`true`)과 다르게 표시한다. R1은 조회 자체를 스킵하지 않는다 — 정보를 지우는 것보다 신뢰도를 낮춰 표시하고 넘기는 쪽이, "판단은 안 하고 사실만 넘긴다"는 원칙에 맞다.
8. **SBOM 생성** — `cyclonedx-py requirements`(또는 environment/poetry)로 CycloneDX JSON 생성. 실패 시 경고만 남기고 dependency_list는 그대로 출력(SBOM 없이도 부분 결과 제공).
9. **병합·검증·출력** — 전체 결과를 `schemas/collector_output.schema.json`에 맞춰 조립, 로컬 검증 후 저장.

## 2-1. 검토했지만 채택하지 않은 의존성 추출 기법

의존성 추출 방법을 더 넓게 검토하면서(매니페스트/import/Dockerfile/락파일 외에) 아래 기법들도 후보에 있었으나, 각각 이유가 있어 이번 스코프에서는 제외한다.

- **환경 인트로스펙션(실제 설치 후 의존성 트리 추출)** — 저장소 코드를 실제로 `pip install`해야 하는데, 검증되지 않은(잠재적으로 악성일 수 있는) 코드를 우리 환경에서 실행하게 되는 리스크가 있어 제외.
- **바이너리/설치 이미지 레이어 스캔** — R1 역할 범위에 이미 명시된 "컨테이너 OS 패키지 심층 분석 제외"와 같은 범주. 이미지를 직접 빌드/열람해야 하는 인프라 부담도 있어 제외.
- **setup.py 동적 실행** — 서드파티 의존성은 PyPI가 배포 시점에 이미 `setup.py`를 실행해 메타데이터(`requires_dist`)를 공개해두므로 우리가 다시 실행할 필요가 없음(6단계에서 그대로 재사용). 스캔 대상 저장소 자신의 `setup.py`는 `ast.parse()`로 `setup()` 호출의 `install_requires` 인자를 **실행 없이** 정적으로만 추출하고, 인자가 동적으로 계산되는 경우(파일 읽기 등 실행이 있어야 값을 아는 경우)는 지원하지 않는 것으로 인정한다 — 의존성 목록에 없는 임의 코드를 실행하는 것 자체가 이 프로젝트의 위협 모델(악성 패키지 탐지)과 정면으로 배치되기 때문.
- **벤더링 코드 탐지**(패키지 매니저를 거치지 않고 소스에 직접 복붙된 서드파티 코드를 라이선스 헤더/해시로 탐지) — 해시 기반으로 제대로 하려면 PyPI 전체 패키지의 파일 해시 코퍼스가 필요해 과함. 라이선스 헤더만 보는 가벼운 버전은 구현은 쉽지만, 정상적인(라이선스를 지키며 출처를 남긴) 양성 벤더링과 구분이 안 되고 정작 숨기려는 악성 벤더링은 헤더를 안 남기므로 탐지 효과가 낮아 전체 제외.
- **npm 락파일 파싱** — 현재 설계·R3 역할 범위 모두 PyPI 생태계를 전제로 하고 있어 제외. (에이전트가 JS 기반일 수 있는지는 총괄 레벨에서 스코프 확정 필요 — 보류 목록 참고)

## 3. 에러 처리 원칙

- 모든 에러는 `{stage, code, message, package?}` 구조로 `errors[]` 배열에 누적 — 하나 실패해도 파이프라인 전체를 죽이지 않음(예외: 1단계 저장소 접근 실패는 즉시 중단).
- 대표 에러 코드: `REPO_UNREACHABLE`, `REPO_PRIVATE_AUTH_REQUIRED`, `MANIFEST_PARSE_FAILED`(스킵), `IMPORT_SCAN_FAILED`(스킵), `AST_PARSE_FAILED`(대상 저장소의 Python 버전이 수집기 실행 환경보다 높아 `ast.parse()`가 `SyntaxError`를 던지는 경우 등 — `ast.parse()`를 쓰는 모든 단계(import 스캔, setup.py 정적 파싱, 외부 연동 탐지) 공통. 해당 파일만 스킵, 전체 파서는 안 죽음), `PYPI_NOT_FOUND`(패키지 `resolution_status: "unresolved"`로 표시 후 계속), `PYPI_RATE_LIMIT_OR_5XX`(지수 백오프 최대 3회 후 unresolved), `DEPS_DEV_LOOKUP_FAILED`(2.6단계 실패 — `version_hint: null`로 두고 계속, 치명적 아님), `SBOM_GENERATION_FAILED`(스킵).
- 최종 `status`는 `success`(에러 없음) / `partial`(일부 스킵) / `failed`(치명적 중단) 3단계.
- **메모**: `environment.yml`의 최상위 `dependencies:` 목록은 conda 패키지(PyPI와 이름이 다를 수 있음, 예: `pytorch` vs PyPI `torch`)이고 `- pip:` 하위 목록만 실제 PyPI 패키지다. 구현 시 이 둘을 구분해서 처리해야 conda 전용 패키지가 `PYPI_NOT_FOUND`로 잘못 처리되는 걸 막을 수 있음(아직 매핑 규칙 미확정 — 후속 과제).

## 2-2. 중간 산출물 — `Dependency` 객체 (2~4단계 병합 결과, 최종 스키마 아님)

2~4단계(매니페스트/락파일/import/Dockerfile)를 병합한 결과로, 5단계 이후(외부 연동 태깅, PyPI/취약점 조회, 최종 SBOM 조립)가 받아쓰는 **내부 계약**. `schemas/collector_output.schema.json`과는 별개이며, 최종 스키마로의 변환은 9단계(병합·출력)에서 처리한다.

```json
{
  "name": "pyyaml",
  "version": "5.3.1",
  "version_spec": null,
  "version_hint": null,
  "extras": [],
  "vcs_url": null,
  "ecosystem": "PyPI",
  "is_transitive": false,
  "source": ["manifest", "dockerfile"],
  "declared_in": ["requirements.txt", "Dockerfile"],
  "resolution_status": "resolved",
  "version_conflicts": [
    { "value": "5.4.1", "declared_in": "Dockerfile" }
  ]
}
```

필드 설명:
- `version`: 가장 신뢰도 높은 확정 버전(정확한 핀 또는 락파일 고정값). 없으면 `null`.
- `version_spec`: 원본 범위 표기 문자열(범위였는데 락파일로 못 풂 경우만 채움).
- `version_hint`: 2.6단계(deps.dev) 조회로 얻은 참고용 추정 버전. `version`과 절대 혼동되지 않도록 분리.
- `extras`: `pkg[extra]` 형태의 extras 목록.
- `vcs_url`: VCS 소스일 때만 채움(`resolution_status: "vcs_source"`와 함께).
- `is_transitive`: 락파일에서만 발견되고 매니페스트/import/Dockerfile 어디에도 직접 선언이 없으면 `true`. **취약점의 위험도 자체와는 무관**(전이 의존성이라고 덜 위험한 건 아님 — 실행되는 코드는 동일) — R2의 위험 점수 계산 입력이 아니라, R4/Dashboard가 "이 취약점이 어떤 경로로 들어왔는지" 보여줄 때 쓰라고 제공하는 조치(remediation) 참고용 정보.
- `source`: `"manifest"` / `"import"` / `"dockerfile"` / `"lockfile"` 중 발견된 출처 전부.
- `declared_in`: 실제 파일 경로 전부(여러 개일 수 있음).
- `resolution_status`: `"resolved"`(확정 버전 있음) / `"unresolved"`(버전 모름) / `"vcs_source"`(VCS 소스라 버전 개념 없음).
- `version_conflicts`: manifest·Dockerfile 등 여러 출처에서 서로 다른 버전이 나왔을 때, `version`에 채택되지 않은 나머지 값들을 그대로 보존(어느 쪽이 맞는지 R1이 판단하지 않음).

로컬 editable(`-e ./local_pkg`)은 이 목록 자체에 포함되지 않는다(의도된 제외).

## 4. 출력 스키마 초안 (`schemas/collector_output.schema.json`)

실제 필드 구조와 값 예시는 [`03-data-contracts.md`](03-data-contracts.md)와 [`04-sample-dataset.md`](04-sample-dataset.md) 참고. 스키마 확정에는 `CONTRIBUTING.md` 규칙에 따라 Risk Analyzer·ML 담당자 승인이 필요합니다.

## 확정 사항 (교차검토 반영)

> ⚠️ **시뮬레이션 초안**: 아래는 실제 팀 교차검토가 아니라 여러 모듈 관점을 미리 가정해서 만든 초안입니다. 실제 담당자와 교차검토 후 다르게 결론 나면 그 내용으로 갱신하세요 (근거는 `docs/review/decisions.md`에).

1. **`cvss_base_score` 인라인 제공 (Risk Analyzer Q1)** — 예. OSV 응답의 `severity`(CVSS 벡터)를 파싱해 `cvss_base_score`(숫자) + `cvss_source`(`nvd`/`osv` 등)로 `vulnerabilities[]`에 직접 포함합니다. 파싱 불가 시 `cvss_base_score: null`.
2. **`external_integrations[]` 필드 추가 (Risk Analyzer Q2)** — 예. 5단계 외부 연동 탐지 결과를 패키지 단위로도 태깅해 각 dependency에 `external_integrations: ["network"|"shell"|"mcp"|"filesystem"]` 배열을 추가합니다. (기존 top-level `integrations[]`는 유지, 이건 패키지-연동 매핑용.)
3. **`latest_release_date`/`maintainer_count` 항상 존재 보장 (Risk Analyzer Q3)** — 완전 보장은 불가(PyPI가 일부 패키지에 정보 미제공). 대신 필드를 항상 present로 두되 값이 없으면 `null` + `data_status: "not_available"`을 명시해 staleness score 계산 시 결측을 구분할 수 있게 합니다.
4. **배포 파일 경로/해시 포함 (ML Q4)** — 예. `distribution_files[]`에 sdist/wheel 파일명, 다운로드 URL, sha256 해시를 포함합니다(정적 분석 시 실제 파일 매칭용).
5. **maintainer 계정 생성일 수집 (ML Q5)** — 기본 미수집(No). PyPI JSON API가 계정 생성일을 제공하지 않아 유저 페이지 추가 스크래핑이 필요하고 요청량이 커집니다. 대신 스키마에 `maintainer_accounts[].account_created_at`을 `null` + `data_status: "not_collected"`로 예약해두어, 추후 필요성이 확정되면 별도 수집기를 붙일 수 있게 합니다. (이견 있으면 논의 환영)
