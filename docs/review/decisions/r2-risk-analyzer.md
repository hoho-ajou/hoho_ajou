# 결정 기록 — Risk Analyzer 설계

## 담당 역할

R2 (Risk Analyzer) — 자세한 목표/범위는 [`docs/governance/OWNERSHIP.md`](../../governance/OWNERSHIP.md) 참고

## 하위 이슈 분할

(하위 이슈 생성 전 — 담당자가 생성 후 채움)

## 결정 사항

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

## 근거 문서

`docs/design/02-risk-analyzer.md` "확정 사항 (교차검토 반영)" Q6~Q9
