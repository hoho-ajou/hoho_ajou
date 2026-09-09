# [R2] Risk Analyzer 설계

## 상위 이슈
Part of #1

## 목표

R1의 출력을 입력받아, 패키지별 위험도를 점수화해 R4에 넘기는 로직을 설계한다.

## 범위

**포함**: 취약점 심각도, 유지보수 상태, 타이포스쿼팅 여부, 에이전트 권한 등 어떤 신호를 어떤 공식으로 결합해 위험 점수를 낼지 — 무엇을 신호로 쓸지와 그 공식은 담당자가 직접 설계한다.

**제외**: ML 기반 신규/변종 악성 패키지 탐지(R3 담당), 그래프 구성(R4 담당), 실제 코드 구현.

## 완료조건

- [ ] 위험도 계산 로직(신호 선정, 공식, 함수 시그니처)이 본인 설계로 문서화되어 있다
- [ ] R1이 실제로 무엇을 줄 수 있는지 확인하고, 필요한 입력을 맞췄다
- [ ] R4가 이 출력을 어떻게 쓸지 확인하고, 필요한 출력 형태를 맞췄다
- [ ] 맞춰보며 나온 문제와 최종 결정이 결정 기록에 남아 있다

판정 기준(스키마 필드 일치 등)은 [`docs/governance/REVIEW_CHECKLIST.md`](../governance/REVIEW_CHECKLIST.md) 참고.

## 참고 자료 (강제 아님 — 출발점)

- `schemas/risk_score.schema.json` — DRAFT(팀 검토 전)
- `docs/contracts/sample_dataset.md`, `docs/review/decisions/r2-risk-analyzer.md` — 역시 시뮬레이션 초안

## 담당 문서

`docs/design/02-risk-analyzer.md`
결정 기록: [`docs/review/decisions/r2-risk-analyzer.md`](../review/decisions/r2-risk-analyzer.md)

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
