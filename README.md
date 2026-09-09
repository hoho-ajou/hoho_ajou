# AASM — AI Agent Attack Surface Management

호호전승은 AI 에이전트의 의존성·권한·외부 연동 정보를 분석하고, 공급망 위협에 따른 공격 가능 경로를 탐지·시각화하는 AASM 플랫폼 개발 프로젝트입니다.

이 저장소는 실행 프로그램을 배포하는 곳이 아닙니다. 실제 구현을 시작하기 전에, 전체 흐름과 모듈 간 입출력 계약을 팀이 함께 설계·검토하는 공간입니다.

## 30초 요약

- Dependency Collector가 AI 에이전트 저장소를 스캔해 의존성·외부연동·취약점·SBOM을 뽑습니다.
- Risk Analyzer와 ML 이상탐지가 각각 규칙 기반 위험도와 신규/변종 악성 패키지를 병렬로 탐지합니다.
- Attack Path Engine이 이 둘을 그래프로 연결해 "의존성 → 에이전트 → 권한 → 공격경로"를 추적합니다.
- Dashboard가 그 그래프를 웹에서 인터랙티브하게 보여줍니다.
- 지금은 **설계 검토 단계**이며 실행 코드는 아직 없습니다.

모르는 용어는 [용어집](docs/GLOSSARY.md), 각 파일의 목적은 [전체 문서 지도](docs/DOCUMENT_GUIDE.md)에서 확인할 수 있습니다.

## 현재 단계

```text
DESIGN_AUTHORED
REVIEW_REQUIRED
NOT_IMPLEMENTED
```

- 6개 모듈 설계 문서(`docs/design/`)와 4개 모듈 간 스키마(`schemas/`) 초안이 작성되어 있습니다.
- 각 담당자가 자기 모듈 설계를 [리뷰 체크리스트](docs/governance/REVIEW_CHECKLIST.md) 기준으로 심화하는 단계입니다.
- 리뷰가 끝나기 전에는 설계 확정이나 구현 완료를 주장하지 않습니다.

## 모듈 구성

| 모듈 | 설명 | 설계 문서 | 담당 역할 |
|---|---|---|---|
| Dependency Collector | 의존성·외부연동 자동 수집, SBOM 생성 | [docs/design/01-collector.md](docs/design/01-collector.md) | R1 |
| Risk Analyzer | 위험도 점수화 (CVSS+EPSS+타이포스쿼팅+권한가중치) | [docs/design/02-risk-analyzer.md](docs/design/02-risk-analyzer.md) | R2 |
| ML 이상탐지 | 신규/변종 악성 패키지 탐지 (Random Forest) | [docs/design/03-ml-detector.md](docs/design/03-ml-detector.md) | R3 |
| Attack Path Engine | 공격경로 그래프 생성 (NetworkX) | [docs/design/04-attack-path.md](docs/design/04-attack-path.md) | R4 |
| Dashboard | 웹 시각화 (Cytoscape.js) | [docs/design/05-dashboard.md](docs/design/05-dashboard.md) | R4 |
| `schemas/` | 모듈 간 데이터 계약 (JSON Schema) | — | — |

역할별 담당자는 [docs/governance/OWNERSHIP.md](docs/governance/OWNERSHIP.md) 참고.

전체 설계: [docs/design/00-overall.md](docs/design/00-overall.md) · [아키텍처 도면](docs/design/architecture_diagram.md)
모듈 간 연결: [공통 샘플 데이터셋](docs/contracts/sample_dataset.md) · [인터페이스 맵](docs/contracts/interface_map.md)

## 설계 검토 운영 방식

이 프로젝트는 **main의 공개 초안 + 각자 설계 심화** 방식으로 진행합니다.

### Issue 구조

```text
#1 전체 Epic (총괄 소유)
└─ R1~R4 각자의 상위 이슈 (docs/roles/*.md, Epic #1 승계)
    └─ 각자 직접 만드는 하위 이슈
```

R1~R4 상위 이슈의 목표·범위·완료조건은 [`docs/roles/`](docs/roles/)에 있고, 요약은 [`docs/governance/OWNERSHIP.md`](docs/governance/OWNERSHIP.md)에서 봅니다. 각자 자기 상위 이슈 아래 하위 이슈를 직접 만들어 진행합니다 ([`.github/ISSUE_TEMPLATE/subissue.yml`](.github/ISSUE_TEMPLATE/subissue.yml) 사용). 리뷰·머지 절차는 [CONTRIBUTING.md](CONTRIBUTING.md)를 따릅니다.

진행 현황은 [실제 Issue 현황](docs/review/ISSUE_TRACKER.md), 확정된 설계 결정은 [결정 기록](docs/review/decisions/README.md)에서 확인합니다.

## 담당 영역

역할별 담당자와 CODEOWNERS는 [docs/governance/OWNERSHIP.md](docs/governance/OWNERSHIP.md)를 참고하세요.

## 안전 원칙

- 개인 제출용 문서(계획서/OT자료), API 키, 실제 개인정보는 저장소에 올리지 않습니다.
- 실제 취약 패키지·공격 경로 재현은 승인된 격리 환경(PoC)에서만 수행합니다.
- 최종 결과 공개 여부는 사람이 결정합니다.
