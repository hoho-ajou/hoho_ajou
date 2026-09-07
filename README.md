# AASM — AI Agent Attack Surface Management

호호전승은 AI 에이전트의 의존성·권한·외부 연동 정보를 분석하고, 공급망 위협에 따른 공격 가능 경로를 탐지·시각화하는 **AASM 플랫폼 개발 프로젝트입니다.**

## 모듈 구성

| 모듈 | 설명 | 설계 문서 |
|---|---|---|
| `collector/` | Dependency Collector — 의존성·외부연동 자동 수집, SBOM 생성 | [docs/design/01-collector.md](docs/design/01-collector.md) |
| `risk-analyzer/` | Risk Analyzer — 위험도 점수화 (CVSS+EPSS+타이포스쿼팅+권한가중치) | [docs/design/02-risk-analyzer.md](docs/design/02-risk-analyzer.md) |
| `ml-detector/` | ML 이상탐지 — 신규/변종 악성 패키지 탐지 (Random Forest) | [docs/design/03-ml-detector.md](docs/design/03-ml-detector.md) |
| `attack-path/` | Attack Path Engine — 공격경로 그래프 생성 (NetworkX) | [docs/design/04-attack-path.md](docs/design/04-attack-path.md) |
| `dashboard/` | Dashboard — 웹 시각화 (Cytoscape.js) | [docs/design/05-dashboard.md](docs/design/05-dashboard.md) |
| `schemas/` | 모듈 간 데이터 계약 (JSON Schema) | — |

전체 설계: [docs/design/00-overall.md](docs/design/00-overall.md) · [아키텍처 도면](docs/design/architecture_diagram.md)

## 모듈 간 연결

- 공통 샘플 데이터셋(4개 모듈 전부가 참조하는 하나의 예시): [docs/contracts/sample_dataset.md](docs/contracts/sample_dataset.md)
- 인터페이스 맵(필드가 어디로 흘러가는지 한 페이지 정리): [docs/contracts/interface_map.md](docs/contracts/interface_map.md)

## 운영 정책

- Git 브랜치/PR/이슈 정책: [GIT_POLICY.md](GIT_POLICY.md)
- 이슈/PR 공통 스키마: [docs/contracts/epic_schema.md](docs/contracts/epic_schema.md), [subissue_schema.md](docs/contracts/subissue_schema.md), [pr_schema.md](docs/contracts/pr_schema.md)
- 팀 차원 미결정 사항: [docs/epics/06-open-decisions.md](docs/epics/06-open-decisions.md)
- 용어집(구현자용): [docs/glossary.md](docs/glossary.md)
