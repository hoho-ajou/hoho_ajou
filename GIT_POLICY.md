# AASM Git 운영 정책

4개 모듈이 순서대로 데이터를 주고받는 구조(Collector → Risk Analyzer/ML → Attack Path Engine → Dashboard)이기 때문에, **"누가 무엇을 넘겨주는가"의 계약(인터페이스)** 을 지키는 게 이 정책의 핵심입니다.

---

## 1. 저장소 구조 (모노레포)

4개를 따로 저장소로 쪼개면 학부생 4인 규모에서 관리 부담만 커지므로, **하나의 저장소 안에 모듈별 폴더**로 관리합니다.

```
aasm/
├── collector/           # Dependency Collector (담당: 총괄/A)
├── risk-analyzer/       # Risk Analyzer (담당: 위험분석)
├── ml-detector/         # ML 이상탐지 (담당: ML탐지)
├── attack-path/         # Attack Path Engine (담당: 공격경로)
├── dashboard/           # Dashboard (담당: 공격경로/시각화)
├── schemas/             # ⭐ 모듈 간 데이터 계약(JSON Schema) — 아래 3번 참고
├── docs/
└── .github/
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md
```

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

**규칙**: `schemas/` 안의 파일을 변경하는 PR은 그 스키마를 **만드는 사람 + 받아쓰는 사람 전원의 승인**이 있어야 병합 가능합니다 (아래 CODEOWNERS 참고). 즉 Collector 혼자 출력 형식을 바꾸면 안 되고, Risk Analyzer·ML 담당자 동의를 반드시 받아야 합니다.

`.github/CODEOWNERS` 예시:
```
/schemas/collector_output.schema.json   @총괄 @위험분석담당 @ML담당
/schemas/risk_score.schema.json         @위험분석담당 @공격경로담당
/schemas/ml_result.schema.json          @ML담당 @공격경로담당
/schemas/attack_graph.schema.json       @공격경로담당 @대시보드담당
/collector/                             @총괄
/risk-analyzer/                         @위험분석담당
/ml-detector/                           @ML담당
/attack-path/                           @공격경로담당
/dashboard/                             @공격경로담당
```

## 4. 이슈(Issue) 정책

**모든 작업은 이슈로 시작합니다.** 노션 "일정" DB의 항목을 그대로 GitHub 이슈로 옮겨서 1:1 매칭시키세요.

### 이슈 템플릿 (`.github/ISSUE_TEMPLATE/task.md`)
```markdown
---
name: 작업 (Task)
about: 일정 DB의 작업 항목을 이슈로 등록
labels: ''
---

## 목표
(이 이슈가 끝나면 무엇이 가능해지는지 한 줄로)

## 관련 모듈
- [ ] Dependency Collector
- [ ] Risk Analyzer
- [ ] ML 이상탐지
- [ ] Attack Path Engine
- [ ] Dashboard

## 완료 조건 (Acceptance Criteria)
- [ ]
- [ ]

## 선행 이슈 (이 작업 전에 끝나야 하는 것)
- Depends on #

## 참고 자료
(study_week1, resources/curated_list.md 등 관련 링크)
```

### 라벨
- 모듈 라벨: `collector` `risk-analyzer` `ml` `attack-path` `dashboard` `schema`(스키마 변경) `infra`
- 유형 라벨: `feature` `bug` `docs` `research`
- 우선순위: `P0` `P1` `P2`
- 상태는 라벨 대신 **GitHub Projects 칸반 보드**(할일/진행중/리뷰중/완료)로 관리 → 노션 "산출물" DB 상태와 동기화

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

### PR 템플릿 (`.github/PULL_REQUEST_TEMPLATE.md`)
```markdown
## 변경 내용


## 관련 이슈
Closes #

## 스키마 변경 여부
- [ ] 이 PR은 schemas/ 안의 파일을 변경하지 않음
- [ ] 변경함 → 관련 모듈 담당자에게 리뷰 요청 완료

## 테스트 방법


## 체크리스트
- [ ] 로컬에서 정상 동작 확인
- [ ] 관련 문서(README 등) 업데이트
```

### 병합 규칙
- **리뷰어 1명 이상 승인 필수** — 자기 코드 자기가 머지 금지
- **누가 리뷰하는가**: 그 모듈의 출력을 받아쓰는 다음 담당자가 우선 리뷰 (예: Collector PR → Risk Analyzer·ML 담당자가 리뷰. 인터페이스 깨지는지 제일 먼저 알 수 있는 사람이기 때문)
- `schemas/` 변경 PR은 CODEOWNERS 전원 승인 필수
- 병합 방식은 **Squash and merge** (커밋 히스토리 깔끔하게 유지)
- main 브랜치 보호 설정: 직접 push 차단, PR 승인 없이 병합 차단

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
