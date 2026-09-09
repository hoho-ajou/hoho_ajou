# [R1] Dependency Collector 설계

## 상위 이슈
Part of #1

## 목표

AI 에이전트 저장소를 스캔해서 (1) 의존성 목록, (2) 외부 연동 도구, (3) 취약점 정보, (4) 표준 SBOM을 뽑아내는 파이프라인 입구 모듈의 설계를 완성한다. 이 모듈의 산출물이 R2·R3의 입력이 된다.

## 범위

**포함**: 의존성 추출, 외부 연동(에이전트가 무엇에 접근 가능한지) 탐지, 취약점 정보 확보, 표준 SBOM 생성 — 이 네 가지를 어떤 기법·어떤 도구·어떤 출력 형식으로 할지는 담당자가 직접 설계한다.

**제외**: reachability 분석(취약 함수 실제 호출 여부), 컨테이너 OS 패키지 심층 분석, 실제 코드 구현.

## 완료조건

- [ ] 위 네 가지를 어떻게 할지에 대한 본인의 설계(함수 시그니처, 출력 형식, 엣지케이스)가 문서화되어 있다
- [ ] 그 출력을 실제로 받아쓰는 R2·R3 담당자와 맞춰보고, 안 맞는 부분을 찾아 조정했다
- [ ] 맞춰보며 나온 문제와 최종 결정이 결정 기록에 남아 있다

판정 기준(스키마 필드 일치 등)은 [`docs/governance/REVIEW_CHECKLIST.md`](../governance/REVIEW_CHECKLIST.md) 참고.

## 참고 자료 (강제 아님 — 출발점)

- `schemas/collector_output.schema.json` — DRAFT(팀 검토 전). 그대로 써도 되고, 설계하다 보니 다르게 필요하면 바꿔도 됨
- `docs/contracts/sample_dataset.md`, `docs/review/decisions/r1-collector.md` — 역시 시뮬레이션 초안

## 담당 문서

`docs/design/01-collector.md`
결정 기록: [`docs/review/decisions/r1-collector.md`](../review/decisions/r1-collector.md)

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
