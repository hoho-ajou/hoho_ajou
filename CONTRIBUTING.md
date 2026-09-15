# CONTRIBUTING — AASM 협업 가이드

5개 모듈(Collector → Risk Analyzer/ML → Attack Path Engine → Dashboard)을 4명이 R1~R4로 나눠 맡습니다. 모듈이 순서대로 데이터를 주고받는 구조이기 때문에, **누가 무엇을 넘겨주는가의 계약(인터페이스)** 을 지키는 것이 이 정책의 핵심입니다.

---

## 1. 저장소 구조 (모노레포)

지금은 **설계 검토 단계**라 모듈 코드 폴더는 아직 없습니다. 실제 구현 시작 시 모듈별 폴더(`collector/`, `risk-analyzer/`, `ml-detector/`, `attack-path/`, `dashboard/`)를 하나의 저장소 안에 만듭니다.

```text
aasm/
├── schemas/             # 모듈 간 데이터 계약(JSON Schema) — 아래 3번 참고
├── docs/                # 설계 문서·거버넌스·검토 기록
├── scripts/             # 문서 일관성 검증 (validate_docs.py)
└── .github/
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md
```

문서 전체 지도는 [`docs/DOCUMENT_GUIDE.md`](docs/DOCUMENT_GUIDE.md) 참고.

## 2. 브랜치 전략

- `main` — 항상 동작하는 상태만 유지. **직접 push 금지**, PR로만 병합
- `<타입>/<모듈>-<번호>-<짧은설명>` — 역할(R1~R4) 작업 브랜치
  - 타입: `feat`/`fix`/`docs`/`refactor`/`test`/`chore` (§5 커밋 타입과 동일)
  - 모듈: `r1`/`r2`/`r3`/`r4`
  - 번호: 관련 이슈 번호
  - 예: `feat/r1-12-pypi-metadata-fetch`, `feat/r2-18-cvss-scoring`, `feat/r3-23-feature-extraction`, `feat/r4-30-graph-builder`
- `<타입>/<짧은설명>` — Epic 직속(PM) 작업이나 이슈 번호 없이 하는 작업(문서 정리 등)
  - 예: `docs/pr-template-sync`, `chore/codeowners-sync`

별도 `develop` 브랜치는 두지 않습니다. 4인 규모에서 브랜치가 늘어날수록 관리 비용만 커집니다 — `main`을 기준으로 각자 브랜치 따서 PR로 합치는 단순 구조(트렁크 기반)로 갑니다.

## 3. 모듈 간 인터페이스 계약

- `schemas/collector_output.schema.json` — Collector가 만드는 SBOM·의존성 목록의 형식
- `schemas/risk_score.schema.json` — Risk Analyzer가 만드는 위험 점수 JSON 형식
- `schemas/ml_result.schema.json` — ML 이상탐지 결과 형식
- `schemas/attack_graph.schema.json` — Attack Path Engine이 만드는 그래프 형식

**규칙**: `schemas/` 안의 파일을 변경하는 PR은 그 스키마를 **만드는 사람 + 받아쓰는 사람 전원의 승인**이 있어야 병합 가능합니다. 즉 R1 혼자 출력 형식을 바꾸면 안 되고, R2·R3 담당자 동의를 반드시 받아야 합니다.

실제 매핑은 [`.github/CODEOWNERS`](.github/CODEOWNERS), 역할별 담당자는 [`docs/governance/OWNERSHIP.md`](docs/governance/OWNERSHIP.md) 참고.

## 4. 이슈(Issue) 정책

**모든 작업은 이슈로 시작합니다.**

- 전체 작업을 이슈로 생성하고, 작은 단위로 분할, 할당합니다
- 각 역할 담당자는 할당된 이슈를 이해하고 하위이슈로 쪼개어 하나씩 수행합니다
- 역할별 하위 이슈는 [`.github/ISSUE_TEMPLATE/subissue.md`]의 템플릿을 기반으로 만듭니다
- 비역할 하위 이슈는 [`.github/ISSUE_TEMPLATE/pm-subissue.md`]의 템플릿을 기반으로 만듭니다

## 5. 커밋 메시지 (Conventional Commits)

```text
<type>(<모듈>): <내용> (#이슈번호)

예)
feat(r1): PyPI JSON API 메타데이터 조회 추가 (#12)
fix(r2): CVSS 점수 정규화 버그 수정 (#19)
docs(schemas): attack_graph 스키마에 필드 설명 추가 (#31)
```

`type`: `feat` `fix` `docs` `refactor` `test` `chore`

`모듈`: `r1`/`r2`/`r3`/`r4`(역할) · `pm`(Epic 직속) · `schemas`(여러 역할에 걸친 스키마 변경, CODEOWNERS 전원 승인 대상)

## 6. Pull Request 정책

PR 템플릿은 [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md). 머지 조건 핵심만 요약하면:

- **리뷰어 1명 이상 승인 필수** — 자기 코드 자기가 머지 금지
- **누가 리뷰하는가**: PR을 올린 사람이 지정한 리뷰어
- 병합 방식은 **Squash and merge**
- main 브랜치 보호: 직접 push 차단, PR 승인 없이 병합 차단
