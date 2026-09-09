# [R3] ML 이상탐지 설계

## 상위 이슈
Part of #1

## 목표

R1의 출력을 입력받아, R2의 규칙 기반 탐지가 놓치는 신규·변종 악성 패키지를 탐지하는 로직을 설계한다.

## 범위

**포함**: 어떤 feature를 뽑을지, 어떤 모델을 쓸지, 학습 데이터를 어떻게 구성할지 — 담당자가 직접 설계한다.

**제외**: PyPI 외 생태계, 실시간/온라인 학습, 실제 모델 학습·추론 코드 구현.

## 완료조건

- [ ] feature·모델·학습 절차가 본인 설계로 문서화되어 있다
- [ ] R1이 실제로 무엇을 줄 수 있는지 확인하고, 필요한 입력을 맞췄다
- [ ] R4가 이 출력을 어떻게 쓸지 확인하고, 필요한 출력 형태를 맞췄다
- [ ] 맞춰보며 나온 문제와 최종 결정이 결정 기록에 남아 있다

판정 기준(스키마 필드 일치 등)은 [`docs/governance/REVIEW_CHECKLIST.md`](../governance/REVIEW_CHECKLIST.md) 참고.

## 참고 자료 (강제 아님 — 출발점)

- `schemas/ml_result.schema.json` — DRAFT(팀 검토 전)
- `docs/contracts/sample_dataset.md`, `docs/review/decisions/r3-ml-detector.md` — 역시 시뮬레이션 초안

## 담당 문서

`docs/design/03-ml-detector.md`
결정 기록: [`docs/review/decisions/r3-ml-detector.md`](../review/decisions/r3-ml-detector.md)

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
