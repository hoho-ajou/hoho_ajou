# CONTRIBUTING — AASM 협업 가이드

4개 모듈이 순서대로 데이터를 주고받는 구조(Collector → Risk Analyzer/ML → Attack Path Engine → Dashboard)이기 때문에, **"누가 무엇을 넘겨주는가"의 계약(인터페이스)** 을 지키는 게 이 정책의 핵심입니다.

---

## 1. 저장소 구조 (모노레포)

지금은 **설계 검토 단계**라 모듈 코드 폴더는 아직 없습니다. 실제 구현 시작 시 모듈별 폴더(`collector/`, `risk-analyzer/`, `ml-detector/`, `attack-path/`, `dashboard/`)를 하나의 저장소 안에 만듭니다(4인 규모에서 저장소를 쪼개면 관리 부담만 커짐).

```
aasm/
├── schemas/             # ⭐ 모듈 간 데이터 계약(JSON Schema) — 아래 3번 참고
├── docs/                # 설계 문서·거버넌스·검토 기록 — 지금 여기가 본체
└── .github/
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md
```

문서 전체 지도는 [`docs/DOCUMENT_GUIDE.md`](docs/DOCUMENT_GUIDE.md) 참고.

## 2. 브랜치 전략

- `main` — 항상 동작하는 상태만 유지. **직접 push 금지**, PR로만 병합
- `<모듈>/<이슈번호>-<짧은설명>` — 작업 브랜치
  - 예: `collector/12-pypi-metadata-fetch`, `risk-analyzer/18-cvss-scoring`, `ml-detector/23-feature-extraction`, `attack-path/30-graph-builder`, `dashboard/35-cytoscape-view`

별도 `develop` 브랜치는 두지 않습니다. 4인 규모에서 브랜치가 늘어날수록 관리 비용만 커집니다 — `main`을 기준으로 각자 브랜치 따서 PR로 합치는 단순 구조(트렁크 기반)로 갑니다.

## 3. ⭐ 모듈 간 인터페이스 계약 (`schemas/`) — 가장 중요

이전 로드맵 검증에서 나온 문제(누가 언제 무엇을 넘겨받는지 안 정해져서 일정이 꼬임)를 Git 차원에서 막는 장치입니다.

- `schemas/collector_output.schema.json` — Collector가 만드는 SBOM·의존성 목록의 형식
- `schemas/risk_score.schema.json` — Risk Analyzer가 만드는 위험 점수 JSON 형식
- `schemas/ml_result.schema.json` — ML 이상탐지 결과 형식
- `schemas/attack_graph.schema.json` — Attack Path Engine이 만드는 그래프 형식

**규칙**: `schemas/` 안의 파일을 변경하는 PR은 그 스키마를 **만드는 사람 + 받아쓰는 사람 전원의 승인**이 있어야 병합 가능합니다 (아래 CODEOWNERS 참고). 즉 R1 혼자 출력 형식을 바꾸면 안 되고, R2·R3 담당자 동의를 반드시 받아야 합니다.

실제 매핑은 [`.github/CODEOWNERS`](.github/CODEOWNERS), 역할별 담당자는 [`docs/governance/OWNERSHIP.md`](docs/governance/OWNERSHIP.md) 참고.

## 4. 이슈(Issue) 정책

**모든 작업은 이슈로 시작합니다.**

- 전체 Epic: `docs/epics/00-overall.md` = GitHub Issue #1 하나뿐. 형식은 [`docs/contracts/epic_schema.md`](docs/contracts/epic_schema.md).
- 역할(R1~R4) 상위 이슈: `docs/roles/*.md` — Epic #1을 승계(`Part of #1`)하며, 역할별 목표·범위·완료조건을 담음. 형식은 [`docs/contracts/role_issue_schema.md`](docs/contracts/role_issue_schema.md). 요약표는 [`docs/governance/OWNERSHIP.md`](docs/governance/OWNERSHIP.md).
- 하위 이슈: 담당자가 자기 역할 상위 이슈 아래 직접 생성. 형식은 [`docs/contracts/subissue_schema.md`](docs/contracts/subissue_schema.md), GitHub 템플릿은 [`.github/ISSUE_TEMPLATE/subissue.yml`](.github/ISSUE_TEMPLATE/subissue.yml).
- 진행 현황: [`docs/review/ISSUE_TRACKER.md`](docs/review/ISSUE_TRACKER.md)

라벨은 쓰지 않습니다 — 4인 규모에서는 이슈 제목의 `[모듈]` 접두사와 담당자 지정만으로 충분합니다. 진행 상태는 [`docs/review/ISSUE_TRACKER.md`](docs/review/ISSUE_TRACKER.md)로 관리합니다.

## 5. 커밋 메시지 (Conventional Commits)

```
<type>(<모듈>): <내용> (#이슈번호)

예)
feat(collector): PyPI JSON API 메타데이터 조회 추가 (#12)
fix(risk-analyzer): CVSS 점수 정규화 버그 수정 (#19)
docs(schemas): attack_graph 스키마에 필드 설명 추가 (#31)
```
`type`: `feat` `fix` `docs` `refactor` `test` `chore`

## 6. Pull Request 정책

PR 템플릿·필드별 요구사항·머지 조건은 [`docs/contracts/pr_schema.md`](docs/contracts/pr_schema.md)를 따릅니다. 핵심만 요약하면:

- **리뷰어 1명 이상 승인 필수** — 자기 코드 자기가 머지 금지
- **누가 리뷰하는가**: 그 모듈의 출력을 받아쓰는 다음 담당자가 우선 리뷰 (예: Collector PR → Risk Analyzer·ML 담당자)
- `schemas/` 변경 PR은 CODEOWNERS 전원 승인 필수
- 병합 방식은 **Squash and merge**
- main 브랜치 보호: 직접 push 차단, PR 승인 없이 병합 차단

## 7. 마일스톤 — 로드맵과 그대로 매핑

GitHub Milestone을 로드맵의 8개 2주 블록과 동일하게 만듭니다.

| Milestone | 기간 | 목표 |
|---|---|---|
| M1 탐색 | 1~2주 | 범위 확정 |
| M2 설계 | 3~4주 | 아키텍처·스키마 초안 확정 (자문①) |
| M3 자산수집 | 5~6주 | Collector MVP + SBOM |
| M4 위험탐지초안 | 7~8주 | Risk Analyzer·ML v0 (자문②) |
| M5 핵심엔진 | 9~10주 | Attack Path Engine 구현 |
| M6 통합검증 | 11~12주 | Dashboard 통합, PoC (자문③) |
| M7 발표개선 | 13~14주 | 기말PT, 개선 |
| M8 마무리 | 15~16주 | 문서화, 정리 |

각 마일스톤 종료 시점에 태그를 남깁니다: `v0.1-collector-mvp`, `v0.2-risk-ml-v0`, `v0.3-integrated`, `v1.0-final` — 나중에 최종보고서·시연 자료로 그대로 활용 가능합니다.

## 8. 예외 상황

- **기말PT 직전 긴급 수정**: `hotfix/<설명>` 브랜치로 main에서 분기 → 리뷰 1명 승인만으로 빠르게 병합 허용
- **머지 충돌**: 충돌난 사람이 직접 rebase 후 재요청 (강제 push는 자기 브랜치에서만)
