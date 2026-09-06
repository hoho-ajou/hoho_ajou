# 교차 검토 — 모듈 간 미해결 질문 (1차 설계 라운드에서 수집)

각 담당자는 자기 앞으로 온 질문에 답하고, 자기 설계/에픽 문서에 "## 확정 사항 (교차검토 반영)" 섹션을 추가해서 최종 스키마 필드를 확정하세요.

## → Collector 담당자에게

**From Risk Analyzer:**
1. `package.vulnerabilities[]`에 CVE ID뿐 아니라 `cvss_base_score`를 직접 넣어줄 수 있나요? (재조회 안 해도 되게)
2. `external_integrations[]` (패키지가 shell/network/MCP 접근을 쓰는지) 필드를 스키마에 넣을 계획이 있나요? Risk Analyzer의 permission_weight 계산에 필수입니다.
3. `latest_release_date`, `maintainer_count`가 모든 패키지에 대해 항상 존재를 보장하나요? (staleness score 계산용)

**From ML 이상탐지:**
4. SBOM에 배포 파일(sdist/wheel) 자체 경로나 해시가 포함되나요, 메타데이터만인가요? (정적 코드 분석 feature용)
5. maintainer의 PyPI 계정 생성일 등 계정 정보까지 수집 범위인가요?

## → Risk Analyzer 담당자에게

**From Attack Path Engine:**
6. 에이전트별 "권한(Permission)" 목록(권한 타입, 대상 자산)을 Risk Analyzer가 제공하나요, 아니면 이 정보 자체가 스키마 어디에도 없는데 누가 만들어야 하나요? (현재 미해결 — 팀 전체가 결정해야 함)
7. `is_externally_reachable`(외부 노출 여부)을 Risk Analyzer가 계산해서 주나요, Attack Path Engine이 직접 판단해야 하나요?

**From Attack Path Engine (스키마 관련, 답변 필요):**
8. `signals` 서브 오브젝트(cvss_norm, epss_score, typo_flag, staleness_score)면 그래프 노드 속성으로 충분한가요, 원본 CVE 목록도 필요한가요?
9. `risk_level`(LOW/MEDIUM/HIGH)로 충분한가요, 숫자 `risk_score`도 필요한가요?

## → ML 이상탐지 담당자에게

**From Attack Path Engine:**
10. `triggered_features` 구조(feature명+importance)가 그래프 구축에 바로 쓸 수 있는 형태인가요, 다른 표현이 필요한가요?
11. `confidence_score`를 Risk Analyzer의 위험 점수와 어떻게 결합할 계획인가요(가중합/별도 노드 등)?

## → Attack Path Engine 담당자에게 (가장 많은 질문이 몰림 — 우선 처리)

**From Risk Analyzer & ML 둘 다 → Attack Path Engine으로 넘어온 질문 6, 7 관련:**
"권한(Permission)" 데이터 출처가 현재 스키마 어디에도 없습니다. 팀 결정 필요: (a) Collector가 에이전트 코드에서 권한 사용 패턴을 추가로 스캔해서 제공, (b) Risk Analyzer가 별도로 정의, (c) Attack Path Engine이 직접 정의하고 나머지는 참조만. **이 문서에서 하나를 선택하고 이유를 적어주세요.**

**From Dashboard:**
12. `risk_score`(0-100)가 모든 노드에, `overall_risk_score`가 모든 경로에 사전 계산되어 붙어있나요? (Dashboard는 재계산 안 한다고 가정 중)
13. 각 노드에 사람이 읽을 수 있는 `label`, 각 경로에 한 줄 `description`, 타입별 `attributes`(CVE 목록/패키지버전/권한·에이전트명/ML 이상점수)를 넣어줄 수 있나요?
14. `node_sequence`/`edge_sequence`가 같은 파일의 `nodes[].id`/`edges[].id`를 항상 유효하게 참조하나요? (참조 무결성 보장)

**Attack Path Engine이 Dashboard에게 남긴 질문:**
15. nodes/edges/paths 구조가 맞나요, Cytoscape.js 전용 `elements: {nodes, edges}` 포맷을 원하나요?

## → Dashboard 담당자에게

**From Attack Path Engine:** 질문 15 답변 필요.

## → 총괄(PM)이 팀 차원에서 정리해야 할 것

- `schemas/`의 공통 메타 필드(`run_id`, `schema_version`)를 4개 스키마 전부에 강제할지 여부
- `pipeline/` 오케스트레이션 코드를 누가 소유·유지보수할지
- 중간 산출물(`data/`)을 로컬에만 둘지 AWS S3에 올릴지 (M3 이전 결정 필요)
- **권한(Permission) 데이터의 출처** — 질문 6/11 관련, Attack Path Engine 담당자의 결정을 최종 승인
