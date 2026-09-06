# 기술 설계 문서 — Dependency Collector (`collector/`)

> 관련 자료: `study_week1/README.md` §5, `architecture.html` #collector, `GIT_POLICY.md` §3(스키마 계약)

## 1. 모듈 구조 (제안)

```
collector/
├── cli.py                     # 진입점 (python -m collector --repo <path|url>)
├── config.py                  # 타임아웃, 캐시 경로, 요청 간격(rate limit) 등 설정값
├── errors.py                  # 공통 예외 클래스 + 에러 코드 enum
├── parsers/
│   ├── manifest_parser.py     # requirements.txt/pyproject.toml/Pipfile → requirements-parser, dparse
│   ├── import_scanner.py      # pipreqs 래퍼 + --diff 로직
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
2. **매니페스트 파싱** — requirements.txt / pyproject.toml / Pipfile / package.json을 찾아 `requirements-parser`, `dparse`로 파싱. 없으면 건너뛰고 3번에 전적으로 의존.
3. **임포트 스캔** — `pipreqs`로 실제 import 스캔, 매니페스트 결과와 `--diff` 비교 → "선언됨/실제사용/양쪽" 태그를 붙여 후보 의존성 목록 확정.
4. **Dockerfile 파싱** (있는 경우) — `FROM` 베이스 이미지, `RUN pip install ...`, `COPY requirements*.txt` 패턴을 `dockerfile-parse`로 추출해 후보 목록에 합침. 베이스 이미지의 OS 패키지(apt 등)는 이번 스코프에서는 이름만 기록하고 PyPI 매칭은 하지 않음.
5. **외부 연동 탐지** — import 구문에서 `langchain`, `langchain_mcp_adapters`, `mcp` 패턴 매칭 + 저장소 내 `mcp.json`/`claude_desktop_config.json` 류 설정 파일 탐색으로 로컬/원격 MCP 서버, LangChain 내장 툴을 식별.
6. **PyPI 메타데이터 조회** — 확정된 패키지마다 `GET /pypi/<name>/json` 호출. ETag 캐시 사용, 클라이언트 자체 요청 간격 제한(기본 5 req/s 토큰버킷 — PyPI는 공식적으로 하드 레이트리밋은 없지만 예의상 자체 제한). `vulnerabilities` 필드 우선 사용.
7. **취약점 보완 조회** — PyPI 응답에 `vulnerabilities`가 비어있는 패키지만 모아 OSV `/v1/querybatch`로 보완 조회.
8. **SBOM 생성** — `cyclonedx-py requirements`(또는 environment/poetry)로 CycloneDX JSON 생성. 실패 시 경고만 남기고 dependency_list는 그대로 출력(SBOM 없이도 부분 결과 제공).
9. **병합·검증·출력** — 전체 결과를 `schemas/collector_output.schema.json`에 맞춰 조립, 로컬 검증 후 저장.

## 3. 에러 처리 원칙

- 모든 에러는 `{stage, code, message, package?}` 구조로 `errors[]` 배열에 누적 — 하나 실패해도 파이프라인 전체를 죽이지 않음(예외: 1단계 저장소 접근 실패는 즉시 중단).
- 대표 에러 코드: `REPO_UNREACHABLE`, `REPO_PRIVATE_AUTH_REQUIRED`, `MANIFEST_PARSE_FAILED`(스킵), `IMPORT_SCAN_FAILED`(스킵), `PYPI_NOT_FOUND`(패키지 `resolution_status: "unresolved"`로 표시 후 계속), `PYPI_RATE_LIMIT_OR_5XX`(지수 백오프 최대 3회 후 unresolved), `SBOM_GENERATION_FAILED`(스킵).
- 최종 `status`는 `success`(에러 없음) / `partial`(일부 스킵) / `failed`(치명적 중단) 3단계.

## 4. 출력 스키마 초안 (`schemas/collector_output.schema.json`)

```json
{
  "schema_version": "0.1.0",
  "scan_id": "uuid",
  "repo": { "url": "https://github.com/org/agent-repo", "commit_sha": "abc123", "scanned_at": "2026-09-06T12:00:00Z" },
  "status": "partial",
  "dependencies": [
    {
      "name": "langchain",
      "version": "0.3.5",
      "ecosystem": "pypi",
      "source": ["manifest", "import"],
      "declared_in": ["requirements.txt"],
      "resolution_status": "resolved",
      "pypi": {
        "latest_version": "0.3.7",
        "summary": "Building applications with LLMs",
        "license": "MIT",
        "home_page": "https://langchain.com",
        "last_release_at": "2026-08-01T00:00:00Z"
      },
      "hashes": [{ "algo": "sha256", "value": "..." }],
      "distribution_files": [
        { "filename": "langchain-0.3.5-py3-none-any.whl", "url": "https://files.pythonhosted.org/.../langchain-0.3.5-py3-none-any.whl", "hashes": [{ "algo": "sha256", "value": "..." }] }
      ],
      "vulnerabilities": [
        { "id": "GHSA-xxxx", "aliases": ["CVE-2026-0001"], "severity": "HIGH", "cvss_base_score": 8.1, "cvss_source": "nvd", "fixed_versions": ["0.3.6"], "osv_url": "https://osv.dev/vulnerability/GHSA-xxxx" }
      ],
      "maintainers": {
        "maintainer_count": 3,
        "data_status": "ok",
        "maintainer_accounts": [
          { "username": "example", "account_created_at": null, "data_status": "not_collected" }
        ]
      },
      "external_integrations": ["network", "shell"]
    }
  ],
  "integrations": [
    { "type": "mcp_remote", "name": "filesystem-server", "detected_in": "config/mcp.json", "transport": "http_sse" },
    { "type": "langchain_builtin_tool", "name": "SerpAPIWrapper", "detected_in": "agent.py" }
  ],
  "sbom": { "format": "CycloneDX", "spec_version": "1.6", "generator": "cyclonedx-py", "file_ref": "sbom.json" },
  "errors": [
    { "stage": "pypi_client", "code": "PYPI_NOT_FOUND", "message": "package 'internal-tool' not found on PyPI", "package": "internal-tool" }
  ],
  "summary": { "total_dependencies": 42, "resolved": 40, "unresolved": 2, "vulnerable_count": 3, "integrations_count": 2 }
}
```

이 문서는 DRAFT이며, `GIT_POLICY.md` 규칙에 따라 `schemas/collector_output.schema.json`으로 확정하려면 Risk Analyzer·ML 담당자 승인이 필요합니다.

## 확정 사항 (교차검토 반영)

1. **`cvss_base_score` 인라인 제공 (Risk Analyzer Q1)** — 예. OSV 응답의 `severity`(CVSS 벡터)를 파싱해 `cvss_base_score`(숫자) + `cvss_source`(`nvd`/`osv` 등)로 `vulnerabilities[]`에 직접 포함합니다. 파싱 불가 시 `cvss_base_score: null`.
2. **`external_integrations[]` 필드 추가 (Risk Analyzer Q2)** — 예. 5단계 외부 연동 탐지 결과를 패키지 단위로도 태깅해 각 dependency에 `external_integrations: ["network"|"shell"|"mcp"|"filesystem"]` 배열을 추가합니다. (기존 top-level `integrations[]`는 유지, 이건 패키지-연동 매핑용.)
3. **`latest_release_date`/`maintainer_count` 항상 존재 보장 (Risk Analyzer Q3)** — 완전 보장은 불가(PyPI가 일부 패키지에 정보 미제공). 대신 필드를 항상 present로 두되 값이 없으면 `null` + `data_status: "not_available"`을 명시해 staleness score 계산 시 결측을 구분할 수 있게 합니다.
4. **배포 파일 경로/해시 포함 (ML Q4)** — 예. `distribution_files[]`에 sdist/wheel 파일명, 다운로드 URL, sha256 해시를 포함합니다(정적 분석 시 실제 파일 매칭용).
5. **maintainer 계정 생성일 수집 (ML Q5)** — 기본 미수집(No). PyPI JSON API가 계정 생성일을 제공하지 않아 유저 페이지 추가 스크래핑이 필요하고 요청량이 커집니다. 대신 스키마에 `maintainer_accounts[].account_created_at`을 `null` + `data_status: "not_collected"`로 예약해두어, 추후 필요성이 확정되면 별도 수집기를 붙일 수 있게 합니다. (이견 있으면 논의 환영)
