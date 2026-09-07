# [Epic] 전체 파이프라인 오케스트레이션 & 모듈 간 계약 확립

## 목표

Collector → (Risk Analyzer, ML 병렬) → Attack Path Engine → Dashboard로 이어지는 5개 모듈이 실제로 데이터를 주고받을 수 있도록, 오케스트레이션 방식과 모듈 간 인터페이스를 **설계 문서 수준에서** 확정한다. 실제 구현(코드 작성)은 이 Epic의 범위가 아니며, 설계가 AI 구현체가 그대로 따라갈 수 있을 만큼 구체적인지가 완료 기준이다.

## 범위

**IN**
- `pipeline/` 오케스트레이터의 호출 흐름·에러 전파 방식을 의사코드 수준으로 설계
- `data/` 중간 산출물 디렉토리 규약(파일 네이밍, `run_id` 규칙) 문서화
- 로깅·설정·테스트 등 프로젝트 전역 컨벤션 명시
- CODEOWNERS, 브랜치 전략 등 GIT_POLICY.md 내용의 실제 GitHub 설정 반영

**OUT** (모듈별 Epic으로 위임, 실제 코드 작성 전부 포함)
- 각 스키마 파일의 상세 필드 정의(각 모듈 담당자가 자기 Epic에서 작성)
- `pipeline/run.py` 등 실제 코드 구현
- 각 모듈 내부 로직 구현
- 클라우드 인프라(AWS EC2/S3/CloudWatch) 세부 구축

## 완료조건

- [ ] `docs/design/00-overall.md` 설계안이 팀 전체 리뷰 후 확정됨
- [ ] 오케스트레이션 흐름(호출 순서, 병렬 fan-out/fan-in, 각 단계 실패 시 처리 방식)이 의사코드 또는 순서도 수준으로 문서화됨
- [ ] 로깅/설정/테스트 컨벤션이 설계 문서에 명시됨
- [ ] `docs/epics/06-open-decisions.md`의 팀 차원 결정 사항이 확정되어 이 문서에 반영됨

## 공통계약

- `docs/contracts/sample_dataset.md` — 전 모듈 공통 예시 시나리오
- `docs/contracts/interface_map.md` — 필드 단위 흐름 정리
- `schemas/*.schema.json` 4개 — 공통 메타 필드(`run_id`, `schema_version` 등) 강제 여부는 `docs/epics/06-open-decisions.md` 결정 1 참고
- `GIT_POLICY.md` — 브랜치/이슈/PR 정책
- `docs/contracts/*.md` — 이슈/PR 공통 스키마

## 담당 문서

`docs/design/00-overall.md`

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
