# 결정 기록 — Attack Path Engine + Dashboard 설계

## 담당 역할

R4 (Attack Path Engine, Dashboard) — 자세한 목표/범위는 [`docs/governance/OWNERSHIP.md`](../../governance/OWNERSHIP.md) 참고

## 하위 이슈 분할

(하위 이슈 생성 전 — 담당자가 생성 후 채움)

## 결정 사항

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

## 근거 문서

`docs/design/04-attack-path.md` "확정 사항 (교차검토 반영)" 1~5, `docs/design/05-dashboard.md` §6-1
