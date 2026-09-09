# 결정 기록 (Decision Records)

> ⚠️ **시뮬레이션 초안**: 지금 각 파일에 있는 내용은 실제 팀 교차검토가 아니라 여러 모듈 관점을 미리 가정해서 만든 초안입니다. 실제 담당자가 설계하고 인접 모듈과 맞춰본 뒤 다르게 결론 나면 그 파일을 실제 내용으로 갱신/대체하세요.

Epic 하나(전체 조율)와 역할(R1~R4) 하나당 결정 기록 파일 하나입니다. 형식은 [`docs/contracts/decision_record_schema.md`](../../contracts/decision_record_schema.md)를 따릅니다.

담당자는 머지/종료하기 전에 자기 파일을 채웁니다 — 오간 모든 논의가 아니라 **최종 결정과 그 근거만** 남깁니다.

| 파일 | 담당 | 결정 개수 |
|---|---|---|
| [00-overall.md](00-overall.md) | Epic [#1](https://github.com/hoho-ajou/hoho_ajou/issues/1) 전체 오케스트레이션 (총괄) | 1 |
| [r1-collector.md](r1-collector.md) | R1 Dependency Collector | 5 |
| [r2-risk-analyzer.md](r2-risk-analyzer.md) | R2 Risk Analyzer | 4 |
| [r3-ml-detector.md](r3-ml-detector.md) | R3 ML 이상탐지 | 2 |
| [r4-attack-path-dashboard.md](r4-attack-path-dashboard.md) | R4 Attack Path Engine + Dashboard | 5 |

역할별 담당자는 [`docs/governance/OWNERSHIP.md`](../../governance/OWNERSHIP.md) 참고.

## 새 결정을 추가할 때

담당 파일에 "결정 N" 블록을 추가합니다. 새 파일을 만들지 않습니다 — 결정 기록은 항상 Epic 1개 + 역할(R1~R4) 4개, 총 5개로 고정입니다.
