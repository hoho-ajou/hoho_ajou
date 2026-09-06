# Epic: 전체 파이프라인 오케스트레이션 & 모듈 간 계약 확립

## Title suggestion
`[Epic] AASM 전체 파이프라인 오케스트레이션 및 schemas/ 계약 확립`

## 목표
Collector → (Risk Analyzer, ML 병렬) → Attack Path Engine → Dashboard로 이어지는 5개 모듈이 실제로 데이터를 주고받으며 end-to-end로 동작하도록, 오케스트레이션 방식과 모듈 간 인터페이스(`schemas/`)를 확정한다.

## 범위
**이 Epic에서 다루는 것 (IN)**
- `pipeline/` 오케스트레이터(각 모듈을 순서대로/병렬로 호출하는 얇은 CLI)의 구조 확정 및 최소 구현
- `data/` 중간 산출물 디렉토리 규약(파일 네이밍, `run_id` 규칙)
- `schemas/` 4개 파일의 존재 확정, 공통 메타 필드(`run_id`, `generated_at`, `source_module`, `schema_version`) 합의
- 로깅·설정·테스트 등 프로젝트 전역 컨벤션 문서화 및 팀 합의
- CODEOWNERS, 브랜치 전략 등 GIT_POLICY.md 내용의 실제 GitHub 설정 반영

**이 Epic에서 다루지 않는 것 (모듈별 Epic으로 위임)**
- 각 스키마 파일의 상세 필드 정의(Collector/Risk Analyzer/ML/Attack Path Engine 담당자가 각자 작성)
- 각 모듈 내부 로직 구현(파싱 알고리즘, 점수화 공식, ML 모델, 그래프 생성 로직, 시각화 UI)
- 클라우드 인프라(AWS EC2/S3/CloudWatch) 세부 구축

## 완료 조건
- [ ] `docs/design/00-overall.md` 설계안이 팀 전체 리뷰 후 확정됨
- [ ] `schemas/` 폴더에 4개 스키마 파일의 최소 스켈레톤(공통 메타 필드만 포함)이 생성되고 CODEOWNERS가 설정됨
- [ ] `pipeline/run.py`가 더미(mock) 입출력으로라도 5개 모듈 호출 순서(병렬 fan-out/fan-in 포함)를 실제로 실행해 보임
- [ ] 로깅/설정/테스트 컨벤션이 문서화되고 최소 1개 모듈에 시범 적용됨
- [ ] 각 모듈 담당자가 자기 모듈의 하위 Epic/이슈를 이 Epic 산하에 생성함

## 관련 모듈
- Dependency Collector
- Risk Analyzer
- ML 이상탐지
- Attack Path Engine
- Dashboard

## 참고 자료
- [`docs/design/00-overall.md`](../design/00-overall.md) — 이 Epic의 기반이 되는 상세 설계 문서
- [`GIT_POLICY.md`](../../GIT_POLICY.md) — 브랜치 전략, schemas/ CODEOWNERS 규칙, 이슈/PR 템플릿
- [`study_week1/architecture.html`](../../study_week1/architecture.html) — 전체 시스템 아키텍처 그림 및 5개 모듈 상세 설명
- `resources/curated_list.md` 중:
  - U. [OpenSSF 생태계 도구 — GUAC](https://rywalker.com/research/guac) (그래프 기반 통합 사례, Attack Path Engine과 발상 유사)
  - D. [Trivy vs Grype 비교](https://appsecsanta.com/sca-tools/trivy-vs-grype) (파일 기반 SCA 파이프라인 참고)
  - I. [Wiz — What is Attack Path Analysis?](https://www.wiz.io/academy/attack-path-analysis)

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
