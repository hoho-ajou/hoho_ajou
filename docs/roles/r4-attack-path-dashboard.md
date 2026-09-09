# [R4] Attack Path Engine + Dashboard 설계

## 상위 이슈
Part of #1

## 목표

R2·R3의 출력과 에이전트 권한 정보를 그래프로 연결해 공격 경로를 식별·우선순위화하고(Attack Path Engine), 그 결과를 웹에서 인터랙티브하게 보여준다(Dashboard).

## 범위

**포함**: 그래프 구조(노드/엣지 정의), 경로 탐색·우선순위화 방식, 권한 데이터 구조 정의, 화면 구성·시각화·필터링·백엔드 API 형태 — 담당자가 직접 설계한다.

**제외**: 그래프 DB 도입, PoC 에이전트 실제 제작, 실시간 스트리밍, 다중 사용자 인증, 실제 코드 구현.

## 완료조건

- [ ] 그래프 구조·경로 탐색·우선순위화 로직과 화면 구성·상호작용·백엔드 API가 본인 설계로 문서화되어 있다
- [ ] R1·R2·R3가 실제로 무엇을 줄 수 있는지 확인하고, 필요한 입력을 맞췄다
- [ ] 맞춰보며 나온 문제와 최종 결정이 결정 기록에 남아 있다

판정 기준(스키마 필드 일치 등)은 [`docs/governance/REVIEW_CHECKLIST.md`](../governance/REVIEW_CHECKLIST.md) 참고.

## 참고 자료 (강제 아님 — 출발점)

- `schemas/attack_graph.schema.json` — DRAFT(팀 검토 전)
- `docs/contracts/sample_dataset.md`, `docs/review/decisions/r4-attack-path-dashboard.md` — 역시 시뮬레이션 초안

## 담당 문서

`docs/design/04-attack-path.md`, `docs/design/05-dashboard.md`
결정 기록: [`docs/review/decisions/r4-attack-path-dashboard.md`](../review/decisions/r4-attack-path-dashboard.md)

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
