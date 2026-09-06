# AASM — AI Agent Attack Surface Management

AI 에이전트 프로젝트의 오픈소스 의존성을 자동 분석해, "의존성 → 에이전트 → 권한 → 공격경로"를 그래프로 연결해 시각화하는 보안 플랫폼입니다. 2026-2학기 파란학기제 도전과제.

## 모듈 구성

| 모듈 | 설명 | 설계 문서 |
|---|---|---|
| `collector/` | Dependency Collector — 의존성·외부연동 자동 수집, SBOM 생성 | [docs/design/01-collector.md](docs/design/01-collector.md) |
| `risk-analyzer/` | Risk Analyzer — 위험도 점수화 (CVSS+EPSS+타이포스쿼팅+권한가중치) | [docs/design/02-risk-analyzer.md](docs/design/02-risk-analyzer.md) |
| `ml-detector/` | ML 이상탐지 — 신규/변종 악성 패키지 탐지 (Random Forest) | [docs/design/03-ml-detector.md](docs/design/03-ml-detector.md) |
| `attack-path/` | Attack Path Engine — 공격경로 그래프 생성 (NetworkX) | [docs/design/04-attack-path.md](docs/design/04-attack-path.md) |
| `dashboard/` | Dashboard — 웹 시각화 (Cytoscape.js) | [docs/design/05-dashboard.md](docs/design/05-dashboard.md) |
| `schemas/` | 모듈 간 데이터 계약 (JSON Schema) | — |

전체 설계: [docs/design/00-overall.md](docs/design/00-overall.md)

## 운영 정책

- Git 브랜치/PR/이슈 정책: [GIT_POLICY.md](GIT_POLICY.md)
- 교차검토 결정 이력: [docs/design/_cross_review_questions.md](docs/design/_cross_review_questions.md)
- 이슈/PR 공통 스키마: [docs/contracts/epic_schema.md](docs/contracts/epic_schema.md), [subissue_schema.md](docs/contracts/subissue_schema.md), [pr_schema.md](docs/contracts/pr_schema.md)
- 팀 차원 미결정 사항: [docs/epics/06-open-decisions.md](docs/epics/06-open-decisions.md)
- 용어집(구현자용): [docs/glossary.md](docs/glossary.md)

## AI 구현용 통합 피드 파일

[AASM_FEED.md](AASM_FEED.md) — 위 모든 문서(정책+용어집+계약+설계+스키마+이슈)를 하나로 이어붙인 파일. 원본 파일을 고친 뒤에는 `bash scripts/build_feed.sh`를 다시 돌려서 재생성해야 합니다 (이 파일 자체는 직접 편집하지 않음).

## 학습 자료

- [study_week1/](study_week1/) — 1주차 학습자료 (개념/용어/사례)
- [resources/curated_list.md](resources/curated_list.md) — 참고자료 182개 큐레이션
