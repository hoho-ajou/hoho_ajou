# 결정 기록 (Decision Records)

Epic과 R1~R4 전체를 통틀어 확정된 결정을 이 파일 하나에 시간순으로 이어붙입니다. 오간 논의 전부가 아니라 **최종 결정과 그 근거만** 남깁니다. 새 결정이 생기면 해당 역할 섹션 아래에 "### 결정 N"을 추가합니다 — 새 파일을 만들지 않습니다.

역할별 담당자는 [`docs/governance/OWNERSHIP.md`](../governance/OWNERSHIP.md) 참고.

---

## Epic — 전체 오케스트레이션

상위 이슈: [#1](https://github.com/hoho-ajou/hoho_ajou/issues/1)

### 결정 1 — 오케스트레이션 방식: 파일 기반 핸드오프 + 얇은 CLI

**결정하려 했던 것**: 모듈 간 통신을 공유 DB/메시지 큐로 할지, 파일 기반으로 할지.

**근거**: 4인 학부 프로젝트 규모에서 DB/큐 인프라는 과설계. Collector→(Risk Analyzer, ML 병렬)→Attack Path→Dashboard는 선형+한 번의 fan-out/fan-in 구조뿐이라 파일 핸드오프로 충분하며, 각 모듈이 독립 실행 가능해야 한다(담당자가 자기 모듈만 테스트할 때 다른 모듈이 안 떠 있어도 됨).

**최종 결정**: `schemas/`로 형식이 고정된 JSON 파일을 로컬 디스크에 순서대로 쌓고, 이를 순서대로 호출하는 얇은 Python CLI(`pipeline/run.py`)를 둔다. 모듈 간 데이터는 `data/<run_id>/*.json` 형태로 저장.

**(참고)** 이 CLI가 실제로 서브프로세스 호출인지 함수 호출인지는 아직 미정 — 총괄이 구현 착수 전 결정.

### 결정 2 — 분석 대상 확정: PyPI 생태계 + LangChain(+MCP) 에이전트

**결정하려 했던 것**: 어떤 패키지 레지스트리, 어떤 AI 에이전트 프레임워크를 분석 대상으로 삼을지. (팀 계획서 §4 "대상 범위 확정(PyPI+에이전트 1종)"의 실제 내용)

**전제**: 에이전트 프레임워크마다 도구 선언 방식·설정파일 구조가 전부 달라 범용 탐지기를 만들기 어렵다. 4인 학부 프로젝트 규모에서는 하나로 고정해야 한다.

**레지스트리(PyPI vs npm) 근거**: AI 에이전트 프레임워크 대부분(7개 중 6개)이 Python 기반, "Mini Shai-Hulud" 웜(2026년 5월)이 PyPI의 `mistralai`, `guardrails-ai`를 감염시켜 PyPI가 격리 조치한 실제 사례[^1], PyPI JSON API+OSV 데이터 접근성, ML 학습용 악성 샘플(`pypi_malregistry`) 확보, Python 3.11+ 스택 정합성. 공격 사례 총량은 npm이 크지만 나머지 기준이 전부 PyPI를 가리킨다.

**프레임워크(LangChain vs 후보 6종: LlamaIndex/CrewAI/AutoGen/Semantic Kernel/OpenHands/Haystack) 근거**: 범용성(도구+메모리+에이전트, 후보들은 RAG/멀티에이전트/코딩 전용으로 특화), MCP 공식 지원(`langchain-mcp-adapters`, `langchain[mcp]` extra — PyPI 확인), GitHub 스타 수(146,273 — 2위 OpenHands 87,828). MCP 채택 비율 자체는 LangChain(5.0%)이 CrewAI(13.3%)·AutoGen(14.4%)보다 낮지만, 절대 저장소 수(1,275개, 2위의 4배)가 표본 확보(목표 5종+)에는 더 중요한 기준이다.

**최종 결정**: 분석 대상을 **PyPI 패키지 생태계 + LangChain(+MCP) 기반 AI 에이전트**로 확정. 그 외는 확장 과제로 남긴다.

**대상의 정의**: 분석 대상은 "AI로 만든 저장소"가 아니라 "LangChain을 import해 AI 에이전트를 구현한 저장소"다.

---

## R1 — Dependency Collector

상위 이슈: [#9](https://github.com/hoho-ajou/hoho_ajou/issues/9) · 담당: 배승원

### 결정 1 — 취약점 CVSS 점수를 Collector 단계에서 미리 채워 넣음

**결정하려 했던 것**: `vulnerabilities[]`에 CVE ID만 넣을지, `cvss_base_score`까지 인라인으로 넣을지 (Risk Analyzer가 재조회하지 않아도 되게).

**근거**: Risk Analyzer가 매 패키지마다 CVSS를 다시 조회하면 API 호출이 중복되고 느려짐.

**최종 결정**: OSV 응답의 `severity`(CVSS 벡터)를 Collector가 파싱해 `cvss_base_score`(숫자) + `cvss_source`(`nvd`/`osv`)로 `vulnerabilities[]`에 직접 포함. 파싱 불가 시 `cvss_base_score: null`.

### 결정 2 — 패키지 단위 `external_integrations[]` 필드 추가

**결정하려 했던 것**: 패키지가 shell/network/MCP 접근을 쓰는지 여부를 Risk Analyzer의 `permission_weight` 계산에 넘길 방법.

**근거**: Risk Analyzer가 권한 가중치를 계산하려면 패키지 단위로 연동 컨텍스트가 필요함.

**최종 결정**: 5단계 외부 연동 탐지 결과를 패키지 단위로도 태깅해 `dependencies[].external_integrations: ["network"|"shell"|"mcp"|"filesystem"]` 배열 추가 (top-level `integrations[]`는 별도 유지).

### 결정 3 — `latest_release_date`/`maintainer_count` 결측 처리

**결정하려 했던 것**: staleness score 계산에 쓰이는 이 필드들이 모든 패키지에 항상 존재함을 보장할 수 있는지.

**근거**: PyPI가 일부 패키지에 이 정보를 제공하지 않아 완전 보장은 불가능함.

**최종 결정**: 필드를 항상 present로 두되 값이 없으면 `null` + `data_status: "not_available"`로 명시해 Risk Analyzer가 결측을 구분할 수 있게 함.

### 결정 4 — 배포 파일 경로/해시 포함 (ML 요청)

**결정하려 했던 것**: SBOM에 배포 파일(sdist/wheel) 자체 경로·해시를 포함할지, 메타데이터만 넣을지.

**근거**: ML 이상탐지의 정적 코드 분석 feature 추출에 실제 파일 매칭이 필요함.

**최종 결정**: `distribution_files[]`에 파일명, 다운로드 URL, sha256 해시를 포함.

### 결정 5 — maintainer 계정 생성일은 기본 미수집

**결정하려 했던 것**: ML이 요청한 메인테이너 PyPI 계정 생성일까지 수집 범위에 넣을지.

**근거**: PyPI JSON API가 계정 생성일을 제공하지 않아 별도 유저 페이지 스크래핑이 필요하고 요청량이 커짐.

**최종 결정**: 기본 미수집. 대신 `maintainer_accounts[].account_created_at`을 `null` + `data_status: "not_collected"`로 스키마에 예약해두어, 추후 필요성이 확정되면 별도 수집기를 붙일 수 있게 함.

**근거 문서**: `docs/architecture_v1/05-collector.md` "확정 사항 (교차검토 반영)"

---

## R2 — Risk Analyzer

상위 이슈: [#10](https://github.com/hoho-ajou/hoho_ajou/issues/10) · 담당: 유다호

### 결정 1 — 에이전트 권한(Permission) 데이터는 Risk Analyzer가 만들지 않음

**결정하려 했던 것**: `permission_weight` 계산에 필요한 권한 등급(LOW/MEDIUM/HIGH)의 원 출처를 Risk Analyzer가 직접 정의할지.

**근거**: Risk Analyzer는 권한 등급을 **입력**으로 쓰는 소비자일 뿐, 권한 목록(타입+대상 자산)의 원 출처가 아님. Attack Path Engine이 그래프 엣지를 만들기 위해 이 데이터를 어차피 구조화해야 하므로 그쪽이 스키마를 소유하는 게 이중 정의를 막음.

**최종 결정**: Attack Path Engine이 정의·소유, Risk Analyzer는 참조(consume)만. `permission_source` 필드로 출처를 명시.

### 결정 2 — `is_externally_reachable`은 Risk Analyzer가 계산하지 않음

**결정하려 했던 것**: 외부 노출 여부를 Risk Analyzer가 패키지 단위로 계산해서 넘길지.

**근거**: 이 값은 그래프 위상(다른 노드와의 연결 관계)에 의존하는데, Risk Analyzer는 패키지 단위 정적 신호만 다루고 그래프 전체 구조를 보지 않음. 억지로 계산하면 그래프 구축 시점의 실제 연결 정보와 어긋날 위험이 있음.

**최종 결정**: Attack Path Engine이 직접 판단.

### 결정 3 — `signals` 서브 오브젝트와 원본 CVE 목록을 둘 다 포함

**결정하려 했던 것**: 그래프 노드 속성으로 정규화된 신호(`cvss_norm`)만 주면 충분한지, 원본 CVE ID 목록도 필요한지.

**근거**: `cvss_norm`만으로는 Dashboard가 요구하는 "CVE 목록" 상세정보 속성을 만들 수 없음.

**최종 결정**: `signals.cve_ids[]`를 추가. 그래프 노드에는 `cvss_norm`(정렬/색상용)과 `cve_ids`(사람이 읽는 상세정보용)를 함께 붙임.

### 결정 4 — `risk_level`과 `risk_score`를 둘 다 유지

**결정하려 했던 것**: 등급(LOW/MEDIUM/HIGH)만 주면 충분한지, 숫자 점수도 따로 필요한지.

**근거**: 정렬·임계값 비교(숫자)와 시각화·룰 분기(등급)의 용도가 다름.

**최종 결정**: 기존 설계 그대로 둘 다 유지. 각 필드의 용도만 문서에 명시적으로 추가.

**근거 문서**: `docs/architecture_v1/06-risk-analyzer.md` "확정 사항 (교차검토 반영)" Q6~Q9

---

## R3 — ML 이상탐지

상위 이슈: [#11](https://github.com/hoho-ajou/hoho_ajou/issues/11) · 담당: 제유호

### 결정 1 — `triggered_features` 구조는 그대로 그래프 노드 속성으로 사용

**결정하려 했던 것**: `{ feature, value, importance }` 배열 형태가 Attack Path Engine의 그래프 구축에 바로 쓸 수 있는지, 재구성이 필요한지.

**근거**: 현재 구조로도 노드 속성 매핑에 문제 없음. 다만 그래프 렌더링·Dashboard 표시 편의를 위한 제약이 필요함.

**최종 결정**: 재구성 불필요. 단 (1) `importance` 내림차순 정렬 상태로 출력, (2) 노드 속성 과다 방지를 위해 상위 5개로 cap, (3) 필드명은 `feature`(string)/`value`(any)/`importance`(0~1 float) 유지. Attack Path Engine은 이 배열을 `attributes.ml_triggered_features`로 그대로 매핑.

### 결정 2 — `confidence_score`와 Risk Analyzer `risk_score`는 사전 결합하지 않음

**결정하려 했던 것**: ML의 `confidence_score`와 Risk Analyzer의 `risk_score`를 ML/Risk Analyzer 단계에서 미리 가중합할지.

**근거**: 두 신호는 탐지 근거가 다름(ML=행동·통계적 이상, Risk Analyzer=알려진 취약점/타이포스쿼팅). 상류에서 미리 합치면 그래프 구축 시점에 각 신호를 따로 확인·재조정할 수 없게 됨.

**최종 결정**: 같은 노드 위의 독립된 두 속성으로 유지. 결합·가중치 부여는 Attack Path Engine의 경로 스코어링 공식에서 처리 (`node_weight = w1 * risk_score + w2 * (confidence_score * 100)`, w1/w2는 Attack Path Engine이 튜닝). `is_flagged`(bool)도 별도 필드로 유지해 임계값 기반 필터링에 사용 가능하게 함.

**근거 문서**: `docs/architecture_v1/07-ml-detector.md` "확정 사항 (교차검토 반영)" Q10~Q11

---

## R4 — Attack Path Engine + Dashboard

상위 이슈: [#12](https://github.com/hoho-ajou/hoho_ajou/issues/12) · 담당: 전선재

### 결정 1 — Permission 데이터: Collector가 값 채움, Attack Path Engine이 스키마 소유 (팀 전체 결정, 최중요)

**결정하려 했던 것**: 에이전트별 권한(권한 타입+대상 자산) 목록을 (a) Collector가 스캔해서 제공, (b) Risk Analyzer가 별도 정의, (c) Attack Path Engine이 정의하고 나머지는 참조만 — 셋 중 어느 방식으로 할지.

**근거**: Collector가 에이전트 코드를 정적 스캔하는 유일한 모듈이므로 실제 값은 Collector가 채워야 함. 하지만 Attack Path Engine이 이 데이터를 그래프 노드/엣지로 직접 소비하므로, 스키마(enum·구조)를 그쪽이 소유해야 이후 그래프 빌더 변경 시 마찰이 없음.

**최종 결정**: (a)+(c) 혼합. `agent.permissions[]`의 값은 Collector(R1)가 코드 스캔으로 채우고, 필드의 enum·구조는 Attack Path Engine(R4)이 정의. Risk Analyzer·ML은 참조만.

### 결정 2 — 출력 형식은 범용 nodes/edges/paths, Cytoscape 변환은 Dashboard 프론트엔드 책임

**결정하려 했던 것**: 출력을 Cytoscape.js 전용 `elements: {nodes, edges}` 포맷으로 만들지, 범용 구조로 만들지 — 그리고 그 변환을 누가 할지.

**근거**: 특정 시각화 라이브러리에 종속되지 않아야 UI 라이브러리 교체 시 상류 스키마 변경이 불필요하고, 범용 구조가 스키마 검증·유닛테스트도 더 쉬움. 변환 로직 자체가 몇 줄 수준이라 부담이 적음.

**최종 결정**: `schemas/attack_graph.schema.json`은 `nodes/edges/paths` 범용 구조 유지. Cytoscape 변환은 Dashboard 프론트엔드(`graphView.js`)가 렌더링 시점에 `toCytoscapeElements()`로 수행. (같은 R4 안에서 Attack Path Engine 쪽과 Dashboard 쪽이 이미 합의된 사항이라 별도 조율 불필요.)

### 결정 3 — Risk Analyzer로부터 `vulnerability_ids` 원본도 함께 요청

**결정하려 했던 것**: Risk Analyzer가 이미 주는 `risk_score`/`risk_level`/`signals`로 충분한지.

**근거**: Dashboard 노드 `attributes.cve_ids`를 채우려면 정규화된 signals만으로는 부족함.

**최종 결정**: 기존 설계로 요구사항 충족(risk_score 숫자+risk_level 등급 모두 제공). 추가로 원본 `vulnerability_ids`(CVE 목록)도 함께 요청.

### 결정 4 — ML `triggered_features`는 변환 없이 그대로 사용, `confidence_score`는 경로 스코어링에서 결합

**결정하려 했던 것**: ML 출력 구조를 그대로 쓸 수 있는지, `confidence_score`를 Risk Analyzer 점수와 어떻게 결합할지.

**근거**: `triggered_features` 구조는 이미 그래프 노드 속성 형식에 맞음. `confidence_score`와 `risk_score`는 탐지 근거가 달라 사전 결합하면 정보 손실이 생김.

**최종 결정**: `triggered_features`는 `attributes.ml_anomaly_score` 및 상세 패널용 부가 정보로 바로 사용. `confidence_score`는 별도 노드 없이 가중합으로 결합(`weight = 1 / (risk_score × confidence_score 보정치)`).

### 결정 5 — Dashboard에 사전 계산된 값만 전달 (Dashboard는 재계산 안 함)

**결정하려 했던 것**: `risk_score`/`overall_risk_score`를 Dashboard가 재계산해야 하는지, 사전 계산되어 붙어있는지.

**근거**: Dashboard는 표시 전용 모듈로 설계됨 — 재계산 로직을 프론트엔드에 두면 파이프라인 값과 어긋날 위험.

**최종 결정**: 모든 `Package`/`Agent`/`Permission` 노드에 사전 계산된 `risk_score`(0-100 정규화), 모든 `paths[]`에 `overall_risk_score`를 채워 넘김. 각 노드는 `label`, 타입별 `attributes`도 포함. `export.py`가 `node_sequence`/`edge_sequence`의 참조 무결성을 검증 후 파일을 씀(단위 테스트로 강제).

**근거 문서**: `docs/architecture_v1/08-attack-path.md` "확정 사항 (교차검토 반영)" 1~5, `docs/architecture_v1/09-dashboard.md` §6-1

[^1]: "Mini Shai-Hulud" 공급망 공격, 2026년 5월. [The Hacker News](https://thehackernews.com/2026/05/mini-shai-hulud-compromises.html)
