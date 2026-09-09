# 결정 기록 — ML 이상탐지 설계

## 담당 역할

R3 (ML 이상탐지) — 자세한 목표/범위는 [`docs/governance/OWNERSHIP.md`](../../governance/OWNERSHIP.md) 참고

## 하위 이슈 분할

(하위 이슈 생성 전 — 담당자가 생성 후 채움)

## 결정 사항

### 결정 1 — `triggered_features` 구조는 그대로 그래프 노드 속성으로 사용

**결정하려 했던 것**: `{ feature, value, importance }` 배열 형태가 Attack Path Engine의 그래프 구축에 바로 쓸 수 있는지, 재구성이 필요한지.

**근거**: 현재 구조로도 노드 속성 매핑에 문제 없음. 다만 그래프 렌더링·Dashboard 표시 편의를 위한 제약이 필요함.

**최종 결정**: 재구성 불필요. 단 (1) `importance` 내림차순 정렬 상태로 출력, (2) 노드 속성 과다 방지를 위해 상위 5개로 cap, (3) 필드명은 `feature`(string)/`value`(any)/`importance`(0~1 float) 유지. Attack Path Engine은 이 배열을 `attributes.ml_triggered_features`로 그대로 매핑.

### 결정 2 — `confidence_score`와 Risk Analyzer `risk_score`는 사전 결합하지 않음

**결정하려 했던 것**: ML의 `confidence_score`와 Risk Analyzer의 `risk_score`를 ML/Risk Analyzer 단계에서 미리 가중합할지.

**근거**: 두 신호는 탐지 근거가 다름(ML=행동·통계적 이상, Risk Analyzer=알려진 취약점/타이포스쿼팅). 상류에서 미리 합치면 그래프 구축 시점에 각 신호를 따로 확인·재조정할 수 없게 됨.

**최종 결정**: 같은 노드 위의 독립된 두 속성으로 유지. 결합·가중치 부여는 Attack Path Engine의 경로 스코어링 공식에서 처리 (`node_weight = w1 * risk_score + w2 * (confidence_score * 100)`, w1/w2는 Attack Path Engine이 튜닝). `is_flagged`(bool)도 별도 필드로 유지해 임계값 기반 필터링에 사용 가능하게 함.

## 근거 문서

`docs/design/03-ml-detector.md` "확정 사항 (교차검토 반영)" Q10~Q11
