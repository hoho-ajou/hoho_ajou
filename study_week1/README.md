# 1주차 학습자료 — 전체 프로젝트 흐름 & Dependency Collector

> raw 파일은 WebFetch(AI가 본문을 읽어 마크다운으로 정리)로 추출한 것이라, 사이트 원문과 100% 바이트 단위로 동일하진 않습니다. 표·수치·인용문·코드는 원문 그대로 옮겼습니다. 완전한 원문이 필요하면 각 섹션의 URL로 직접 들어가세요.

## 🧭 아키텍처 그림

전체 그림이 먼저 필요하면 [`architecture.html`](architecture.html)을 브라우저로 열어보세요. 5개 모듈이 뭘 하고 서로 뭘 주고받는지 한 장으로 그려뒀습니다.

## 📖 읽는 순서 (추천)

처음이라면 위에서 아래로 순서대로 읽으세요. 각 단계는 앞 단계를 전제로 합니다.

1. **[TL;DR](#-tldr-5분-요약)** — 5분 요약, 전체 그림부터 잡기
2. **[왜 이 문제가 중요한가](#1-배경--왜-ai-에이전트-공급망-보안인가)** — 배경
3. **[실제 사건으로 체감하기](#2-실제-공격-사례-3가지)** — 사례 3개
4. **[핵심 용어](#3-핵심-용어-사전-가나다순)** — 모르는 단어 나올 때마다 참고 (가나다순 사전)
5. **[유사 프로젝트 비교](#4-유사-프로젝트--서비스-경쟁참고-대상)** — 남들은 어떻게 풀었나
6. **[Dependency Collector 구현 가이드](#5-dependency-collector-모듈---실제로-뭘-만드는가)** — 우리가 만들 것
7. **[MCP 딥다이브](#6-mcpmodel-context-protocol--collector가-탐지해야-할-대상)** — 심화
8. **[직접 해보기](#7-직접-해보기-hands-on)** — 손으로 익히기
9. **[FAQ](#8-자주-헷갈리는-것-faq)**

---

## 🎯 TL;DR (5분 요약)

- AI 에이전트(LangChain·MCP 등)는 외부 라이브러리·도구에 강하게 의존한다 → **의존성 자체가 공격 표면**
- 공급망 공격의 대표 유형: **타이포스쿼팅**(이름 비슷한 가짜 패키지), **악성 유지보수자 침투**(xz-utils 사례처럼 2년 넘게 신뢰를 쌓은 뒤 배신), **모델 파일 자체의 악성코드**
- 업계는 이미 이 문제를 **SBOM(부품 명세서) 생성 → SCA(구성요소 분석) → 취약점 매칭**의 3단계로 표준화해서 풀고 있음 (Syft, Snyk, Dependabot 등)
- 우리 팀의 차별점: 여기에 **AI 에이전트의 권한 그래프**를 더해서 "그 취약점이 실제로 에이전트의 어떤 권한과 연결되는가"까지 본다 (CNAPP의 공격경로 분석 방법론을 AI 에이전트에 적용)
- **Dependency Collector**는 이 전체 파이프라인의 입구: 코드에서 의존성을 뽑아내고(파싱 or 임포트 스캔), PyPI API로 메타데이터를 채우고, SBOM을 생성하는 모듈

---

## 1. 배경 — 왜 AI 에이전트 공급망 보안인가

AI 에이전트는 LLM 혼자 동작하지 않고 **외부 도구·라이브러리·API에 강하게 의존**합니다. 이 의존성 자체가 공격 표면이 됩니다.

- 오토노머스 에이전트의 대표 리스크: 프롬프트 인젝션, 툴 오남용/권한 상승, 메모리 포이즈닝, 연쇄 실패, **공급망 공격**
- IBM 2026 X-Force: 2020년 대비 공급망·제3자 침해가 약 4배 증가 — CI/CD 자동화와 SaaS 연동 사이의 신뢰 관계를 공격자가 악용
- 오케스트레이터 에이전트가 여러 하위 에이전트의 API 키를 들고 있는 구조라면, 오케스트레이터 하나만 뚫려도 전체가 뚫림 — 우리 **Risk Analyzer**가 다루는 지점
- JFrog 2026 리포트 수치로 보는 규모감:
  - 2025년 악성 npm 패키지 **451% 급증**(17만개 이상)
  - 신규 패키지 **1,170만 개**가 기업 공급망에 유입(전년비 +67%)
  - 공개 레지스트리에서 **약 500개의 악성 AI 모델** 발견
  - CVE는 4.8만 건 신규 공시(+20%)됐지만 "Critical" 중 실제 악용 가능한 건 **12%뿐** → 그냥 목록 나열이 아니라 우선순위화가 왜 중요한지 보여주는 수치

원문 → [`01_socket_ai_agents_supply_chain.md`](raw/01_socket_ai_agents_supply_chain.md) · [`02_esecurityplanet_ai_threats_2026.md`](raw/02_esecurityplanet_ai_threats_2026.md)

---

## 2. 실제 공격 사례 3가지

이론보다 사례가 기억에 남습니다. 난이도 순으로 배치했습니다.

### 사례 1 — colorama/colorizr 타이포스쿼팅 (가장 단순한 유형)
PyPI의 `colorama`(파이썬)와 NPM의 `colorizr`(자바스크립트) 이름을 헷갈리게 만든 가짜 패키지들. Windows에서는 레지스트리에서 환경변수를 탈취하고 작업 스케줄러로 지속성을 확보하며 백신을 회피, Linux에서는 RSA 키를 배포하고 `gs-netcat`으로 암호화된 역쉘을 열어 Pastebin으로 데이터를 유출. 패키지 소유자 계정명, 파일 해시(SHA256)까지 실제로 공개된 분석 사례.

→ **왜 중요한가**: 우리 Risk Analyzer가 잡아야 할 "이름 유사도 기반 탐지"가 정확히 이 유형을 겨냥합니다.

원문 → [`06_jfrog_typosquatting.md`](raw/06_jfrog_typosquatting.md) · [`07_checkmarx_colorama.md`](raw/07_checkmarx_colorama.md)

### 사례 2 — xz-utils 백도어 (CVE-2024-3094) — 역사상 가장 정교한 오픈소스 공급망 공격
"Jia Tan"이라는 인물이 **2년 넘게** xz-utils 프로젝트에 정상적으로 기여하며 신뢰를 쌓고 메인테이너 권한까지 얻은 뒤, 2023년 12월 배포판(v5.6.0)에 백도어를 몰래 심음. 이 백도어는 `sshd`가 사용하는 OpenSSL 함수를 가로채 특정 개인키를 가진 공격자에게 원격 코드 실행을 허용. GitHub 저장소가 아니라 **배포(릴리즈) 버전에만** 숨겨져 있어서 코드 리뷰로는 못 찾음. 발견 경위도 극적인데, 마이크로소프트 엔지니어가 PostgreSQL 성능 이슈를 디버깅하다가 "SSH 로그인이 0.5초 더 걸린다"는 사소한 이상을 알아채면서 우연히 드러남.

→ **왜 중요한가**: 단순 자동 스캔으로는 절대 못 잡는 유형. "메인테이너 자체가 위협"이라는 점에서, 우리가 다루는 "의존성 유지보수 상태" 체크(마지막 업데이트, 메인테이너 수 등)가 왜 위험 신호가 되는지 보여주는 최고의 사례.

원문 → [`13_datadog_xz_utils_backdoor.md`](raw/13_datadog_xz_utils_backdoor.md)

### 사례 3 — AI 모델 파일 자체의 악성코드
공개 모델 레지스트리(Hugging Face 등)에서 포이즈닝된 모델 파일을 로드하면 임의 코드가 실행되는 사례들이 발견됨. 조직의 53%가 모델을 공개 레지스트리에서 직접 받아쓰는데, 검증 없이 받으면 그대로 침투 경로가 됨.

→ **왜 중요한가**: 우리 프로젝트 범위(PyPI 패키지)를 넘어서는 위협이지만, "AI 에이전트 생태계 전체가 공급망 공격의 신흥 표적"이라는 배경 논리를 뒷받침하는 근거.

원문 → [`02_esecurityplanet_ai_threats_2026.md`](raw/02_esecurityplanet_ai_threats_2026.md)

---

## 3. 핵심 용어 사전 (가나다순)

| 용어 | 뜻 |
|---|---|
| **CNAPP** | 클라우드 네이티브 애플리케이션 보호 플랫폼. 자산·권한·네트워크를 그래프로 연결해 공격 경로를 찾는 방식 — Attack Path Engine이 참고할 방법론 |
| **CVE** | 공개적으로 등록된 특정 취약점의 식별번호 (예: CVE-2024-3094) |
| **CVSS** | 취약점의 심각도를 점수(0~10)로 매기는 업계 표준 지표 — Risk Analyzer의 위험도 점수화 설계에 참고 |
| **MCP** (Model Context Protocol) | LLM 앱이 외부 도구·데이터에 표준화된 방식으로 접근하게 해주는 오픈 프로토콜. "AI용 USB 포트"에 비유됨. Host→Client→Server 구조, JSON-RPC 2.0 기반 |
| **OSV** (Open Source Vulnerabilities) | 구글이 운영하는 무료 오픈소스 취약점 데이터베이스/API. 패키지명+버전만 보내면 알려진 취약점을 알려줌 |
| **PURL** (Package URL) | 패키지를 생태계+이름+버전까지 정확히 식별하는 표준 URL 형식 (예: `pkg:pypi/requests@2.31.0`) |
| **SBOM** (Software Bill of Materials) | 소프트웨어에 들어간 라이브러리·패키지·라이선스를 전부 나열한 "부품 명세서". 자동차 부품표처럼, 앱이 어떤 의존성으로 구성됐는지 목록화한 것 |
| **SCA** (Software Composition Analysis) | 오픈소스 구성요소를 자동으로 식별하고 알려진 취약점·라이선스 문제를 찾는 분석 기법 — 우리 프로젝트 전체의 기반 개념 |
| **SPDX / CycloneDX** | SBOM을 기계가 읽을 수 있게 표현하는 두 가지 표준 포맷. CycloneDX는 보안(취약점) 중심, SPDX는 라이선스·법적 컴플라이언스 중심 |
| **reachability 분석** | 취약한 함수가 실제로 내 코드에서 호출되는지까지 추적하는 기법(Snyk 등). 호출 안 되면 우선순위를 낮춤 — 오탐(노이즈) 감소용 |
| **타이포스쿼팅** | 인기 패키지와 이름이 한두 글자 다른 가짜 패키지를 올려 오타로 설치를 유도하는 공격 (예: requests → requets) |

---

## 4. 유사 프로젝트 · 서비스 (경쟁/참고 대상)

| 도구 | 하는 일 | 우리와 다른 점 |
|---|---|---|
| **Dependabot** (GitHub) | 새 버전 나오면 자동으로 PR 생성. 무료, GitHub Advisory Database(2만+ 건) 기반 | 취약점 자체를 깊이 스캔하진 않음. AI 에이전트 권한과 연결하지 않음 |
| **Snyk** | 알려진 CVE를 탐지. 자체 DB가 커서 평균 47일 더 빨리 탐지, reachability 분석으로 노이즈 감소 | 설치된 의존성 사후 모니터링 중심. 에이전트 권한 그래프 없음 |
| **Socket.dev** | 설치 전 패키지의 악성 행위를 행동 분석으로 탐지(신종 악성코드 포함) | 우리 ML 이상탐지와 목적이 가장 비슷함. AI 에이전트 특화는 아님 |
| **Syft / cyclonedx-python** | 오픈소스 SBOM 생성기. 다양한 매니페스트(requirements.txt, Poetry, 환경 전체)에서 SBOM 추출 | Dependency Collector가 SBOM 생성 시 그대로 가져다 쓸 수 있는 오픈소스 도구 |
| **CNAPP 계열** (Wiz, Sysdig 등) | 클라우드 자산-권한-네트워크를 그래프로 연결해 공격 경로 도출 | 클라우드 인프라 대상. 우리는 이 "그래프로 공격경로 찾기" 방법론을 AI 에이전트 대상으로 옮기는 것 |
| **OSV API** (osv.dev) | 오픈소스 취약점을 무료로 조회하는 API | Dependency Collector가 수집한 패키지의 취약점 조회에 바로 쓸 수 있음 |

원문 → [`03_fossa_sbom_examples.md`](raw/03_fossa_sbom_examples.md) · [`04_appsecsanta_snyk_vs_dependabot.md`](raw/04_appsecsanta_snyk_vs_dependabot.md) · [`05_wiz_attack_path_analysis.md`](raw/05_wiz_attack_path_analysis.md) · [`11_jit_syft_grype_guide.md`](raw/11_jit_syft_grype_guide.md)

---

## 5. Dependency Collector 모듈 — 실제로 뭘 만드는가

**목표**: AI 에이전트 프로젝트의 소스코드를 스캔해서 (1) 의존성 목록, (2) 외부 연동 도구(LangChain·MCP 등), (3) PyPI 메타데이터·취약점을 자동으로 뽑아내는 모듈

### 5-1. 의존성을 뽑아내는 두 가지 방식

| 방식 | 도구 | 장점 | 단점 |
|---|---|---|---|
| **매니페스트 파싱** | `requirements-parser`, `dparse`, 표준 JSON 파서(package.json) | 정확하고 빠름 | 애초에 requirements.txt가 없거나 부실하면 못 씀 |
| **실제 임포트 스캔** | `pipreqs` | 코드에 실제로 `import`된 것만 잡아냄, requirements.txt가 없어도 동작 | 동적 임포트는 못 잡을 수 있음 |

**실전 팁**: AI 에이전트 오픈소스 프로젝트는 종종 requirements.txt가 부실합니다. 이럴 때 `pipreqs`로 실제 임포트를 먼저 스캔하고, 있는 requirements.txt와 `--diff`로 비교하면 "누락된 의존성"까지 잡아낼 수 있습니다.

원문 → [`10_pypi_requirements_parser.md`](raw/10_pypi_requirements_parser.md) · [`14_pipreqs_github.md`](raw/14_pipreqs_github.md) · [`12_dev_dependency_scanner_python.md`](raw/12_dev_dependency_scanner_python.md)

### 5-2. PyPI API로 메타데이터 + 취약점 한 번에 가져오기

```
GET https://pypi.org/pypi/<패키지명>/json
```

이 한 번의 호출로 얻는 것:
- `info`: 최신 버전, 작성자, 의존성(classifiers 등)
- `urls`: 배포 파일 해시(MD5/SHA256/BLAKE2b-256) — 무결성 검증에 활용 가능
- **`vulnerabilities`**: 이 패키지의 알려진 취약점 목록이 OSV 링크와 함께 바로 들어있음 — 별도 API 호출 없이 기초 취약점 확인 가능

더 정밀한 취약점 조회가 필요하면 OSV API를 직접 호출:
```bash
curl -X POST https://api.osv.dev/v1/query \
  -H "Content-Type: application/json" \
  -d '{"package": {"name": "flask", "ecosystem": "PyPI"}, "version": "2.0.1"}'
```

원문 → [`15_pypi_json_api_docs.md`](raw/15_pypi_json_api_docs.md) · [`17_osv_api_query_endpoint.md`](raw/17_osv_api_query_endpoint.md)

### 5-3. SBOM 생성

수집된 의존성 목록을 표준 포맷(SBOM)으로 내보내면, 다음 단계(Risk Analyzer 등)가 파싱하기 훨씬 쉬워집니다.

```bash
pip install cyclonedx-bom
cyclonedx-py requirements requirements.txt -o sbom.json   # CycloneDX 포맷
```

또는 Syft를 서브프로세스로 호출해도 됩니다 (컨테이너·다국어 프로젝트까지 지원):
```bash
syft <프로젝트 경로> -o cyclonedx-json > sbom.json
```

원문 → [`16_cyclonedx_python_github.md`](raw/16_cyclonedx_python_github.md) · [`11_jit_syft_grype_guide.md`](raw/11_jit_syft_grype_guide.md)

### 5-4. 전체 파이프라인 한눈에 보기

```
[AI 에이전트 저장소]
      │
      ├─▶ ① 매니페스트 파싱 (requirements-parser/dparse) ──┐
      └─▶ ② 실제 임포트 스캔 (pipreqs, --diff로 보완)       ├─▶ 의존성 목록 확정
                                                            │
                                                            ▼
                                            ③ PyPI JSON API 호출 (버전·해시·취약점)
                                                            │
                                                            ▼
                                            ④ SBOM 생성 (cyclonedx-py / Syft)
                                                            │
                                                            ▼
                                        [Risk Analyzer / ML 이상탐지로 전달]
```

---

## 6. MCP(Model Context Protocol) — Collector가 탐지해야 할 대상

AI 에이전트가 외부 도구에 연결되는 표준 방식이 MCP입니다. Dependency Collector는 이 MCP 서버 연동도 "외부 연동 도구"로 함께 수집해야 합니다.

- 구조: **Host**(LLM 앱) → **Client** → **Server**(도구·데이터 제공), JSON-RPC 2.0 기반
- LangChain은 `langchain-mcp-adapters`(`pip install "langchain[mcp]"`)로 MCP 서버를 툴 소스처럼 다룸
- 3단계 통합: ①LangChain 내장 툴 ②HTTP/SSE로 붙는 원격 MCP 서버 ③로컬 프로세스로 도는 MCP 서버 — 이 중 ②③이 Collector가 자동 탐지해야 할 대상
- 초기 MCP(2024말)는 인증 표준이 없어 보안 문제가 있었으나 이후 OAuth 2.0(동적 클라이언트 등록, 자동 엔드포인트 탐색) 도입으로 개선 중 — "표준화된 지 얼마 안 된 프로토콜이라 보안 관행이 아직 성숙하지 않았다"는 점 자체가 우리 프로젝트의 문제의식과 정확히 맞닿음

원문 → [`08_stytch_mcp_intro.md`](raw/08_stytch_mcp_intro.md) · [`09_langchain_mcp_docs.md`](raw/09_langchain_mcp_docs.md)

---

## 7. 직접 해보기 (Hands-on)

읽기만 하지 말고 터미널에 쳐보세요. 5분이면 됩니다.

```bash
# 1. 아무 패키지의 PyPI 메타데이터 직접 조회 (브라우저로 열어도 됨)
curl -s https://pypi.org/pypi/requests/json | python3 -m json.tool | head -50

# 2. 특정 버전의 알려진 취약점 조회
curl -s -X POST https://api.osv.dev/v1/query \
  -H "Content-Type: application/json" \
  -d '{"package": {"name": "requests", "ecosystem": "PyPI"}, "version": "2.6.0"}' | python3 -m json.tool

# 3. pipreqs로 아무 파이썬 프로젝트 폴더의 실제 의존성 뽑아보기
pip install pipreqs
pipreqs --print /path/to/some/project

# 4. cyclonedx-bom으로 SBOM 만들어보기
pip install cyclonedx-bom
cyclonedx-py requirements requirements.txt -o sbom.json
cat sbom.json | python3 -m json.tool | less
```

---

## 8. 자주 헷갈리는 것 (FAQ)

**Q. SBOM이랑 requirements.txt랑 뭐가 다른가요?**
requirements.txt는 "설치할 목록"(사람이 직접 관리), SBOM은 "실제로 뭐가 들어있는지 기계가 읽을 수 있게 표준화한 명세서"(도구가 생성, 해시·라이선스·취약점 정보까지 포함). SBOM이 requirements.txt를 포함하는 상위 개념이라고 보면 됩니다.

**Q. SCA, SBOM, ASM(우리 프로젝트) 관계가 뭔가요?**
SBOM(부품 목록 만들기) → SCA(그 목록에서 알려진 문제 찾기) → 우리 프로젝트(ASM)는 여기에 "그 문제가 AI 에이전트의 실제 권한과 연결되는가"라는 한 단계를 더 얹는 것입니다.

**Q. 왜 requirements.txt 파싱이랑 pipreqs 임포트 스캔을 둘 다 해야 하나요?**
requirements.txt는 사람이 쓴 것이라 실제 코드와 다를 수 있습니다(누락, 오래된 버전 명시 등). 두 결과를 비교(`pipreqs --diff`)하면 "선언은 안 됐지만 실제로 쓰이는" 숨은 의존성까지 잡아낼 수 있습니다 — 이게 우리 팀이 자산을 "빠짐없이" 식별해야 하는 이유입니다.

**Q. xz-utils 사례는 자동화 도구로 막을 수 있었나요?**
못 막았습니다. 코드 자체는 GitHub에 없고 배포 버전에만 있었고, 정상적으로 신뢰를 쌓은 메인테이너가 심은 것이라 자동 스캐너의 패턴 탐지로는 걸러지지 않았습니다. 이게 "규칙 기반 탐지의 한계"이고, 우리 팀이 ML 이상탐지를 추가하는 이유와 연결됩니다(다만 ML도 이런 극단적 사례까지 잡는다고 보장할 순 없다는 점은 솔직히 인지해야 함).

---

## 📎 원문 전체 목록

| 번호 | 파일 | 원문 |
|---|---|---|
| 01 | [`raw/01_socket_ai_agents_supply_chain.md`](raw/01_socket_ai_agents_supply_chain.md) | Socket — AI Agents Supply Chain Attack Surface |
| 02 | [`raw/02_esecurityplanet_ai_threats_2026.md`](raw/02_esecurityplanet_ai_threats_2026.md) | eSecurityPlanet — AI Software Supply Chain Threats 2026 (JFrog 리포트) |
| 03 | [`raw/03_fossa_sbom_examples.md`](raw/03_fossa_sbom_examples.md) | FOSSA — SBOM Examples, Explained |
| 04 | [`raw/04_appsecsanta_snyk_vs_dependabot.md`](raw/04_appsecsanta_snyk_vs_dependabot.md) | AppSec Santa — Snyk vs Dependabot |
| 05 | [`raw/05_wiz_attack_path_analysis.md`](raw/05_wiz_attack_path_analysis.md) | Wiz — What is Attack Path Analysis |
| 06 | [`raw/06_jfrog_typosquatting.md`](raw/06_jfrog_typosquatting.md) | JFrog — Typosquatting in the Software Supply Chain |
| 07 | [`raw/07_checkmarx_colorama.md`](raw/07_checkmarx_colorama.md) | Checkmarx — PyPI Colorama/Colorizr Attack |
| 08 | [`raw/08_stytch_mcp_intro.md`](raw/08_stytch_mcp_intro.md) | Stytch — MCP Comprehensive Introduction |
| 09 | [`raw/09_langchain_mcp_docs.md`](raw/09_langchain_mcp_docs.md) | LangChain Docs — MCP Integration |
| 10 | [`raw/10_pypi_requirements_parser.md`](raw/10_pypi_requirements_parser.md) | PyPI — requirements-parser |
| 11 | [`raw/11_jit_syft_grype_guide.md`](raw/11_jit_syft_grype_guide.md) | Jit — Syft & Grype SBOM Guide |
| 12 | [`raw/12_dev_dependency_scanner_python.md`](raw/12_dev_dependency_scanner_python.md) | DEV Community — Build a Dependency Vulnerability Scanner |
| 13 | [`raw/13_datadog_xz_utils_backdoor.md`](raw/13_datadog_xz_utils_backdoor.md) | Datadog Security Labs — XZ Utils Backdoor (CVE-2024-3094) |
| 14 | [`raw/14_pipreqs_github.md`](raw/14_pipreqs_github.md) | GitHub — pipreqs |
| 15 | [`raw/15_pypi_json_api_docs.md`](raw/15_pypi_json_api_docs.md) | PyPI 공식 문서 — JSON API |
| 16 | [`raw/16_cyclonedx_python_github.md`](raw/16_cyclonedx_python_github.md) | GitHub — cyclonedx-python |
| 17 | [`raw/17_osv_api_query_endpoint.md`](raw/17_osv_api_query_endpoint.md) | OSV 공식 문서 — POST /v1/query |

## 🖼️ 직접 보면 좋은 다이어그램 (텍스트로 옮기기 어려운 것)

- MCP 구조도: https://stytch.com/blog/model-context-protocol-introduction/
- 공급망 공격 흐름도: https://socket.dev/blog/ai-agents-supply-chain-attack-surface
- 클라우드 공격경로 그래프 예시: https://www.wiz.io/academy/detection-and-response/attack-path-analysis
- SBOM 구조 예시: https://fossa.com/blog/sbom-examples-explained/
