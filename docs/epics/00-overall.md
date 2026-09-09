# [Epic] AASM 전체 설계 및 구현 조율

## 목표

5개 모듈(Collector·Risk Analyzer·ML 이상탐지·Attack Path Engine·Dashboard)이 실제로 이어지는 하나의 파이프라인이 되도록 설계·조율한다. 이 Epic 하나가 전체 프로젝트를 담당하며, R1~R4가 각자 모듈을 맡아 그 안에서 작업한다.

## 범위

**포함**: 오케스트레이션 방식(모듈 호출 순서·오류 처리), 중간 산출물 저장 규약, 프로젝트 전역 컨벤션, R1~R4 간 조율, 팀 차원 결정 사항(공통 메타 필드 강제 여부, pipeline 코드 소유권, 데이터 저장 위치 등).

**제외**: 각 모듈 내부 로직(R1~R4가 직접 설계), 실제 코드 구현.

## 완료조건

- [ ] 오케스트레이션 흐름이 문서화되어 있다
- [ ] R1~R4가 각자 모듈 설계를 마친 뒤, 전체가 실제로 이어지는지 맞춰봤다
- [ ] 팀 차원 결정 사항이 확정되어 결정 기록에 반영됐다

판정 기준(스키마 필드 일치 등)은 [`docs/governance/REVIEW_CHECKLIST.md`](../governance/REVIEW_CHECKLIST.md) 참고.

## 참고 자료 (강제 아님 — 출발점)

- `docs/design/00-overall.md` — DRAFT(팀 검토 전)
- `docs/contracts/sample_dataset.md`, `docs/review/decisions/00-overall.md` — 역시 시뮬레이션 초안
- 역할별 목표/범위: [`docs/governance/OWNERSHIP.md`](../governance/OWNERSHIP.md)

## 담당 문서

`docs/design/00-overall.md`
결정 기록: [`docs/review/decisions/00-overall.md`](../review/decisions/00-overall.md)

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
