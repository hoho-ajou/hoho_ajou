# 용어집 (구현자용 — schemas/design 전 모듈 공통)

`study_week1/README.md` §3의 용어집이 "처음 배우는 사람" 대상이라면, 이 문서는 **schemas/*.json과 docs/design/*.md를 그대로 구현할 사람(또는 AI)** 대상입니다. 각 스키마 필드명이 어느 용어에서 왔는지 연결하는 데 씁니다.

## 전체 파이프라인 공통

| 용어 | 정의 |
|---|---|
| **run_id** | 파이프라인 한 번의 전체 실행을 식별하는 ID. Collector가 생성해서 이후 모든 모듈 출력에 그대로 전달됨 |
| **schema_version** | 각 `schemas/*.json` 파일의 버전 문자열. 필드 추가/변경 시 올림 (`CONTRIBUTING.md` §3) |
| **파일 기반 핸드오프** | 모듈 간 통신을 API 호출이 아니라 JSON 파일 쓰기/읽기로 하는 방식(`00-overall.md` §2). 각 모듈은 독립 실행 가능해야 함 |
| **CODEOWNERS 대상 파일** | `schemas/*.json`처럼 변경 시 관련 모듈 담당자 전원의 승인이 강제되는 파일 |

## Dependency Collector

| 용어 | 정의 |
|---|---|
| **SBOM** (Software Bill of Materials) | 소프트웨어를 구성하는 모든 패키지·라이선스·해시의 목록. `collector_output.schema.json`의 `sbom{}` 필드 |
| **CycloneDX** | SBOM을 표현하는 표준 JSON/XML 포맷 (보안 중심). `cyclonedx-py`로 생성 |
| **PURL** (Package URL) | `pkg:pypi/requests@2.31.0` 형태로 패키지를 생태계+이름+버전까지 정확히 식별하는 표준 |
| **OSV** | Google이 운영하는 오픈소스 취약점 DB/API. Collector가 PyPI 메타데이터로 못 채운 취약점을 보완 조회 |
| **resolution_status** | 의존성 하나가 PyPI 조회에 성공(`resolved`)했는지 실패(`unresolved`)했는지. 실패해도 파이프라인은 계속 진행 |
| **MCP** (Model Context Protocol) | LLM이 외부 도구/데이터에 접근하는 표준 프로토콜(JSON-RPC 2.0, Host→Client→Server). Collector가 코드/설정 파일에서 탐지해야 할 "외부 연동" 유형 중 하나 |
| **agent.permissions[]** | 에이전트 코드가 실제로 행사하는 권한(타입+대상 자산). **Collector가 정적 스캔으로 값을 채우지만, 필드의 enum·구조는 Attack Path Engine이 소유**(`04-attack-path.md` 확정 사항 1번) |

## Risk Analyzer

| 용어 | 정의 |
|---|---|
| **CVSS** (Common Vulnerability Scoring System) | 취약점 심각도 0~10 점수. `signals.cvss_norm`은 이를 0~1로 정규화한 값 |
| **EPSS** (Exploit Prediction Scoring System) | 어떤 취약점이 실제로 악용될 확률(0~1)을 예측하는 지표. CVSS(심각도)와 달리 "실제 악용 가능성"을 봄 |
| **타이포스쿼팅 (typosquatting)** | 인기 패키지와 이름이 비슷한 가짜 패키지(예: `requests`→`requets`)로 오설치를 유도하는 공격. `typo_flag`/`typo_nearest_match`는 Levenshtein 거리로 탐지 |
| **staleness_score** | 패키지가 얼마나 방치됐는지(마지막 릴리스 이후 경과 개월 수 기반) 나타내는 0~1 값. 유지보수 중단 패키지의 위험도를 가중 |
| **permission_weight** | 에이전트가 가진 권한의 위험도에 따른 가중치(1.0~3.0). Attack Path Engine이 정의한 `agent.permissions[]`를 참조해 계산 |
| **risk_score / risk_level** | 각 패키지의 최종 위험도 — 숫자(`risk_score`)와 3단계 등급(`LOW`/`MEDIUM`/`HIGH`, `risk_level`) 둘 다 제공 |

## ML 이상탐지

| 용어 | 정의 |
|---|---|
| **Random Forest** | 다수의 결정 트리를 앙상블해 분류하는 지도학습 모델. 기존에 알려진 악성 패턴 학습용 |
| **Isolation Forest** | 정상 데이터의 "다수 패턴"에서 벗어난 이상치를 탐지하는 비지도학습 모델. 신규/변종 악성 패키지 탐지용 |
| **triggered_features** | 모델이 이 패키지를 악성으로 판단하는 데 기여한 feature와 중요도 상위 5개 목록. 그대로 Dashboard 상세 패널에 사용 가능(`04-attack-path.md` 확정 사항 4번) |
| **confidence_score** | ML 모델의 판단 확신도(0~1). Attack Path Engine이 `risk_score`와 가중합으로 결합 |

## Attack Path Engine

| 용어 | 정의 |
|---|---|
| **NetworkX** | Python 그래프 라이브러리. Neo4j 대신 채택(외부 DB 불필요, 소규모 그래프에 충분) |
| **betweenness_centrality** | 그래프에서 한 노드가 다른 노드 간 최단 경로에 얼마나 자주 등장하는지 나타내는 지표. 핵심 자산/병목 식별에 사용 |
| **Yen's algorithm / shortest_simple_paths** | 두 노드 사이의 최단 경로뿐 아니라 상위 k개 경로까지 순서대로 찾는 알고리즘. 공격 경로 후보를 여러 개 뽑을 때 사용 |
| **CNAPP** | 클라우드 자산·권한·네트워크를 그래프로 연결해 공격 경로를 찾는 방법론. BloodHound의 `shortestPath()` 개념을 참고했지만 직접 의존하지는 않음 |
| **node_sequence / edge_sequence** | `paths[]` 안에서 경로를 구성하는 노드/엣지 id의 순서 목록. `nodes[]`/`edges[]`의 실제 id를 참조해야 함(참조 무결성, export 시 단위 테스트로 강제) |

## Dashboard

| 용어 | 정의 |
|---|---|
| **Cytoscape.js** | 그래프 시각화 JS 라이브러리(vis-network/Sigma.js 대신 채택). `elements:{nodes,edges}` 포맷은 프론트엔드가 로드 시 변환 — `attack_graph.schema.json` 자체는 이 포맷을 따르지 않음 |
| **FastAPI** | Dashboard의 얇은 백엔드 프레임워크. 정적 JSON 서빙 + 최소 API만 담당 |

## Git/이슈 운영

| 용어 | 정의 |
|---|---|
| **Conventional Commits** | `<type>(<module>): <설명>` 형식의 커밋 메시지 규칙. `docs/contracts/pr_schema.md` 참고 |
| **CODEOWNERS** | 특정 경로 변경 시 자동으로 리뷰어를 지정하는 GitHub 기능. 현재 `.github/CODEOWNERS`는 역할명 placeholder 상태 |
| **Epic / 하위 이슈** | Epic은 모듈 단위 큰 목표(`docs/epics/`), 하위 이슈는 그 안의 실행 단위 작업. 스키마는 `docs/contracts/epic_schema.md`, `docs/contracts/subissue_schema.md` |

## 초보자용 배경 설명이 필요하면

용어의 배경(왜 중요한지, 실제 공격 사례 등)은 `study_week1/README.md` §1~3, `study_week1/architecture.html`을 참고하세요. 이 문서는 "정의"만, 그쪽은 "왜/사례"까지 다룹니다.
