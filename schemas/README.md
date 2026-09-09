# 모듈 간 데이터 계약 — 현재 상태: DRAFT

이 4개 스키마는 **초기 뼈대로 준비된 초안**이며, 실제 팀 교차검토를 거쳐 확정된 것이 아닙니다. 각 모듈 담당자가 설계를 진행하며 그대로 써도 되고, 인접 모듈과 실제로 맞춰보면서 다르게 바꿔도 됩니다.

바뀐 내용은 관련 담당자(CODEOWNERS, `docs/governance/OWNERSHIP.md` 참고)와 실제로 맞춰본 뒤, `docs/review/decisions/0X-*.md`에 왜 그렇게 바꿨는지 남기세요.

| 파일 | 담당 |
|---|---|
| `collector_output.schema.json` | Dependency Collector 담당 작성, Risk Analyzer·ML 담당 확인 |
| `risk_score.schema.json` | Risk Analyzer 담당 작성, Attack Path Engine 담당 확인 |
| `ml_result.schema.json` | ML 담당 작성, Attack Path Engine 담당 확인 |
| `attack_graph.schema.json` | Attack Path Engine 담당 작성, Dashboard 담당 확인 |
