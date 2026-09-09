# AASM 설계 문서 입구

전체 흐름과 각 모듈의 기술 설계입니다. 지금은 **설계 검토 단계**이며 실행 코드는 없습니다.

## 읽는 순서

1. [`00-overall.md`](00-overall.md) — 전체 파이프라인 오케스트레이션, 프로젝트 공통 컨벤션
2. [`architecture_diagram.md`](architecture_diagram.md) — 위 내용을 그림(Mermaid)으로 훑기
3. 자기 담당 모듈 문서 (`01-collector.md` ~ `05-dashboard.md`)
4. [`../contracts/sample_dataset.md`](../contracts/sample_dataset.md), [`../contracts/interface_map.md`](../contracts/interface_map.md) — 모듈 간 실제 연결

## 모듈별 문서

| 문서 | 모듈 | 담당 역할 |
|---|---|---|
| [`01-collector.md`](01-collector.md) | Dependency Collector | R1 |
| [`02-risk-analyzer.md`](02-risk-analyzer.md) | Risk Analyzer | R2 |
| [`03-ml-detector.md`](03-ml-detector.md) | ML 이상탐지 | R3 |
| [`04-attack-path.md`](04-attack-path.md) | Attack Path Engine | R4 |
| [`05-dashboard.md`](05-dashboard.md) | Dashboard | R4 |

역할별 담당자·목표·범위는 [`../governance/OWNERSHIP.md`](../governance/OWNERSHIP.md) 참고. 각 문서 안의 "확정 사항" 절이 실제 근거이며, 그중 확정된 결정은 [`../review/decisions/`](../review/decisions/README.md)에 별도 정리되어 있습니다.

## 완료 기준

각 모듈 문서가 "완료"로 인정되려면 [`../governance/REVIEW_CHECKLIST.md`](../governance/REVIEW_CHECKLIST.md)를 통과해야 합니다.
