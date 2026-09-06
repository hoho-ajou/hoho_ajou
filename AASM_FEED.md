# AASM — 통합 설계 피드 (AI 구현용 단일 문서)

이 파일 하나에 AASM 프로젝트를 처음부터 구현하는 데 필요한 설계/계약/스키마/용어를 전부 모았습니다.
각 섹션은 실제 저장소 파일(`docs/`, `schemas/`, `GIT_POLICY.md`)의 원문이며, 이 파일은 그것들을 순서대로 이어붙인 것입니다.
생성: 2026-09-06 / 원본이 갱신되면 이 파일도 다시 생성해야 합니다 (수동 편집 금지 — 각 원본 파일을 고치세요).

## 목차

1. Git/이슈/PR 운영 정책 (GIT_POLICY.md)
2. 용어집 (docs/glossary.md)
3. 이슈 계약: Epic / 하위 이슈 / PR 스키마 (docs/contracts/)
4. 전체 아키텍처 설계 (docs/design/00-overall.md)
5. 모듈별 기술 설계 (docs/design/01~05)
6. 모듈 간 데이터 계약 — JSON Schema 원문 (schemas/)
7. 교차검토 이력 (docs/design/_cross_review_questions.md)
8. 상위 이슈(Epic) 목록 (docs/epics/)

---

# ============================================================
# 원본: GIT_POLICY.md
# ============================================================

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


# ============================================================
# 원본: docs/glossary.md
# ============================================================

# 용어집 (구현자용 — schemas/design 전 모듈 공통)

`study_week1/README.md` §3의 용어집이 "처음 배우는 사람" 대상이라면, 이 문서는 **schemas/*.json과 docs/design/*.md를 그대로 구현할 사람(또는 AI)** 대상입니다. 각 스키마 필드명이 어느 용어에서 왔는지 연결하는 데 씁니다.

## 전체 파이프라인 공통

| 용어 | 정의 |
|---|---|
| **run_id** | 파이프라인 한 번의 전체 실행을 식별하는 ID. Collector가 생성해서 이후 모든 모듈 출력에 그대로 전달됨 |
| **schema_version** | 각 `schemas/*.json` 파일의 버전 문자열. 필드 추가/변경 시 올림 (`GIT_POLICY.md` §3) |
| **파일 기반 핸드오프** | 모듈 간 통신을 API 호출이 아니라 JSON 파일 쓰기/읽기로 하는 방식(`00-overall.md` §2). 각 모듈은 독립 실행 가능해야 함 |
| **CODEOWNERS 대상 파일** | `schemas/*.json`처럼 변경 시 관련 모듈 담당자 전원의 승인이 강제되는 파일 |

## Dependency Collector

| 용어 | 정의 |
|---|---|
| **SBOM** (Software Bill of Materials) | 소프트웨어를 구성하는 모든 패키지·라이선스·해시의 목록. `collector_output.schema.json`의 `sbom{}` 필드 |
| **CycloneDX** | SBOM을 표현하는 표준 JSON/XML 포맷 (보안 중심). `cyclonedx-py`로 생성 |
| **PURL** (Package URL) | `pkg:pypi/requests@2.31.0` 형태로 패키지를 생태계+이름+버전까지 정확히 식별하는 표준 |
| **OSV** | Google이 운영하는 오픈소스 취약점 DB/API. Collector가 PyPI 메타데이터로 못 채운 취약점을 보완 조회 |
| **resolution_status** | 의존성 하나가 PyPI 조회에 성공(`resolved`)했는지 실패(`unresolved`)했는지. 실패해도 파이프라인은 계속 진행 |
| **MCP** (Model Context Protocol) | LLM이 외부 도구/데이터에 접근하는 표준 프로토콜(JSON-RPC 2.0, Host→Client→Server). Collector가 코드/설정 파일에서 탐지해야 할 "외부 연동" 유형 중 하나 |
| **agent.permissions[]** | 에이전트 코드가 실제로 행사하는 권한(타입+대상 자산). **Collector가 정적 스캔으로 값을 채우지만, 필드의 enum·구조는 Attack Path Engine이 소유**(`04-attack-path.md` 확정 사항 1번) |

## Risk Analyzer

| 용어 | 정의 |
|---|---|
| **CVSS** (Common Vulnerability Scoring System) | 취약점 심각도 0~10 점수. `signals.cvss_norm`은 이를 0~1로 정규화한 값 |
| **EPSS** (Exploit Prediction Scoring System) | 어떤 취약점이 실제로 악용될 확률(0~1)을 예측하는 지표. CVSS(심각도)와 달리 "실제 악용 가능성"을 봄 |
| **타이포스쿼팅 (typosquatting)** | 인기 패키지와 이름이 비슷한 가짜 패키지(예: `requests`→`requets`)로 오설치를 유도하는 공격. `typo_flag`/`typo_nearest_match`는 Levenshtein 거리로 탐지 |
| **staleness_score** | 패키지가 얼마나 방치됐는지(마지막 릴리스 이후 경과 개월 수 기반) 나타내는 0~1 값. 유지보수 중단 패키지의 위험도를 가중 |
| **permission_weight** | 에이전트가 가진 권한의 위험도에 따른 가중치(1.0~3.0). Attack Path Engine이 정의한 `agent.permissions[]`를 참조해 계산 |
| **risk_score / risk_level** | 각 패키지의 최종 위험도 — 숫자(`risk_score`)와 3단계 등급(`LOW`/`MEDIUM`/`HIGH`, `risk_level`) 둘 다 제공 |

## ML 이상탐지

| 용어 | 정의 |
|---|---|
| **Random Forest** | 다수의 결정 트리를 앙상블해 분류하는 지도학습 모델. 기존에 알려진 악성 패턴 학습용 |
| **Isolation Forest** | 정상 데이터의 "다수 패턴"에서 벗어난 이상치를 탐지하는 비지도학습 모델. 신규/변종 악성 패키지 탐지용 |
| **triggered_features** | 모델이 이 패키지를 악성으로 판단하는 데 기여한 feature와 중요도 상위 5개 목록. 그대로 Dashboard 상세 패널에 사용 가능(`04-attack-path.md` 확정 사항 4번) |
| **confidence_score** | ML 모델의 판단 확신도(0~1). Attack Path Engine이 `risk_score`와 가중합으로 결합 |

## Attack Path Engine

| 용어 | 정의 |
|---|---|
| **NetworkX** | Python 그래프 라이브러리. Neo4j 대신 채택(외부 DB 불필요, 소규모 그래프에 충분) |
| **betweenness_centrality** | 그래프에서 한 노드가 다른 노드 간 최단 경로에 얼마나 자주 등장하는지 나타내는 지표. 핵심 자산/병목 식별에 사용 |
| **Yen's algorithm / shortest_simple_paths** | 두 노드 사이의 최단 경로뿐 아니라 상위 k개 경로까지 순서대로 찾는 알고리즘. 공격 경로 후보를 여러 개 뽑을 때 사용 |
| **CNAPP** | 클라우드 자산·권한·네트워크를 그래프로 연결해 공격 경로를 찾는 방법론. BloodHound의 `shortestPath()` 개념을 참고했지만 직접 의존하지는 않음 |
| **node_sequence / edge_sequence** | `paths[]` 안에서 경로를 구성하는 노드/엣지 id의 순서 목록. `nodes[]`/`edges[]`의 실제 id를 참조해야 함(참조 무결성, export 시 단위 테스트로 강제) |

## Dashboard

| 용어 | 정의 |
|---|---|
| **Cytoscape.js** | 그래프 시각화 JS 라이브러리(vis-network/Sigma.js 대신 채택). `elements:{nodes,edges}` 포맷은 프론트엔드가 로드 시 변환 — `attack_graph.schema.json` 자체는 이 포맷을 따르지 않음 |
| **FastAPI** | Dashboard의 얇은 백엔드 프레임워크. 정적 JSON 서빙 + 최소 API만 담당 |

## Git/이슈 운영

| 용어 | 정의 |
|---|---|
| **Conventional Commits** | `<type>(<module>): <설명>` 형식의 커밋 메시지 규칙. `docs/contracts/pr_schema.md` 참고 |
| **CODEOWNERS** | 특정 경로 변경 시 자동으로 리뷰어를 지정하는 GitHub 기능. 현재 `.github/CODEOWNERS`는 역할명 placeholder 상태 |
| **Epic / 하위 이슈** | Epic은 모듈 단위 큰 목표(`docs/epics/`), 하위 이슈는 그 안의 실행 단위 작업. 스키마는 `docs/contracts/epic_schema.md`, `docs/contracts/subissue_schema.md` |

## 초보자용 배경 설명이 필요하면

용어의 배경(왜 중요한지, 실제 공격 사례 등)은 `study_week1/README.md` §1~3, `study_week1/architecture.html`을 참고하세요. 이 문서는 "정의"만, 그쪽은 "왜/사례"까지 다룹니다.


# ============================================================
# 원본: docs/contracts/epic_schema.md
# ============================================================

# 상위 이슈(Epic) 공통 스키마

`docs/epics/*.md`는 전부 이 스키마를 따릅니다. 총괄(PM)이 새 상위 이슈를 추가하거나, 기존 이슈를 GitHub Issue로 옮길 때 이 구조를 그대로 씁니다.

## 필수 섹션 (순서 고정)

```markdown
# [Epic] <모듈명 또는 결정 대상> <동사형 제목>

## 목표
(1~3문장. 이 이슈가 끝나면 시스템 관점에서 무엇이 가능해지는지 — 개별 작업이 아니라 "왜 이 모듈이 존재하는지"를 씀. 이 산출물을 누가 입력으로 소비하는지 명시)

## 범위
- (포함되는 작업을 불릿으로. 각 항목은 하나의 하위 이슈로 쪼개질 수 있는 크기)

**범위 밖**: (명시적으로 제외한다고 선언. "그냥 안 적음"과 "일부러 뺌"을 구분하기 위해 필수)

## 완료조건 (Acceptance Criteria)
- [ ] (사람이 아니라 AI 구현체가 봐도 참/거짓을 판정할 수 있는 문장. "잘 동작한다" 금지, "임의의 X를 넣으면 Y가 나온다" 형태로)

## 입력/출력 인터페이스
(관련 `schemas/*.schema.json` 파일명을 명시하고 핵심 필드만 요약. 전체 스키마는 링크로 대체하고 여기서 재정의하지 않음 — 스키마 파일이 단일 진실 공급원(SSOT))

## 참고자료
(`docs/design/`, `study_week1/`, `resources/curated_list.md` 등 실제 존재하는 경로만. 만들 예정인 문서는 넣지 않음)

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
```

## 필드 규칙

| 필드 | 규칙 |
|---|---|
| 제목 | `[Epic] ` 접두사 고정. GitHub Issue 생성 시 라벨 `epic` + 모듈 라벨(`module:collector` 등) 동시 부여 |
| 완료조건 | 최소 3개, 각 항목은 실행 가능한 검증(테스트 커맨드·입출력 예시)으로 연결 가능해야 함 |
| 범위 밖 | 비워두지 않음. 없으면 "현재 없음"이라고 명시 |
| 입력/출력 인터페이스 | `schemas/`의 실제 파일명을 반드시 인용. 필드를 여기서 새로 정의하지 않고 스키마 파일을 고침 |
| 하위 이슈 섹션 | 문구를 임의로 바꾸지 않음 — 담당자 본인이 하위 이슈를 만들기 전까지 이 placeholder를 유지 |

## GitHub Issue로 옮길 때

- 라벨: `epic`, `module:<모듈명>` (collector/risk-analyzer/ml-detector/attack-path/dashboard/pm)
- 마일스톤: `GIT_POLICY.md` §5 마일스톤 표(M1~M8) 중 해당 구간
- Assignee: CODEOWNERS 상 해당 모듈 담당자


# ============================================================
# 원본: docs/contracts/subissue_schema.md
# ============================================================

# 하위 이슈(Sub-issue) 공통 스키마

**하위 이슈는 각 담당자가 직접 만듭니다 (총괄이 대신 만들지 않음).** 다만 AI가 그대로 구현할 수 있을 만큼 구체적이어야 하므로, 아래 스키마를 담당자 전원이 동일하게 따릅니다. `docs/epics/*.md`의 "범위" 항목 하나가 보통 하위 이슈 1~3개로 쪼개집니다.

## 필수 섹션 (순서 고정)

```markdown
# [<모듈>] <구체적 작업 — 동사로 끝나는 한 문장>

## 상위 이슈
Relates to #<epic 번호>

## 작업 내용
(어떤 파일/함수/클래스를 만들거나 고치는지 구체적으로. "파서 구현" 대신
"`collector/parsers/requirements_txt.py`에 `parse(path: str) -> list[Dependency]` 구현" 수준)

## 입력/출력 예시
(최소 1개의 구체적인 입력값 → 출력값 쌍. 표나 JSON 스니펫으로.
관련 있으면 `schemas/*.schema.json`의 어느 필드를 채우는지 명시)

## 완료조건 (Acceptance Criteria)
- [ ] (테스트 가능한 조건. 가능하면 실제 테스트 케이스 이름/커맨드까지)

## 엣지케이스
(비어있는 입력, 존재하지 않는 패키지, 네트워크 실패 등 — 표로 "상황 → 기대 동작")

## 참고자료
(해당 모듈 `docs/design/0X-*.md`의 관련 절 번호, study_week1 자료)
```

## 필드 규칙

| 필드 | 규칙 |
|---|---|
| 제목 | `[<모듈명>]` 접두사. 브랜치명은 `GIT_POLICY.md` 규칙대로 `<모듈>/<이슈번호>-<설명>` |
| 작업 내용 | 파일 경로와 함수 시그니처까지 — AI 구현체가 "어디에 뭘 만들지" 추측하지 않게 |
| 입력/출력 예시 | 산문 설명만으로 끝내지 않음. 실제 값 예시 필수 (사람이 봐도, AI가 봐도 모호하지 않게) |
| 엣지케이스 | 최소 2개. 설계 문서의 "3. 에러 처리 원칙"(`01-collector.md` 등)에 이미 정의된 원칙을 재확인 |
| 크기 | 하위 이슈 하나가 리뷰 가능한 PR 1개 분량을 넘지 않도록 쪼갬 (기준: 파일 1~3개, 리뷰 시간 30분 이내) |

## GitHub Issue로 옮길 때

- 라벨: `module:<모듈명>`, 크기 라벨(`size:S`/`size:M`/`size:L`)
- `Depends on #`으로 선행 이슈 명시 (병렬 작업 시 충돌 방지)
- 상위 Epic 이슈에 체크리스트 항목으로 연결 (GitHub의 tasklist 문법 사용 가능)


# ============================================================
# 원본: docs/contracts/pr_schema.md
# ============================================================

# Pull Request 공통 스키마

`.github/PULL_REQUEST_TEMPLATE.md`가 실제로 GitHub에서 채워지는 양식이고, 이 문서는 그 각 필드가 왜 필요하고 무엇을 채워야 "충분한지"를 정의하는 계약입니다. AI가 구현한 PR도 예외 없이 이 기준을 만족해야 리뷰 가능한 것으로 간주합니다.

## 필드별 요구사항

| 필드 | 최소 요구사항 |
|---|---|
| 변경 내용 | 무엇을 바꿨는지 불릿 3개 이내. "리팩터링" 같은 추상적 표현 금지 — 어떤 파일의 어떤 동작이 바뀌었는지 |
| 관련 이슈 | `Closes #<하위 이슈 번호>` 필수. 이슈 없는 PR은 반려 (범위가 불명확한 작업이라는 뜻) |
| 스키마 변경 여부 | `schemas/*.json`을 건드렸으면 체크 후 CODEOWNERS 대상 담당자 리뷰 승인이 머지 조건 (`GIT_POLICY.md` §3) |
| 테스트 방법 | 실행한 커맨드 + 실제 출력(또는 스크린샷). "잘 됩니다" 금지 — `pytest tests/test_x.py -v` 결과 붙여넣기 수준 |
| 체크리스트 | 로컬 동작 확인 + 문서 업데이트 여부. 둘 다 체크 안 되어 있으면 머지 보류 |

## 커밋 메시지 규칙 (Conventional Commits, `GIT_POLICY.md` §4 재확인)

```
<type>(<module>): <설명>

[선택: 본문]

Closes #<이슈번호>
```

- `type`: `feat` / `fix` / `docs` / `refactor` / `test` / `chore`
- `module`: `collector` / `risk-analyzer` / `ml-detector` / `attack-path` / `dashboard` / `schemas` / `pipeline`
- 하나의 커밋은 하나의 하위 이슈에 대응 (여러 이슈를 한 커밋에 묶지 않음)

## 머지 조건

1. 체크리스트 전항목 체크
2. `schemas/` 변경 시 CODEOWNERS 승인
3. CI(추후 `.github/workflows/` 추가 시) 통과
4. 최소 1인 리뷰 승인 (2인 이하 소규모 모듈은 총괄이 대신 리뷰 가능)


# ============================================================
# 원본: docs/design/00-overall.md
# ============================================================

# AASM 전체 설계 문서 (00 — Overall)

담당: PM/총괄 · 최종 수정: 2026-09-06

## 1. 저장소 구조 근거

`GIT_POLICY.md`가 이미 모노레포 구조(`collector/ risk-analyzer/ ml-detector/ attack-path/ dashboard/ schemas/ docs/`)를 확정했습니다. 4인 학부 프로젝트에서 멀티레포는 버전 동기화·CI 중복 설정 비용이 이득보다 큽니다. 여기에 다음을 추가 제안합니다.

```
aasm/
├── pipeline/            # ⭐ 신규 제안: 모듈을 순서대로 실행하는 오케스트레이터
├── collector/
├── risk-analyzer/
├── ml-detector/
├── attack-path/
├── dashboard/
├── schemas/
├── data/                # ⭐ 신규 제안: 단계별 중간 산출물(JSON) 저장소, .gitignore 처리
└── docs/
```

`pipeline/`과 `data/`가 architecture.html에는 명시되지 않았지만, 실제로 팀이 코드를 짜기 시작하면 "누가 다음 모듈을 호출하는가"가 반드시 필요합니다. Syft→Grype 같은 실제 SCA 도구 체인도 "이전 단계가 JSON 파일을 만들고 다음 단계가 그 파일을 읽는" 방식으로 동작합니다(파일 기반 핸드오프가 업계에서도 검증된 패턴). 우리도 동일한 방식을 채택합니다.

## 2. 오케스트레이션: 파일 기반 핸드오프 + 얇은 CLI

**결론: 공유 DB나 메시지 큐 대신, `schemas/`로 형식이 고정된 JSON 파일을 로컬 디스크에 순서대로 쌓는 방식 + 이를 순서대로 호출하는 얇은 Python CLI(`pipeline/run.py`)를 둡니다.**

이유:
- 학부 4인 프로젝트에 DB/큐 인프라는 과설계입니다. Collector→(Risk Analyzer, ML 병렬)→Attack Path→Dashboard는 선형+한 번의 fan-out/fan-in 구조뿐이라 파일 핸드오프로 충분합니다.
- 각 모듈은 독립 실행 가능해야 합니다(모듈 담당자가 자기 모듈만 테스트할 때 다른 모듈이 안 떠 있어도 됨) → "함수를 직접 import해서 호출"이 아니라 "표준 입출력 JSON 파일"을 계약으로 삼습니다.
- `pipeline/run.py`는 각 모듈을 서브프로세스(또는 함수 호출)로 실행하고, 모듈 간 데이터는 `data/<run_id>/collector_output.json` 형태로 저장합니다. 대략:

```
1. collector.main(repo_path)         -> data/<run_id>/collector_output.json
2. (병렬) risk_analyzer.main(...)    -> data/<run_id>/risk_score.json
          ml_detector.main(...)     -> data/<run_id>/ml_result.json
3. attack_path.main(risk_score.json, ml_result.json) -> data/<run_id>/attack_graph.json
4. dashboard가 attack_graph.json을 읽어 웹으로 렌더링
```

- 3단계는 2단계 두 산출물이 **모두** 끝나야 시작 가능(fan-in) — `pipeline/run.py`가 이 대기 로직을 담당합니다. 각 모듈은 서로의 존재를 몰라도 되고, `pipeline/`만 이 순서를 압니다.
- 클라우드 환경(AWS EC2)에서는 이 CLI를 cron 또는 수동 트리거로 실행하는 것으로 충분하며, 마이크로서비스화는 이번 학기 범위 밖입니다.

## 3. `schemas/` 4개 파일의 역할 (상세 스펙은 각 담당자가 작성)

- `collector_output.schema.json` — Collector 산출물. SBOM(CycloneDX 준용) + 의존성 목록 + 탐지된 MCP/외부 연동 도구 리스트를 담는 최상위 구조. Risk Analyzer/ML의 입력.
- `risk_score.schema.json` — 패키지별 위험 점수(CVSS 참고), 타이포스쿼팅 등 정적 필터링 플래그. Attack Path Engine 입력의 절반.
- `ml_result.schema.json` — 패키지별 이상탐지 스코어/라벨. Attack Path Engine 입력의 나머지 절반.
- `attack_graph.schema.json` — 노드(의존성/에이전트/권한)와 엣지(연결)로 구성된 그래프. Dashboard 입력.

각 스키마는 최소 `run_id`, `generated_at`, `source_module`, `schema_version` 공통 메타 필드를 갖도록 통일할 것을 제안합니다. 상세 필드는 module owner가 정의하되, `schemas/` 변경은 GIT_POLICY.md의 CODEOWNERS 규칙(만드는 사람+받는 사람 전원 승인)을 그대로 따릅니다.

## 4. 프로젝트 공통 컨벤션

- **언어/런타임**: Python 3.11+ 통일(Collector/Risk Analyzer/ML 모두 Python 생태계 도구 사용 전제). Dashboard만 JS(Node 20+).
- **의존성 관리**: 모듈별 `requirements.txt` 또는 `pyproject.toml` 개별 관리(모노레포 안에서도 모듈 독립성 유지).
- **로깅**: 표준 `logging` 모듈, 포맷 `%(asctime)s [%(levelname)s] %(name)s: %(message)s`, 모듈명은 폴더명과 동일하게(`collector`, `risk_analyzer` 등)로 통일해 나중에 로그를 합쳐 봐도 출처가 바로 보이게 합니다.
- **설정 관리**: 모듈 루트에 `config.yaml` 또는 `.env`(민감정보용), 하드코딩 금지. API 키(PyPI는 불필요하지만 향후 OSV rate limit 등 대비)는 `.env` + `.gitignore`.
- **테스트**: 각 모듈 `tests/` 폴더, `pytest` 통일. 최소 기준: 스키마 검증 테스트(자기 모듈 출력이 `schemas/*.schema.json`을 통과하는지) 1개는 필수 — 이게 사실상 우리 프로젝트의 "통합 테스트" 역할을 대신합니다.
- **CI**: GitHub Actions로 PR마다 `pytest` + 스키마 검증 실행 권장(4인 규모라 최소한으로 시작, M3 즈음 도입).

## 5. 이번 검토에서 확인한 리스크

CNAPP류 상용 도구는 보통 이 오케스트레이션 계층을 명시적인 컴포넌트로 갖고 있는데(Syft→Grype 파이프라인처럼 파일 기반 핸드오프가 실제로 검증된 패턴), 우리 architecture.html에는 이 계층이 그림에 드러나 있지 않아 이번 문서에서 `pipeline/`으로 명시했습니다. M2(설계) 마일스톤에서 이 문서를 팀 전체가 리뷰하고 확정하는 것을 제안합니다.


# ============================================================
# 원본: docs/design/01-collector.md
# ============================================================

# 기술 설계 문서 — Dependency Collector (`collector/`)

> 관련 자료: `study_week1/README.md` §5, `architecture.html` #collector, `GIT_POLICY.md` §3(스키마 계약)

## 1. 모듈 구조 (제안)

```
collector/
├── cli.py                     # 진입점 (python -m collector --repo <path|url>)
├── config.py                  # 타임아웃, 캐시 경로, 요청 간격(rate limit) 등 설정값
├── errors.py                  # 공통 예외 클래스 + 에러 코드 enum
├── parsers/
│   ├── manifest_parser.py     # requirements.txt/pyproject.toml/Pipfile → requirements-parser, dparse
│   ├── import_scanner.py      # pipreqs 래퍼 + --diff 로직
│   ├── dockerfile_parser.py   # Dockerfile FROM/RUN pip install/COPY 추출 (dockerfile-parse 라이브러리)
│   └── integration_detector.py # LangChain/MCP 탐지 (import AST 스캔 + mcp.json류 설정파일 탐색)
├── pypi_client.py             # PyPI JSON API 클라이언트 (ETag 캐시, 재시도/백오프)
├── vuln_client.py             # OSV 배치 쿼리 (PyPI 응답에 취약점 정보가 없을 때 보완)
├── sbom_generator.py          # cyclonedx-py 서브프로세스 호출 래퍼
├── merger.py                  # 파서별 결과 병합·중복 제거 → 최종 스키마 조립
├── output_writer.py           # schemas/collector_output.schema.json으로 검증 후 파일 출력
└── tests/
```

## 2. 실행 순서

1. **저장소 확보/검증** — 로컬 경로 또는 git URL. 접근 불가(비공개/삭제/인증필요)면 초기 단계에서 즉시 `status: "failed"`로 중단(뒤 단계 낭비 방지).
2. **매니페스트 파싱** — requirements.txt / pyproject.toml / Pipfile / package.json을 찾아 `requirements-parser`, `dparse`로 파싱. 없으면 건너뛰고 3번에 전적으로 의존.
3. **임포트 스캔** — `pipreqs`로 실제 import 스캔, 매니페스트 결과와 `--diff` 비교 → "선언됨/실제사용/양쪽" 태그를 붙여 후보 의존성 목록 확정.
4. **Dockerfile 파싱** (있는 경우) — `FROM` 베이스 이미지, `RUN pip install ...`, `COPY requirements*.txt` 패턴을 `dockerfile-parse`로 추출해 후보 목록에 합침. 베이스 이미지의 OS 패키지(apt 등)는 이번 스코프에서는 이름만 기록하고 PyPI 매칭은 하지 않음.
5. **외부 연동 탐지** — import 구문에서 `langchain`, `langchain_mcp_adapters`, `mcp` 패턴 매칭 + 저장소 내 `mcp.json`/`claude_desktop_config.json` 류 설정 파일 탐색으로 로컬/원격 MCP 서버, LangChain 내장 툴을 식별.
6. **PyPI 메타데이터 조회** — 확정된 패키지마다 `GET /pypi/<name>/json` 호출. ETag 캐시 사용, 클라이언트 자체 요청 간격 제한(기본 5 req/s 토큰버킷 — PyPI는 공식적으로 하드 레이트리밋은 없지만 예의상 자체 제한). `vulnerabilities` 필드 우선 사용.
7. **취약점 보완 조회** — PyPI 응답에 `vulnerabilities`가 비어있는 패키지만 모아 OSV `/v1/querybatch`로 보완 조회.
8. **SBOM 생성** — `cyclonedx-py requirements`(또는 environment/poetry)로 CycloneDX JSON 생성. 실패 시 경고만 남기고 dependency_list는 그대로 출력(SBOM 없이도 부분 결과 제공).
9. **병합·검증·출력** — 전체 결과를 `schemas/collector_output.schema.json`에 맞춰 조립, 로컬 검증 후 저장.

## 3. 에러 처리 원칙

- 모든 에러는 `{stage, code, message, package?}` 구조로 `errors[]` 배열에 누적 — 하나 실패해도 파이프라인 전체를 죽이지 않음(예외: 1단계 저장소 접근 실패는 즉시 중단).
- 대표 에러 코드: `REPO_UNREACHABLE`, `REPO_PRIVATE_AUTH_REQUIRED`, `MANIFEST_PARSE_FAILED`(스킵), `IMPORT_SCAN_FAILED`(스킵), `PYPI_NOT_FOUND`(패키지 `resolution_status: "unresolved"`로 표시 후 계속), `PYPI_RATE_LIMIT_OR_5XX`(지수 백오프 최대 3회 후 unresolved), `SBOM_GENERATION_FAILED`(스킵).
- 최종 `status`는 `success`(에러 없음) / `partial`(일부 스킵) / `failed`(치명적 중단) 3단계.

## 4. 출력 스키마 초안 (`schemas/collector_output.schema.json`)

```json
{
  "schema_version": "0.1.0",
  "scan_id": "uuid",
  "repo": { "url": "https://github.com/org/agent-repo", "commit_sha": "abc123", "scanned_at": "2026-09-06T12:00:00Z" },
  "status": "partial",
  "dependencies": [
    {
      "name": "langchain",
      "version": "0.3.5",
      "ecosystem": "pypi",
      "source": ["manifest", "import"],
      "declared_in": ["requirements.txt"],
      "resolution_status": "resolved",
      "pypi": {
        "latest_version": "0.3.7",
        "summary": "Building applications with LLMs",
        "license": "MIT",
        "home_page": "https://langchain.com",
        "last_release_at": "2026-08-01T00:00:00Z"
      },
      "hashes": [{ "algo": "sha256", "value": "..." }],
      "distribution_files": [
        { "filename": "langchain-0.3.5-py3-none-any.whl", "url": "https://files.pythonhosted.org/.../langchain-0.3.5-py3-none-any.whl", "hashes": [{ "algo": "sha256", "value": "..." }] }
      ],
      "vulnerabilities": [
        { "id": "GHSA-xxxx", "aliases": ["CVE-2026-0001"], "severity": "HIGH", "cvss_base_score": 8.1, "cvss_source": "nvd", "fixed_versions": ["0.3.6"], "osv_url": "https://osv.dev/vulnerability/GHSA-xxxx" }
      ],
      "maintainers": {
        "maintainer_count": 3,
        "data_status": "ok",
        "maintainer_accounts": [
          { "username": "example", "account_created_at": null, "data_status": "not_collected" }
        ]
      },
      "external_integrations": ["network", "shell"]
    }
  ],
  "integrations": [
    { "type": "mcp_remote", "name": "filesystem-server", "detected_in": "config/mcp.json", "transport": "http_sse" },
    { "type": "langchain_builtin_tool", "name": "SerpAPIWrapper", "detected_in": "agent.py" }
  ],
  "sbom": { "format": "CycloneDX", "spec_version": "1.6", "generator": "cyclonedx-py", "file_ref": "sbom.json" },
  "errors": [
    { "stage": "pypi_client", "code": "PYPI_NOT_FOUND", "message": "package 'internal-tool' not found on PyPI", "package": "internal-tool" }
  ],
  "summary": { "total_dependencies": 42, "resolved": 40, "unresolved": 2, "vulnerable_count": 3, "integrations_count": 2 }
}
```

이 문서는 DRAFT이며, `GIT_POLICY.md` 규칙에 따라 `schemas/collector_output.schema.json`으로 확정하려면 Risk Analyzer·ML 담당자 승인이 필요합니다.

## 확정 사항 (교차검토 반영)

1. **`cvss_base_score` 인라인 제공 (Risk Analyzer Q1)** — 예. OSV 응답의 `severity`(CVSS 벡터)를 파싱해 `cvss_base_score`(숫자) + `cvss_source`(`nvd`/`osv` 등)로 `vulnerabilities[]`에 직접 포함합니다. 파싱 불가 시 `cvss_base_score: null`.
2. **`external_integrations[]` 필드 추가 (Risk Analyzer Q2)** — 예. 5단계 외부 연동 탐지 결과를 패키지 단위로도 태깅해 각 dependency에 `external_integrations: ["network"|"shell"|"mcp"|"filesystem"]` 배열을 추가합니다. (기존 top-level `integrations[]`는 유지, 이건 패키지-연동 매핑용.)
3. **`latest_release_date`/`maintainer_count` 항상 존재 보장 (Risk Analyzer Q3)** — 완전 보장은 불가(PyPI가 일부 패키지에 정보 미제공). 대신 필드를 항상 present로 두되 값이 없으면 `null` + `data_status: "not_available"`을 명시해 staleness score 계산 시 결측을 구분할 수 있게 합니다.
4. **배포 파일 경로/해시 포함 (ML Q4)** — 예. `distribution_files[]`에 sdist/wheel 파일명, 다운로드 URL, sha256 해시를 포함합니다(정적 분석 시 실제 파일 매칭용).
5. **maintainer 계정 생성일 수집 (ML Q5)** — 기본 미수집(No). PyPI JSON API가 계정 생성일을 제공하지 않아 유저 페이지 추가 스크래핑이 필요하고 요청량이 커집니다. 대신 스키마에 `maintainer_accounts[].account_created_at`을 `null` + `data_status: "not_collected"`로 예약해두어, 추후 필요성이 확정되면 별도 수집기를 붙일 수 있게 합니다. (이견 있으면 논의 환영)


# ============================================================
# 원본: docs/design/02-risk-analyzer.md
# ============================================================

# Risk Analyzer 기술 설계 문서

> 담당: 위험분석 · 관련: `study_week1/architecture.html`(패키지 위험도 × 에이전트 권한), `study_week1/README.md`(CVE/CVSS/타이포스쿼팅 용어), `resources/curated_list.md` F(타이포스쿼팅)·W(EPSS/CVSS/NVD)

## 1. 배경 및 설계 목표

기존 학습자료는 "CVSS 참고", "패키지 위험도 × 에이전트 권한"이라는 **개념**만 제시하고 구체적 산식이 없다. 이 문서는 그 공백을 메우기 위한 실제 스코어링 알고리즘을 정의한다.

리서치 결과 두 가지를 반영했다:
- **타이포스쿼팅 임계값**: 실제 도구(anti-typosquatting류)는 인기 패키지 top-N(보통 top 10,000) 대비 Levenshtein distance ≤ 2를 기본 임계값으로 쓴다 — 과거 40건 타이포스쿼팅 사례 중 18건이 거리 2 이하였다는 근거. 단, 단순 거리 임계값만 쓰면 오탐이 많다는 지적이 있어 낮은 다운로드 수·최근 등록일 같은 보조 신호와 AND 조건으로 묶는다.
- **CVSS × EPSS 결합 주의점**: "CVSS 점수 × EPSS 확률"처럼 서수(ordinal)와 확률을 곱하는 단순 결합은 통계적으로 부적절하다는 지적이 있음(Cloudsmith/Intruder 자료). 대신 정규화(0~1) 후 가중합(weighted sum)으로 결합하고, EPSS는 "실제 악용 확률"이라는 별도 축으로 취급한다.

## 2. 스코어링 알고리즘

### 2.1 패키지 자체 위험도 (`package_risk`, 0~1)

```
package_risk = w1 * cvss_norm
             + w2 * epss_score
             + w3 * typo_flag
             + w4 * staleness_score

기본 가중치: w1=0.35, w2=0.30, w3=0.20, w4=0.15  (합 1.0, 조정 가능한 설정값)
```

- `cvss_norm = max(CVSS_base_score) / 10.0` — 패키지에 걸린 알려진 CVE 중 최고 심각도. CVE 없으면 0.
- `epss_score` — NVD/FIRST EPSS API 값(0~1) 그대로 사용. 여러 CVE가 있으면 최댓값.
- `typo_flag` (0/0.5/1 단계형) — 아래 2.2 알고리즘 결과.
- `staleness_score` — 아래 2.3 알고리즘 결과.

CVE가 전혀 없는 패키지도 typo_flag·staleness만으로 위험 신호를 낼 수 있게 설계(무CVE ≠ 무위험, xz-utils 사례 참고).

### 2.2 타이포스쿼팅 탐지 (`typo_flag`)

1. PyPI 인기 패키지 top-5,000 리스트(예: PyPI 다운로드 통계 기반)를 사전에 확보.
2. 대상 패키지명과 top-5,000 각 이름 사이 Levenshtein distance 계산(`python-Levenshtein` 등).
3. 최소 거리 `d_min`에 대해:
   - `d_min == 0` (정상 등록된 유명 패키지) → `typo_flag = 0`
   - `1 <= d_min <= 2` **AND** (다운로드 수 하위 or 등록 6개월 이내) → `typo_flag = 1` (고위험)
   - `d_min <= 2`이지만 보조 신호 없음 → `typo_flag = 0.5` (주의, 오탐 가능성 고려)
   - `d_min > 2` → `typo_flag = 0`
4. 대체/문자 치환형(`l`↔`1`, `rn`↔`m` 등 combosquatting) 패턴은 v2에서 정규식 규칙 추가 예정(범위 밖 명시).

### 2.3 유지보수 상태 (`staleness_score`, 0~1)

```
months_since_last_release = (오늘 - last_release_date) / 30
staleness_score = min(1.0, months_since_last_release / 24)   # 24개월 이상 방치 시 1.0

maintainer_count == 1 이면 +0.2 (최대 1.0로 클램프)
```

### 2.4 에이전트 권한 가중치 (`permission_weight`, 1.0~3.0)

Attack Path Engine이 최종 그래프 단계에서 권한을 다루지만, Risk Analyzer는 **패키지가 호출되는 컨텍스트의 권한 등급**만 단순 곱셈 승수로 반영한다(상세 그래프 분석은 하지 않음).

| 권한 등급 | 예시 | weight |
|---|---|---|
| LOW | 순수 계산/포매팅 라이브러리 | 1.0 |
| MEDIUM | 파일시스템 읽기, 네트워크 호출 도구 | 1.8 |
| HIGH | 쉘 실행, API 키/시크릿 접근, 외부 MCP 서버 연동 | 3.0 |

권한 등급은 Collector가 산출한 `external_integrations`(MCP/도구 연동 목록)에서 도출하거나, 없으면 기본값 MEDIUM(1.8) 적용. **(교차검토 반영, Q6)** 권한 목록 자체의 정식 스키마·소유권은 Attack Path Engine이 가지며, Risk Analyzer는 그 스키마를 참조(consume)해 `permission_weight`만 계산한다. `permission_source: "attack_path_engine"`로 입력 출처를 명시한다 (아래 §5 출력 스키마 참고).

### 2.5 최종 위험 점수

```
risk_score = round(package_risk * permission_weight, 3)   # 이론상 0 ~ 3.0
risk_level = LOW (<1.0) / MEDIUM (1.0~2.0) / HIGH (>2.0)
```

## 3. 파일 구조 (`risk-analyzer/`)

```
risk-analyzer/
├── __init__.py
├── main.py                  # 진입점: collector 출력 로드 → 점수화 → risk_score.json 출력
├── config.py                 # 가중치(w1~w4), 임계값, permission_weight 표
├── scorers/
│   ├── cvss_epss.py          # NVD/EPSS API 조회 + 정규화
│   ├── typosquatting.py      # Levenshtein 기반 유사도 탐지
│   ├── staleness.py           # PyPI 메타데이터 기반 유지보수 신호
│   └── permission.py          # 권한 등급 매핑
├── data/
│   └── top_packages.json      # 인기 패키지 top-5000 이름 목록(사전 다운로드)
└── tests/
    └── test_scorers.py
```

## 4. Collector 스키마에 요청하는 INPUT 필드

`schemas/collector_output.schema.json`에 아래 필드가 **반드시** 있어야 함:

- `package.name`, `package.ecosystem` (예: "pypi") — 필수
- `package.version` — CVE 버전 매칭용, 필수
- `package.latest_release_date` (ISO8601) — staleness 계산용
- `package.maintainer_count` (int) — staleness 보정용
- `package.vulnerabilities[]` — 각 항목에 `cve_id`, `cvss_base_score` (Collector가 PyPI JSON API의 `vulnerabilities` 필드에서 이미 수집 가능)
- `package.osv_ids[]` — EPSS 조회 시 CVE ID로 매핑 안 되는 경우 대비
- `external_integrations[]` — 이 패키지가 사용되는 컨텍스트(예: "shell_exec", "network", "mcp_server") — 권한 가중치 산정에 필수. **현재 Collector 산출물에 없다면 신규 요청 필요.**

## 5. 출력 스키마 초안 (`schemas/risk_score.schema.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RiskScoreOutput",
  "type": "object",
  "required": ["generated_at", "packages"],
  "properties": {
    "generated_at": { "type": "string", "format": "date-time" },
    "packages": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "version", "ecosystem", "package_risk", "permission_weight", "permission_source", "risk_score", "risk_level", "signals"],
        "properties": {
          "name": { "type": "string" },
          "version": { "type": "string" },
          "ecosystem": { "type": "string" },
          "package_risk": { "type": "number", "minimum": 0, "maximum": 1 },
          "permission_weight": { "type": "number", "minimum": 1.0, "maximum": 3.0 },
          "permission_source": {
            "type": "string",
            "description": "권한 등급 산정에 쓰인 권한 데이터의 출처. Risk Analyzer는 권한 목록을 직접 생성하지 않고 Attack Path Engine 소유 스키마를 참조한다(Q6 결정).",
            "enum": ["attack_path_engine", "default_medium_fallback"]
          },
          "risk_score": { "type": "number", "minimum": 0, "description": "숫자형 원점수(0~3.0). Dashboard 등 정렬/시각화용." },
          "risk_level": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH"], "description": "risk_score를 사람이 읽기 쉬운 등급으로 변환. Attack Path Engine 그래프 노드 라벨/색상용." },
          "signals": {
            "type": "object",
            "properties": {
              "cvss_norm": { "type": "number" },
              "cve_ids": {
                "type": "array",
                "items": { "type": "string" },
                "description": "cvss_norm 계산에 쓰인 원본 CVE ID 목록 (Q8 결정: 정규화값 + 원본 목록 둘 다 포함, Dashboard의 attributes.cve 표시 요구사항(질문 13) 지원)"
              },
              "epss_score": { "type": "number" },
              "typo_flag": { "type": "number", "enum": [0, 0.5, 1] },
              "typo_nearest_match": { "type": ["string", "null"] },
              "staleness_score": { "type": "number" },
              "months_since_last_release": { "type": "number" }
            }
          }
        }
      }
    }
  }
}
```

이 스키마는 Attack Path Engine 담당의 리뷰가 필요하다(GIT_POLICY.md의 CODEOWNERS 규칙: `@위험분석담당 @공격경로담당`). 특히 `signals` 세부 필드가 그래프 노드 속성으로 그대로 쓰기 충분한지 확인 요청.

## 확정 사항 (교차검토 반영)

**Q6. 권한(Permission) 데이터 출처 → (c) Attack Path Engine이 정의·소유, Risk Analyzer는 참조(consume)만.**
Risk Analyzer의 `permission_weight`는 이미 권한 등급(LOW/MEDIUM/HIGH)을 **입력**으로 쓰는 소비자이지, 권한 목록(타입+대상 자산)의 원 출처가 아니다. 반대로 Attack Path Engine은 그래프 엣지(에이전트→자산 접근)를 만들기 위해 권한 데이터를 어차피 구조화해야 하므로, 스키마 소유권을 그쪽에 두고 Risk Analyzer·Collector는 그 스키마를 참조해 자기 필드에 매핑하는 것이 이중 정의를 막는다. 위 §2.4에 `permission_source` 필드를 추가해 출처를 명시했다.

**Q7. `is_externally_reachable` → Attack Path Engine이 직접 판단.**
이 값은 네트워크/그래프 위상(다른 노드와의 연결 관계)에 의존하는데, Risk Analyzer는 패키지 단위 정적 신호만 다루고 그래프 전체 구조를 보지 않는다. Risk Analyzer가 억지로 계산하면 그래프 구축 시점의 실제 연결 정보와 어긋날 위험이 있다.

**Q8. `signals` 서브 오브젝트 + 원본 CVE 목록 → 둘 다 포함.**
`cvss_norm`만으로는 Dashboard가 요구하는 "CVE 목록" 속성(질문 13)을 만들 수 없으므로 `signals.cve_ids[]`를 추가했다. 그래프 노드에는 `cvss_norm`(정렬/색상용)과 `cve_ids`(사람이 읽는 상세정보용)를 함께 붙인다.

**Q9. `risk_level` vs `risk_score` → 둘 다 유지(기존 설계 그대로).**
원래 스키마에 이미 `risk_score`(숫자, 정렬·임계값 비교용)와 `risk_level`(등급, 시각화·룰 분기용)이 모두 있었다. 별도 변경 불필요, 문서에 각 필드의 용도만 명시적으로 추가했다.


# ============================================================
# 원본: docs/design/03-ml-detector.md
# ============================================================

# ML 이상탐지 (ml-detector) 기술 설계 문서

담당: ML탐지 · 관련 스키마: `schemas/ml_result.schema.json` (Attack Path Engine 담당 리뷰 필요)

## 1. 목적

Risk Analyzer는 "알려진 패턴"(타이포스쿼팅 이름 유사도, 알려진 CVE)만 규칙으로 잡는다. `ml-detector`는 Collector가 만든 SBOM/메타데이터에서 **정상/악성 패키지의 통계적 특징 차이**를 학습한 분류기로, 아직 DB에 없는 신규·변종 악성 패키지(예: xz-utils처럼 신뢰를 쌓은 뒤 배신하는 유형은 못 잡더라도, 다수의 자동화된 악성 패키지는 잡는 것을 목표)를 탐지한다.

## 2. Feature 목록 (출처별)

| 범주 | Feature | 출처 |
|---|---|---|
| 메타데이터 | package age(첫 배포일로부터 경과일), 최근 업데이트 후 경과일, 버전 개수, maintainer 수, maintainer 계정 생성일 | PyPI JSON API `info`/`releases` |
| 메타데이터 | download count(있으면), 스타 수/포크 수(연결된 GitHub repo가 있을 때) | PyPI stats(BigQuery) 또는 pypistats.org, GitHub API |
| 설명/텍스트 | description 길이, README 존재 여부, description-코드 불일치(설명은 평범한데 코드가 난독화됨), 키워드 플래그(`eval`, `exec`, `base64`, `subprocess`, `os.system`, `socket`, `urllib.request`, `pickle.loads` 등 등장 횟수) | 배포 파일(sdist/wheel) 내 소스 정적 스캔 |
| 설치 동작 | `setup.py`/`pyproject.toml` 내 install-time 실행 코드 유무(`setup.py` custom `cmdclass`, post-install hook), 네트워크 호출 코드 존재 여부 | 배포 파일 파싱 |
| 코드 특성 | 코드 엔트로피(문자열/블록 단위 Shannon entropy — 난독화·base64 페이로드 탐지용), 파일 크기 대비 문자열 상수 비율, 이진 파일(barary blob) 포함 여부 | 배포 파일 정적 분석 |
| 이름 유사도 | 인기 패키지와의 편집 거리(Levenshtein) 최소값 — Risk Analyzer의 규칙과 겹치지만 ML 피처로도 포함해 상호보완 | 상위 N개 PyPI 패키지 목록 대비 계산 |
| 의존성 그래프 | 선언된 의존성 수, 의존성 중 신규/저평판 패키지 비율 | Collector SBOM |

참고 논문 [arXiv:2412.05259](https://arxiv.org/pdf/2412.05259)의 텍스트/파일/코드/메타데이터 4대 특징군 구성을 그대로 채택했다.

## 3. 학습 데이터셋 (실존, 접근 가능 확인됨)

- **악성 샘플 — DataDog `malicious-software-packages-dataset`**(GitHub, `DataDog/malicious-software-packages-dataset`): 사람이 전수 검증한 28,000+ 건의 실제 악성 PyPI/npm/기타 패키지. `samples/` 폴더에 생태계별로 정리되어 있고 지속적으로 업데이트됨. 1차 학습 데이터로 채택.
- **악성 샘플(보강) — `lxyeternal/pypi_malregistry`**(GitHub): ASE 2023 논문 기반, PyPI 악성 패키지 10,000+ 건. PyPI 전용이라 우리 프로젝트(PyPI 중심)와 정확히 맞음.
- **정상(negative) 샘플**: PyPI 상위 다운로드 패키지 목록(`hugovk/top-pypi-packages` 스냅샷 또는 pypistats.org 상위 15,000개) — "실제로 널리 쓰이는 정상 패키지"로 구성. 클래스 불균형(정상 >> 악성)은 실제 환경과 유사하므로 오버샘플링(SMOTE) 대신 `class_weight='balanced'` 우선 적용.
- 주의: 악성 샘플은 실행 금지, 정적 분석 전용 샌드박스(Collector 파이프라인과 분리된 격리 환경)에서만 압축 해제/분석.

## 4. 모델 선택

- **1차 베이스라인: Random Forest** (`sklearn.ensemble.RandomForestClassifier`) — 팀 제안대로 채택. 이유: 특징 스케일링 불필요, 특징 중요도(feature_importances_)를 그대로 "어떤 feature가 트리거됐는지" 설명에 사용 가능(요구사항 3의 출력 스키마와 직결), 학습/추론 속도가 빨라 4인 학기 프로젝트 일정에 적합.
  - 하이퍼파라미터 시작값: `n_estimators=300`, `max_depth=None`(과적합 시 12~20으로 제한), `class_weight='balanced'`, `min_samples_leaf=2`, 5-fold stratified CV로 튜닝.
- **비교 대상**: Isolation Forest(비지도, "정상 분포에서 벗어난 정도"로 미라벨 신규 패턴 탐지 보완용) — Random Forest 결과와 앙상블 또는 2단계 필터로 병행 검토.
- **확장 옵션**(시간 남으면): 논문의 stacking classifier(RF + Gradient Boosting + Logistic Regression 메타러너)로 고도화.

## 5. 평가 지표 및 목표

팀 전체 목표(탐지율 90% / FPR 10% 미만)에 맞춰:

- **Recall(탐지율) ≥ 0.90** — 실제 악성 패키지 중 90% 이상 탐지
- **False Positive Rate < 0.10** — 정상 패키지를 악성으로 오탐하는 비율 10% 미만
- 보조 지표: Precision, F1, ROC-AUC, Precision-Recall AUC(불균형 데이터에서 더 신뢰도 높음)
- Hold-out test set은 학습에 쓰지 않은 최신 악성 샘플(예: DataDog 데이터셋의 최근 3개월치)로 구성해 "미래 신규 패턴 일반화" 검증

## 6. 파일 구조 (`ml-detector/`)

```
ml-detector/
├── data/
│   ├── raw/            # DataDog, pypi_malregistry 원본 (git-ignore, 다운로드 스크립트만 커밋)
│   └── processed/      # feature 추출 완료된 학습용 CSV/Parquet
├── features/
│   └── extract.py      # SBOM/메타데이터 → feature vector 변환
├── models/
│   ├── train.py        # RandomForest 학습 + CV
│   └── artifacts/       # 학습된 모델 pickle/joblib (버전 태그)
├── inference/
│   └── predict.py       # Collector 출력 → ml_result.schema.json 형식으로 예측
├── eval/
│   └── metrics.py       # recall/FPR/precision 계산 및 리포트
└── README.md
```

## 7. 출력 JSON 스키마 (DRAFT — `schemas/ml_result.schema.json`)

```json
{
  "schema_version": "0.1.0-draft",
  "generated_at": "2026-09-06T00:00:00Z",
  "results": [
    {
      "package_name": "example-pkg",
      "package_version": "1.2.3",
      "ecosystem": "pypi",
      "is_flagged": true,
      "confidence_score": 0.87,
      "model": "random_forest_v1",
      "triggered_features": [
        { "feature": "install_script_present", "value": true, "importance": 0.31 },
        { "feature": "code_entropy_max", "value": 7.6, "importance": 0.22 },
        { "feature": "maintainer_account_age_days", "value": 4, "importance": 0.18 }
      ]
    }
  ]
}
```

이 스키마는 DRAFT이며 Attack Path Engine 담당자의 검토·승인 후 `schemas/ml_result.schema.json`으로 확정한다(`GIT_POLICY.md` 4번 CODEOWNERS 규칙에 따름).

## 확정 사항 (교차검토 반영)

**Q10. `triggered_features` 구조 (Attack Path Engine 질문 10):**
현재 `{ feature, value, importance }` 배열 형태를 그대로 그래프 노드 속성으로 사용 가능하다고 판단, 재구성 불필요. 다만 그래프 렌더링·Dashboard 표시 편의를 위해 다음을 확정한다: (1) 배열은 `importance` 내림차순 정렬 상태로 출력, (2) 노드 속성 과다 방지를 위해 상위 5개로 cap, (3) 필드명은 그대로 `feature`(string) / `value`(any) / `importance`(0~1 float) 유지. Attack Path Engine은 이 배열을 노드의 `attributes.ml_triggered_features`로 그대로 매핑하면 된다.

**Q11. `confidence_score`와 Risk Analyzer `risk_score` 결합 (Attack Path Engine 질문 11):**
ML/Risk Analyzer 단에서 사전 가중합하지 않는다. 두 신호는 탐지 근거가 다르므로(ML=행동·통계적 이상, Risk Analyzer=알려진 취약점/타이포스쿼팅) 같은 노드 위의 **독립된 두 속성**으로 유지하고, 결합·가중치 부여는 Attack Path Engine의 경로 스코어링 공식에서 처리하도록 위임한다. 예: `node_weight = w1 * risk_score + w2 * (confidence_score * 100)` (w1, w2는 Attack Path Engine이 튜닝). `is_flagged`(bool)도 별도 필드로 유지해 임계값 기반 필터링에 사용 가능하게 한다.


# ============================================================
# 원본: docs/design/04-attack-path.md
# ============================================================

# Attack Path Engine — 기술 설계 문서

담당: 공격경로 / 시각화 · 작성일: 2026-09-06

## 1. 그래프 라이브러리 선택: NetworkX (Python)

Neo4j 대신 **NetworkX**를 선택합니다. 이유:

- **규모**: 학기 프로젝트 대상 그래프는 (패키지 수십 개 × 에이전트 수 개 × 권한 수십 개) 수준 — 메모리 내 그래프로 충분하고, 별도 DB 서버 운영 부담(설치·인증·백업)이 없습니다.
- **팀 통합 비용**: Risk Analyzer·ML·Collector가 모두 Python/JSON 기반이므로, `pip install networkx`만으로 같은 언어 안에서 그래프를 구성·순회할 수 있습니다. Neo4j를 쓰면 Cypher 학습, DB 서버 배포, JSON↔그래프 동기화 계층이 추가로 필요해 4인 팀 규모에서 리스크 대비 이득이 작습니다.
- **출력 호환성**: NetworkX는 `node_link_data()`로 표준 JSON(노드/엣지 배열)을 바로 뽑아낼 수 있어, Dashboard가 소비할 `attack_graph.schema.json`과 자연스럽게 맞습니다.
- **참고했지만 채택 안 한 것**: BloodHound·Wiz Security Graph는 실제로 Neo4j(Cypher)를 씁니다. `shortestPath()` Cypher 쿼리로 진입점→Domain Admin 최단경로를 찾는 방식([BloodHound Cypher 가이드](https://bloodhound.specterops.io/analyze-data/explore/cypher-search))인데, 우리는 이 방법론(가중치 최단경로로 toxic path 탐색)만 차용하고 실행 엔진은 NetworkX로 대체합니다. 데이터 규모가 커지면(자산 수천 개 이상) Neo4j로 이전 가능하도록 그래프 빌더와 알고리즘 계층을 분리해 둡니다.

## 2. 노드/엣지 스키마

| 노드 타입 | 속성 예시 |
|---|---|
| `Package` | `purl`, `name`, `version`, `ecosystem`, `risk_score`(Risk Analyzer 제공), `is_externally_reachable`(bool) |
| `Agent` | `agent_id`, `name`, `anomaly_score`(ML 제공) |
| `Permission` | `perm_id`, `type`(예: `file_write`, `network_egress`, `api_key_access`), `sensitivity`(0~10, "high-value" 여부 판단 기준) |
| `Asset` | `asset_id`, `type`(예: `secret_store`, `db`, `external_api`), `is_crown_jewel`(bool) |

| 엣지 타입 | 방향 | 의미 |
|---|---|---|
| `depends_on` | Agent → Package | 에이전트가 이 패키지에 의존 |
| `has_vulnerability` | Package → Package(취약점 노드 대신 속성으로 단순화 가능) | 위험 신호 존재 (또는 `risk_score` 속성으로 대체) |
| `grants` | Package/Agent → Permission | 이 컴포넌트가 이 권한을 실제로 보유/행사 |
| `exposes` | Permission → Asset | 이 권한이 이 자산에 접근 가능하게 함 |
| `flagged_anomalous` | ML 결과 → Agent (속성으로 병합 가능) | ML이 이상행동으로 표시 |

가중치(`weight`)는 각 엣지에 부여하며, `weight = 1 / (risk_score × anomaly_score 보정치)` 형태로 "위험할수록 가중치가 낮아(=최단경로 탐색 시 더 선호되게)" 설계합니다.

## 3. 경로 탐색 · 우선순위화 알고리즘

1. **그래프 구성**: Risk Analyzer·ML JSON을 읽어 `networkx.DiGraph()`에 위 노드/엣지 추가.
2. **진입점 정의**: `is_externally_reachable=True`인 `Package` 노드 전체를 소스 후보로.
3. **고가치 타깃 정의**: `is_crown_jewel=True`인 `Asset` 노드, 또는 `sensitivity >= 8`인 `Permission` 노드를 타깃으로.
4. **경로 탐색**: 각 (소스, 타깃) 쌍에 대해 `networkx.shortest_simple_paths(G, source, target, weight="weight")`로 가중치 기준 상위 K개 경로를 생성(Yen's 알고리즘 기반, BloodHound의 `shortestPath()`와 동일한 발상). 그래프가 작으므로 `all_simple_paths()`로 전수 탐색 후 정렬하는 방식도 병행 가능.
5. **"toxic combination" 판정**: 경로 길이(홉 수) 대신 **경로 내 최소 개별 위험도가 아니라 결합 위험도**를 본다 — `path_score = Σ(hop별 risk/anomaly) × exposure_multiplier(진입점이 외부 노출인가)`. 개별 hop이 전부 "중간 위험"이어도 path_score가 임계치를 넘으면 toxic으로 표시.
6. **우선순위화**: `path_score` 내림차순 정렬 → 상위 N개를 "critical path"로 태깅, `networkx.betweenness_centrality()`로 여러 경로에 공통으로 등장하는 병목 노드(예: 특정 권한)를 별도로 표시해 "이 노드 하나만 고쳐도 여러 경로가 끊긴다"는 인사이트 제공.
7. **PoC 검증**: 취약 테스트 에이전트에서 실제로 해당 경로(패키지 취약점 → 권한 획득 → 자산 접근)를 재현해 시나리오 설명 텍스트를 첨부.

## 4. 입력 필드 요구사항

- **Risk Analyzer로부터**: `purl`, `package_risk_score`(0~10), `vulnerability_ids`(CVE/OSV), `is_externally_reachable`, 해당 패키지를 사용하는 `agent_id` 매핑.
- **ML로부터**: `agent_id`, `anomaly_score`(0~1), `anomaly_type`(예: 비정상 API 호출 패턴), 탐지 시각.
- **Collector/공통**: 에이전트별 `permission` 목록(권한 타입, 대상 자산) — 이 필드가 현재 스키마에 없다면 Collector 또는 별도 설정 파일에서 받아야 함(팀 확인 필요).

## 5. `attack-path/` 폴더 구조 (제안)

```
attack-path/
├── graph_builder.py      # Risk Analyzer/ML JSON → networkx.DiGraph
├── path_finder.py        # shortest_simple_paths, toxic combination 판정
├── prioritizer.py        # path_score 계산, betweenness_centrality
├── scenario_writer.py    # 경로 → 자연어 침해 시나리오 텍스트 생성
├── poc/                  # 취약 테스트 에이전트 + 검증 스크립트
├── export.py             # node_link_data() → attack_graph.schema.json 형식으로 출력
└── tests/
```

## 6. 출력 스키마 초안 (`schemas/attack_graph.schema.json`, Dashboard 소비용)

```json
{
  "schema_version": "1.0",
  "run_id": "run-2026-09-06-01",
  "generated_at": "2026-09-06T00:00:00Z",
  "source_module": "attack-path",
  "nodes": [
    {
      "id": "pkg:pypi/flask@2.0.1", "type": "dependency", "label": "flask 2.0.1",
      "risk_score": 72,
      "attributes": {"package_version": "2.0.1", "cve_ids": ["CVE-XXXX"], "typosquat_flag": false}
    },
    {
      "id": "perm:api_key_access", "type": "permission", "label": "API Key Access",
      "risk_score": 80,
      "attributes": {"permission_name": "api_key_access", "target_asset": "asset:secret_store"}
    }
  ],
  "edges": [
    {"id": "e1", "source": "agent:orchestrator-1", "target": "pkg:pypi/flask@2.0.1", "type": "depends_on", "risk_contribution": 14}
  ],
  "paths": [
    {
      "path_id": "path-001",
      "node_sequence": ["pkg:pypi/flask@2.0.1", "agent:orchestrator-1", "perm:api_key_access", "asset:secret_store"],
      "edge_sequence": ["e1", "e2", "e3"],
      "overall_risk_score": 89,
      "description": "외부 노출된 flask 취약점(CVE-XXXX)을 통해 orchestrator-1 에이전트를 장악하면, 보유한 api_key_access 권한으로 secret_store까지 접근 가능"
    }
  ]
}
```

(초안이므로 Dashboard 담당 리뷰 후 필드명·타입 확정 필요)

## 확정 사항 (교차검토 반영)

**1. Permission 데이터 출처 (팀 전체 결정, 최중요):** 제시된 (a)/(b)/(c) 중 하나가 아니라 **(a)+(c) 혼합**을 채택합니다. Collector가 에이전트 코드를 정적 스캔하는 유일한 모듈이므로 실제 "이 에이전트가 이 권한을 행사한다"는 사실(`agent.permissions[]`: 권한 타입 + 대상 자산 문자열)은 Collector가 코드 스캔으로 채워 넣고, 그 필드의 **enum·구조 자체는 Attack Path Engine이 정의**합니다(그래프 노드/엣지로 직접 소비하는 쪽이 스키마를 소유해야 이후 그래프 빌더 변경 시 마찰이 없기 때문). Risk Analyzer·ML은 이 필드를 만들지 않고 참조만 합니다. Collector 담당자에게 `agent.permissions[]` 필드 추가를 요청 예정.

**2. 출력 형식 (Q15):** Dashboard 설계서(`05-dashboard.md` §5)가 이미 `nodes/edges/paths` 구조로 스키마를 확정했으므로 Cytoscape `elements:{nodes,edges}` 포맷으로 바꾸지 않습니다. Cytoscape 변환은 프론트엔드(`graphView.js`)가 로드 시 수행합니다.

**3. Risk Analyzer로부터 (Q8/9):** `02-risk-analyzer.md`가 이미 `risk_score`(숫자)와 `risk_level` 둘 다, 그리고 `signals{cvss_norm, epss_score, typo_flag, staleness_score}`를 제공하도록 확정되어 있어 요구사항을 충족합니다. 추가로 원본 `vulnerability_ids`(CVE 목록)도 함께 넘겨주시길 요청합니다 — Dashboard 노드 `attributes.cve_ids`를 채우려면 signals만으로는 부족합니다.

**4. ML로부터 (Q10/11):** `triggered_features`(feature+importance 배열) 구조는 그대로 `Agent` 노드의 `attributes.ml_anomaly_score` 및 상세 패널용 부가 정보로 바로 사용 가능하며 변환 불필요합니다. `confidence_score`는 별도 노드를 만들지 않고 가중합으로 결합합니다: `weight = 1 / (risk_score × confidence_score 보정치)` (§3 기존 설계 유지).

**5. Dashboard에게 (Q12-14):** 모든 `Package`/`Agent`/`Permission` 노드에 사전 계산된 `risk_score`(0-100 정규화), 모든 `paths[]`에 `overall_risk_score`를 채워 넘깁니다(Dashboard 재계산 없음 보장). 각 노드는 `label`(사람이 읽는 이름), 타입별 `attributes`(패키지 버전/CVE 목록/권한명·자산명/에이전트명/ML 이상점수)를 포함합니다. `export.py`가 `node_link_data()` 출력 직후 `node_sequence`/`edge_sequence`의 모든 id가 동일 파일 `nodes[].id`/`edges[].id`에 실제 존재하는지 검증하는 참조 무결성 체크를 통과해야만 파일을 씁니다(단위 테스트로 강제).


# ============================================================
# 원본: docs/design/05-dashboard.md
# ============================================================

# Dashboard 설계 문서 (05 — Dashboard)

담당: 공격경로/시각화 · 최종 수정: 2026-09-06

## 1. 시각화 라이브러리: Cytoscape.js 확정

`resources/curated_list.md` J절의 2026 비교 가이드(Cytoscape.js vs vis-network vs Sigma.js)와 WebSearch로 확인한 실제 보안 그래프 UI 사례(공격경로 시각화 툴들이 risk score로 정렬하고 클릭 시 경로를 하이라이트하는 패턴)를 근거로, 사전 검토된 **Cytoscape.js를 그대로 확정**합니다.

- 우리 그래프는 `의존성 → 에이전트 → 권한 → 공격경로`의 4단계 이종(heterogeneous) 노드 타입 + 계층적 흐름을 가지며, 노드 수는 학부 프로젝트 규모(수십~수백 개)로 대규모가 아닙니다. 이 규모에서는 Sigma.js(WebGL, 수만 개 노드 최적화)의 장점이 필요 없고, vis-network는 그래프 알고리즘·레이아웃 확장(`cytoscape-dagre`, `cytoscape-cola` 등)이 Cytoscape.js보다 빈약합니다.
- Cytoscape.js는 원래 생물정보학 네트워크 분석용으로 설계되어 "노드/엣지에 속성을 붙이고 그 속성으로 스타일·필터·경로탐색을 하는" 용도에 강하며, 보안 공격경로 시각화 연구·툴에서도 실제로 채택 사례가 있습니다. `dagre` 레이아웃이 우리의 단계적 흐름(의존성→...→경로)을 자연스러운 좌→우 계층 구조로 그려준다는 점이 결정적입니다.

## 2. 웹 스택: FastAPI(얇은 백엔드) + 정적 JS 프론트엔드

`docs/design/00-overall.md`는 "Dashboard만 JS(Node 20+)"로 잠정 제안했으나, 이를 다음과 같이 보완 제안합니다.

**결론: 아주 얇은 FastAPI 백엔드(Python) + 빌드 도구 없는 순수 JS(Cytoscape.js) 프론트엔드.**

이유:
- Dashboard의 입력은 `schemas/attack_graph.schema.json`을 따르는 JSON 파일 하나뿐입니다(00-overall.md의 파일 기반 핸드오프 원칙 그대로 계승). 백엔드가 하는 일은 (1) `data/<run_id>/attack_graph.json`을 읽어 스키마 유효성 검사 후 그대로 내려주기, (2) 사용 가능한 run 목록 제공, (3) 정적 파일 서빙뿐입니다.
- 이걸 Python(FastAPI)으로 하면 `pydantic` 모델을 `schemas/attack_graph.schema.json`과 1:1로 맞춰 다른 3개 모듈과 동일한 스키마 검증 관례(00-overall.md 4절의 "자기 모듈 출력이 schemas/*.schema.json을 통과하는지" 테스트 원칙)를 그대로 재사용할 수 있고, 팀 전체가 Python 3.11 통일 컨벤션을 따르므로 유지보수 부담이 적습니다. Node 백엔드를 새로 만들면 팀에서 유일하게 다른 런타임/CI 설정이 하나 더 늘어납니다.
- 프론트엔드는 React/Vue 등 프레임워크 없이 순수 JS + Cytoscape.js로 구성합니다. 지도교수·쿤텍에게 보여주는 최종 산출물이 "그래프를 그리고 클릭하면 정보가 뜨는" 수준이라 SPA 프레임워크는 과설계이며, 빌드 파이프라인이 없으면 `python -m http.server` 또는 FastAPI의 `StaticFiles`만으로 실행 가능해 발표/시연 리스크가 줄어듭니다.

## 3. 핵심 인터랙션 기능 (우선순위 순)

1. **위험도 기준 필터링** — 슬라이더로 risk_score 임계값을 조절하면 그 이하 노드/엣지를 dim 처리. 검토 대상을 빠르게 좁히는 것이 보안 리뷰의 핵심 동작이므로 최우선.
2. **경로(Path) 하이라이트** — 오른쪽 "위험 경로 목록"에서 경로를 클릭하면 그래프에서 해당 노드/엣지 시퀀스만 강조하고 나머지는 회색 처리 + 애니메이션 이동.
3. **노드 상세 패널** — 노드 클릭 시 우측 패널에 타입별 상세 정보(패키지명·버전·CVE 목록, 에이전트명, 권한명 등) 표시.
4. **검색** — 노드 라벨/CVE ID로 검색해 그래프 내 위치로 포커스 이동.
5. **레이아웃 전환** — 기본 `dagre`(계층형) ↔ `cola`(힘 기반, 전체 구조 탐색용) 토글.
6. **PNG 내보내기** — Cytoscape.js 내장 기능으로 현재 뷰를 이미지로 저장(보고서 삽입용).

## 4. 화면 구성 (3-뷰 구조)

- **그래프 뷰(메인)**: Cytoscape 캔버스, 상단에 run 선택 드롭다운 + 위험도 슬라이더 + 검색창.
- **위험 자산/경로 리스트 뷰(우측 패널 상단)**: risk_score 내림차순 정렬 테이블(경로/노드), 클릭 시 그래프 하이라이트와 연동.
- **노드/경로 상세 뷰(우측 패널 하단, 컨텍스트 전환)**: 선택된 노드 또는 경로의 전체 필드를 사람이 읽을 수 있는 형태로 표시.

## 5. Attack Path Engine에 요청하는 INPUT 스키마 (`schemas/attack_graph.schema.json`)

Dashboard는 아래 필드가 **반드시** 채워진 상태로 넘어와야 자체 재계산 없이 바로 렌더링할 수 있습니다.

```jsonc
{
  "schema_version": "1.0",
  "run_id": "string",
  "generated_at": "ISO8601 string",
  "source_module": "attack-path",
  "nodes": [
    {
      "id": "string (unique)",
      "type": "dependency | agent | permission | path_step",
      "label": "string (사람이 읽을 표시명, 필수)",
      "risk_score": "number 0-100 (Dashboard는 재계산하지 않음)",
      "attributes": {
        "package_version": "string, optional",
        "cve_ids": ["string", "..."],
        "typosquat_flag": "boolean, optional",
        "ml_anomaly_score": "number, optional",
        "permission_name": "string, optional",
        "agent_name": "string, optional"
      }
    }
  ],
  "edges": [
    { "id": "string", "source": "node id", "target": "node id",
      "type": "depends_on | grants_permission | enables_path",
      "risk_contribution": "number 0-100, optional" }
  ],
  "paths": [
    {
      "path_id": "string",
      "node_sequence": ["node id", "..."],
      "edge_sequence": ["edge id", "..."],
      "overall_risk_score": "number 0-100 (필수, 리스트 정렬 기준)",
      "description": "string (사람이 읽을 한 줄 요약, 필수)"
    }
  ]
}
```

## 6-1. 확정 사항 (교차검토 반영)

**질문 15 답변 (Attack Path Engine → Dashboard):** Attack Path Engine은 **범용 `nodes/edges/paths` JSON**(위 5절 스키마 그대로)만 출력하고, Cytoscape 전용 `elements` 포맷으로의 변환은 **Dashboard 프론트엔드가 렌더링 시점에** 수행합니다.

**이유:** (1) attack-path 모듈이 특정 시각화 라이브러리에 종속되지 않아 UI 라이브러리 교체 시 상류 스키마 변경이 불필요하고, (2) 범용 구조가 스키마 검증·유닛테스트하기 더 쉬우며, (3) 변환 로직 자체가 몇 줄 수준이라 Dashboard 쪽 부담이 거의 없습니다.

```js
// frontend/js/graphView.js
function toCytoscapeElements(graph) {
  const nodes = graph.nodes.map(n => ({
    data: { id: n.id, label: n.label, type: n.type, riskScore: n.risk_score, ...n.attributes }
  }));
  const edges = graph.edges.map(e => ({
    data: { id: e.id, source: e.source, target: e.target, type: e.type }
  }));
  return { nodes, edges };
}
cy.add(toCytoscapeElements(graph)); // graph = attack_graph.json
```

## 6. `dashboard/` 파일 구조 제안

```
dashboard/
├── backend/
│   ├── app.py                 # FastAPI 진입점, StaticFiles 마운트
│   ├── models.py              # attack_graph.schema.json에 대응하는 pydantic 모델
│   ├── routes/graph.py        # GET /api/runs, GET /api/graph/{run_id}
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/
│       ├── api.js             # fetch 래퍼
│       ├── graphView.js        # cytoscape 초기화·레이아웃·하이라이트
│       ├── riskList.js         # 위험 리스트 렌더링·정렬
│       └── detailPanel.js      # 노드/경로 상세 패널
├── tests/
│   └── test_schema_validation.py
└── README.md
```


# ============================================================
# 원본: schemas/collector_output.schema.json
# ============================================================

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CollectorOutput",
  "description": "Dependency Collector 모듈 출력. CODEOWNERS: @총괄 @위험분석담당 @ML담당",
  "type": "object",
  "required": ["schema_version", "scan_id", "repo", "status", "dependencies", "summary"],
  "properties": {
    "schema_version": { "type": "string", "const": "0.1.0" },
    "scan_id": { "type": "string", "format": "uuid" },
    "repo": {
      "type": "object",
      "required": ["url", "scanned_at"],
      "properties": {
        "url": { "type": "string" },
        "commit_sha": { "type": ["string", "null"] },
        "scanned_at": { "type": "string", "format": "date-time" }
      }
    },
    "status": { "type": "string", "enum": ["success", "partial", "failed"] },
    "dependencies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "ecosystem", "resolution_status"],
        "properties": {
          "name": { "type": "string" },
          "version": { "type": ["string", "null"] },
          "ecosystem": { "type": "string" },
          "source": { "type": "array", "items": { "type": "string", "enum": ["manifest", "import", "dockerfile"] } },
          "declared_in": { "type": "array", "items": { "type": "string" } },
          "resolution_status": { "type": "string", "enum": ["resolved", "unresolved"] },
          "pypi": {
            "type": "object",
            "properties": {
              "latest_version": { "type": ["string", "null"] },
              "summary": { "type": ["string", "null"] },
              "license": { "type": ["string", "null"] },
              "home_page": { "type": ["string", "null"] },
              "last_release_at": { "type": ["string", "null"], "format": "date-time" }
            }
          },
          "hashes": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": { "algo": { "type": "string" }, "value": { "type": "string" } }
            }
          },
          "distribution_files": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "filename": { "type": "string" },
                "url": { "type": "string" },
                "hashes": { "type": "array", "items": { "type": "object" } }
              }
            }
          },
          "vulnerabilities": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["id", "severity"],
              "properties": {
                "id": { "type": "string" },
                "aliases": { "type": "array", "items": { "type": "string" } },
                "severity": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"] },
                "cvss_base_score": { "type": ["number", "null"], "minimum": 0, "maximum": 10 },
                "cvss_source": { "type": ["string", "null"], "enum": ["nvd", "osv", null] },
                "fixed_versions": { "type": "array", "items": { "type": "string" } },
                "osv_url": { "type": "string" }
              }
            }
          },
          "maintainers": {
            "type": "object",
            "properties": {
              "maintainer_count": { "type": ["integer", "null"] },
              "data_status": { "type": "string", "enum": ["ok", "not_available"] },
              "maintainer_accounts": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "username": { "type": "string" },
                    "account_created_at": { "type": ["string", "null"] },
                    "data_status": { "type": "string", "enum": ["ok", "not_collected"] }
                  }
                }
              }
            }
          },
          "external_integrations": {
            "type": "array",
            "items": { "type": "string", "enum": ["network", "shell", "mcp", "filesystem"] }
          }
        }
      }
    },
    "agent": {
      "type": "object",
      "description": "에이전트 단위 권한 정보. 필드 구조/enum 소유권은 Attack Path Engine, 값 채우기는 Collector 담당 (교차검토 확정 사항 1번)",
      "properties": {
        "permissions": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["type", "target_asset"],
            "properties": {
              "type": { "type": "string", "description": "Attack Path Engine이 정의하는 enum (예: file_write, network_egress, api_key_access, shell_exec)" },
              "target_asset": { "type": "string" }
            }
          }
        }
      }
    },
    "integrations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "name": { "type": "string" },
          "detected_in": { "type": "string" },
          "transport": { "type": "string" }
        }
      }
    },
    "sbom": {
      "type": "object",
      "properties": {
        "format": { "type": "string" },
        "spec_version": { "type": "string" },
        "generator": { "type": "string" },
        "file_ref": { "type": "string" }
      }
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["stage", "code", "message"],
        "properties": {
          "stage": { "type": "string" },
          "code": { "type": "string" },
          "message": { "type": "string" },
          "package": { "type": ["string", "null"] }
        }
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_dependencies": { "type": "integer" },
        "resolved": { "type": "integer" },
        "unresolved": { "type": "integer" },
        "vulnerable_count": { "type": "integer" },
        "integrations_count": { "type": "integer" }
      }
    }
  }
}
```


# ============================================================
# 원본: schemas/risk_score.schema.json
# ============================================================

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RiskScoreOutput",
  "description": "Risk Analyzer 모듈 출력. CODEOWNERS: @위험분석담당 @공격경로담당",
  "type": "object",
  "required": ["generated_at", "packages"],
  "properties": {
    "generated_at": { "type": "string", "format": "date-time" },
    "packages": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "version", "ecosystem", "package_risk", "permission_weight", "permission_source", "risk_score", "risk_level", "signals"],
        "properties": {
          "name": { "type": "string" },
          "version": { "type": "string" },
          "ecosystem": { "type": "string" },
          "package_risk": { "type": "number", "minimum": 0, "maximum": 1 },
          "permission_weight": { "type": "number", "minimum": 1.0, "maximum": 3.0 },
          "permission_source": {
            "type": "string",
            "description": "권한 등급 산정에 쓰인 권한 데이터의 출처. Risk Analyzer는 권한 목록을 직접 생성하지 않고 Attack Path Engine 소유 스키마를 참조한다.",
            "enum": ["attack_path_engine", "default_medium_fallback"]
          },
          "risk_score": { "type": "number", "minimum": 0, "description": "숫자형 원점수(0~3.0). Dashboard 등 정렬/시각화용." },
          "risk_level": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH"] },
          "vulnerability_ids": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Attack Path Engine 요청으로 추가 — Dashboard의 attributes.cve_ids 채우기용 원본 CVE/OSV ID 목록"
          },
          "signals": {
            "type": "object",
            "properties": {
              "cvss_norm": { "type": "number", "minimum": 0, "maximum": 1 },
              "cve_ids": { "type": "array", "items": { "type": "string" } },
              "epss_score": { "type": "number", "minimum": 0, "maximum": 1 },
              "typo_flag": { "type": "number", "enum": [0, 0.5, 1] },
              "typo_nearest_match": { "type": ["string", "null"] },
              "staleness_score": { "type": "number", "minimum": 0, "maximum": 1 },
              "months_since_last_release": { "type": "number" }
            }
          }
        }
      }
    }
  }
}
```


# ============================================================
# 원본: schemas/ml_result.schema.json
# ============================================================

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MLResultOutput",
  "description": "ML 이상탐지 모듈 출력. CODEOWNERS: @ML담당 @공격경로담당",
  "type": "object",
  "required": ["schema_version", "generated_at", "results"],
  "properties": {
    "schema_version": { "type": "string" },
    "generated_at": { "type": "string", "format": "date-time" },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["package_name", "package_version", "ecosystem", "is_flagged", "confidence_score", "model", "triggered_features"],
        "properties": {
          "package_name": { "type": "string" },
          "package_version": { "type": "string" },
          "ecosystem": { "type": "string" },
          "is_flagged": { "type": "boolean" },
          "confidence_score": { "type": "number", "minimum": 0, "maximum": 1 },
          "model": { "type": "string" },
          "triggered_features": {
            "type": "array",
            "description": "importance 내림차순 정렬, 상위 5개로 cap. Attack Path Engine이 attributes.ml_triggered_features로 그대로 매핑.",
            "maxItems": 5,
            "items": {
              "type": "object",
              "required": ["feature", "value", "importance"],
              "properties": {
                "feature": { "type": "string" },
                "value": {},
                "importance": { "type": "number", "minimum": 0, "maximum": 1 }
              }
            }
          }
        }
      }
    }
  }
}
```


# ============================================================
# 원본: schemas/attack_graph.schema.json
# ============================================================

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AttackGraphOutput",
  "description": "Attack Path Engine 모듈 출력 (Dashboard 소비용). CODEOWNERS: @공격경로담당 @대시보드담당. 형식은 범용 nodes/edges/paths — Cytoscape 등 라이브러리별 변환은 소비 측(Dashboard) 프론트엔드가 수행.",
  "type": "object",
  "required": ["schema_version", "run_id", "generated_at", "nodes", "edges", "paths"],
  "properties": {
    "schema_version": { "type": "string" },
    "run_id": { "type": "string" },
    "generated_at": { "type": "string", "format": "date-time" },
    "source_module": { "type": "string", "const": "attack-path" },
    "nodes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "type", "label", "risk_score"],
        "properties": {
          "id": { "type": "string" },
          "type": { "type": "string", "enum": ["dependency", "agent", "permission", "asset"] },
          "label": { "type": "string", "description": "사람이 읽는 이름. Dashboard 표시용" },
          "risk_score": { "type": "number", "minimum": 0, "maximum": 100, "description": "사전 정규화(0-100) 완료 — Dashboard는 재계산하지 않음" },
          "attributes": {
            "type": "object",
            "description": "타입별 상세 정보 (패키지버전/cve_ids/권한명·자산명/에이전트명/ml_triggered_features 등)"
          }
        }
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "source", "target", "type"],
        "properties": {
          "id": { "type": "string" },
          "source": { "type": "string", "description": "nodes[].id 참조 — 참조 무결성 필수" },
          "target": { "type": "string", "description": "nodes[].id 참조 — 참조 무결성 필수" },
          "type": { "type": "string", "enum": ["depends_on", "grants", "exposes", "flagged_anomalous"] },
          "risk_contribution": { "type": "number" }
        }
      }
    },
    "paths": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path_id", "node_sequence", "edge_sequence", "overall_risk_score", "description"],
        "properties": {
          "path_id": { "type": "string" },
          "node_sequence": { "type": "array", "items": { "type": "string" }, "description": "nodes[].id 참조, 참조 무결성 필수 (export.py에서 검증 후 출력)" },
          "edge_sequence": { "type": "array", "items": { "type": "string" }, "description": "edges[].id 참조, 참조 무결성 필수" },
          "overall_risk_score": { "type": "number", "minimum": 0, "maximum": 100, "description": "사전 계산 완료" },
          "description": { "type": "string", "description": "사람이 읽는 침해 시나리오 한 줄 설명" }
        }
      }
    }
  }
}
```


# ============================================================
# 원본: docs/design/_cross_review_questions.md
# ============================================================

# 교차 검토 — 모듈 간 미해결 질문 (1차 설계 라운드에서 수집)

각 담당자는 자기 앞으로 온 질문에 답하고, 자기 설계/에픽 문서에 "## 확정 사항 (교차검토 반영)" 섹션을 추가해서 최종 스키마 필드를 확정하세요.

## → Collector 담당자에게

**From Risk Analyzer:**
1. `package.vulnerabilities[]`에 CVE ID뿐 아니라 `cvss_base_score`를 직접 넣어줄 수 있나요? (재조회 안 해도 되게)
2. `external_integrations[]` (패키지가 shell/network/MCP 접근을 쓰는지) 필드를 스키마에 넣을 계획이 있나요? Risk Analyzer의 permission_weight 계산에 필수입니다.
3. `latest_release_date`, `maintainer_count`가 모든 패키지에 대해 항상 존재를 보장하나요? (staleness score 계산용)

**From ML 이상탐지:**
4. SBOM에 배포 파일(sdist/wheel) 자체 경로나 해시가 포함되나요, 메타데이터만인가요? (정적 코드 분석 feature용)
5. maintainer의 PyPI 계정 생성일 등 계정 정보까지 수집 범위인가요?

## → Risk Analyzer 담당자에게

**From Attack Path Engine:**
6. 에이전트별 "권한(Permission)" 목록(권한 타입, 대상 자산)을 Risk Analyzer가 제공하나요, 아니면 이 정보 자체가 스키마 어디에도 없는데 누가 만들어야 하나요? (현재 미해결 — 팀 전체가 결정해야 함)
7. `is_externally_reachable`(외부 노출 여부)을 Risk Analyzer가 계산해서 주나요, Attack Path Engine이 직접 판단해야 하나요?

**From Attack Path Engine (스키마 관련, 답변 필요):**
8. `signals` 서브 오브젝트(cvss_norm, epss_score, typo_flag, staleness_score)면 그래프 노드 속성으로 충분한가요, 원본 CVE 목록도 필요한가요?
9. `risk_level`(LOW/MEDIUM/HIGH)로 충분한가요, 숫자 `risk_score`도 필요한가요?

## → ML 이상탐지 담당자에게

**From Attack Path Engine:**
10. `triggered_features` 구조(feature명+importance)가 그래프 구축에 바로 쓸 수 있는 형태인가요, 다른 표현이 필요한가요?
11. `confidence_score`를 Risk Analyzer의 위험 점수와 어떻게 결합할 계획인가요(가중합/별도 노드 등)?

## → Attack Path Engine 담당자에게 (가장 많은 질문이 몰림 — 우선 처리)

**From Risk Analyzer & ML 둘 다 → Attack Path Engine으로 넘어온 질문 6, 7 관련:**
"권한(Permission)" 데이터 출처가 현재 스키마 어디에도 없습니다. 팀 결정 필요: (a) Collector가 에이전트 코드에서 권한 사용 패턴을 추가로 스캔해서 제공, (b) Risk Analyzer가 별도로 정의, (c) Attack Path Engine이 직접 정의하고 나머지는 참조만. **이 문서에서 하나를 선택하고 이유를 적어주세요.**

**From Dashboard:**
12. `risk_score`(0-100)가 모든 노드에, `overall_risk_score`가 모든 경로에 사전 계산되어 붙어있나요? (Dashboard는 재계산 안 한다고 가정 중)
13. 각 노드에 사람이 읽을 수 있는 `label`, 각 경로에 한 줄 `description`, 타입별 `attributes`(CVE 목록/패키지버전/권한·에이전트명/ML 이상점수)를 넣어줄 수 있나요?
14. `node_sequence`/`edge_sequence`가 같은 파일의 `nodes[].id`/`edges[].id`를 항상 유효하게 참조하나요? (참조 무결성 보장)

**Attack Path Engine이 Dashboard에게 남긴 질문:**
15. nodes/edges/paths 구조가 맞나요, Cytoscape.js 전용 `elements: {nodes, edges}` 포맷을 원하나요?

## → Dashboard 담당자에게

**From Attack Path Engine:** 질문 15 답변 필요.

## → 총괄(PM)이 팀 차원에서 정리해야 할 것

- `schemas/`의 공통 메타 필드(`run_id`, `schema_version`)를 4개 스키마 전부에 강제할지 여부
- `pipeline/` 오케스트레이션 코드를 누가 소유·유지보수할지
- 중간 산출물(`data/`)을 로컬에만 둘지 AWS S3에 올릴지 (M3 이전 결정 필요)
- **권한(Permission) 데이터의 출처** — 질문 6/11 관련, Attack Path Engine 담당자의 결정을 최종 승인


# ============================================================
# 원본: docs/epics/00-overall.md
# ============================================================

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


# ============================================================
# 원본: docs/epics/01-collector.md
# ============================================================

# [Epic] Dependency Collector 모듈 구축

## 목표

AI 에이전트 저장소를 스캔해서 (1) 의존성 목록, (2) LangChain·MCP 등 외부 연동 도구, (3) PyPI 메타데이터·취약점, (4) 표준 SBOM을 자동으로 뽑아내는 파이프라인 입구 모듈을 완성한다. 이 모듈의 산출물이 Risk Analyzer·ML 이상탐지의 입력이 되므로, 여기서 놓친 자산은 뒤 단계 전체가 못 본다.

## 범위

- 매니페스트 파싱(requirements.txt, pyproject.toml, Pipfile, package.json)
- 실제 import 스캔(pipreqs) 및 매니페스트와의 `--diff` 비교
- Dockerfile 파싱(베이스 이미지, `pip install`, `COPY requirements*`)
- LangChain·MCP 외부 연동 탐지(코드 내 import 패턴 + `mcp.json`류 설정 파일)
- PyPI JSON API 메타데이터·취약점 조회 (캐싱·재시도 포함)
- 취약점 정보 보완용 OSV 배치 조회
- CycloneDX 포맷 SBOM 생성(`cyclonedx-py` 활용)
- 위 모든 결과를 하나의 표준 출력 객체로 병합·검증·저장

**범위 밖**: 비-PyPI 생태계(npm 등)의 취약점 심층 분석, 컨테이너 OS 패키지(apt 등)의 상세 취약점 분석, reachability 분석(어떤 취약 함수가 실제 호출되는지) — 이는 추후 로드맵 또는 Risk Analyzer 영역.

## 완료조건

- [ ] 임의의 공개 GitHub AI 에이전트 저장소(requirements.txt 유무와 무관)를 입력하면 의존성 목록이 생성된다
- [ ] LangChain/MCP 연동이 있는 저장소에서 해당 연동이 최소 1개 이상 탐지된다
- [ ] 각 의존성에 PyPI 메타데이터(버전·라이선스·해시)와 알려진 취약점 정보가 채워진다 (PyPI 미등록 패키지는 `unresolved`로 표시되고 파이프라인은 계속 진행된다)
- [ ] CycloneDX 형식 SBOM 파일이 생성된다
- [ ] 비공개/접근 불가 저장소, 매니페스트 부재, PyPI 조회 실패 등 예외 상황에서도 전체 프로세스가 죽지 않고 `partial`/`failed` 상태와 에러 목록을 포함한 결과를 반환한다
- [ ] 출력이 `schemas/collector_output.schema.json` DRAFT를 만족하며, Risk Analyzer·ML 담당자 리뷰를 거쳐 스키마가 확정된다

## 출력 인터페이스

`docs/design/01-collector.md`의 DRAFT 스키마 참고. 핵심 구조만 요약:

```
{
  schema_version, scan_id, repo, status,
  dependencies: [{ name, version, ecosystem, source, resolution_status, pypi{...}, hashes[], vulnerabilities[] }],
  integrations: [{ type, name, detected_in, transport? }],
  sbom: { format, spec_version, generator, file_ref },
  errors: [{ stage, code, message, package? }],
  summary: { total_dependencies, resolved, unresolved, vulnerable_count, integrations_count }
}
```

이 스키마는 `GIT_POLICY.md` §3에 따라 `schemas/collector_output.schema.json`으로 최종 확정 전 **Risk Analyzer·ML 담당자 전원 승인**이 필요한 CODEOWNERS 대상 파일입니다.

## 참고자료

- `study_week1/README.md` §5 (Dependency Collector 구현 가이드), §6 (MCP 딥다이브)
- `study_week1/architecture.html` #collector 섹션
- `study_week1/raw/10_pypi_requirements_parser.md`, `14_pipreqs_github.md`, `15_pypi_json_api_docs.md`, `16_cyclonedx_python_github.md`, `17_osv_api_query_endpoint.md`
- `docs/design/01-collector.md` (본 에픽의 상세 설계 및 스키마 DRAFT)
- `GIT_POLICY.md` §3 (스키마 계약·CODEOWNERS 규칙)

## 하위 이슈

(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)


# ============================================================
# 원본: docs/epics/02-risk-analyzer.md
# ============================================================

# [Epic] Risk Analyzer 모듈 구현

담당: 위험분석 | 관련 모듈: Risk Analyzer | 라벨: `risk-analyzer`, `schema`, `feature`

## 목표

Dependency Collector가 만든 SBOM·의존성 목록을 입력받아, 패키지별로 "패키지 자체 위험도(CVE/CVSS/EPSS + 타이포스쿼팅 + 유지보수 상태) × 에이전트 권한 가중치" 공식으로 위험 점수를 산출하고, 이를 표준 JSON으로 Attack Path Engine에 넘기는 것.

## 범위

**포함**
- CVSS 기반 취약점 심각도 정규화 (Collector가 수집한 CVE/CVSS 값 활용)
- EPSS(악용 예측 확률) API 연동 및 결합 로직
- 타이포스쿼팅 탐지: 인기 패키지 top-N 대비 Levenshtein distance 기반 규칙 + 보조 신호(다운로드 수, 등록일)
- 유지보수 상태 신호: 마지막 릴리즈일, 메인테이너 수 기반 staleness 점수
- 에이전트 권한 등급(LOW/MEDIUM/HIGH) 승수 반영
- 최종 위험 점수·등급을 `schemas/risk_score.schema.json` 형식으로 출력

**제외 (범위 밖)**
- ML 기반 신규/변종 악성 패키지 탐지 (ML 이상탐지 모듈 담당)
- 의존성-권한-공격경로 그래프 구성 (Attack Path Engine 담당)
- combosquatting(문자 치환형) 등 고급 타이포스쿼팅 규칙, 다국어/비-PyPI 생태계 지원 — v2 이후 별도 이슈로 분리

## 완료 조건 (Acceptance Criteria)

- [ ] `risk-analyzer/` 디렉토리에 스코어링 파이프라인 동작 (Collector 출력 JSON → risk_score.json)
- [ ] CVSS·EPSS·타이포스쿼팅·staleness 4개 신호가 각각 독립 모듈로 분리되어 단위 테스트 가능
- [ ] 최소 1개 실제 CVE 보유 패키지(예: 과거 취약점 있는 버전)로 점수 산출 검증
- [ ] 타이포스쿼팅 탐지가 알려진 사례(colorama/colorizr류 이름)를 최소 1건 이상 정탐
- [ ] `schemas/risk_score.schema.json` 초안 작성 및 Attack Path Engine 담당 리뷰·승인 완료 (GIT_POLICY.md CODEOWNERS 규칙)
- [ ] Collector 출력에 필요한 필드(아래 입력 인터페이스)가 실제로 채워지는지 Collector 담당과 교차 확인

## 입력/출력 인터페이스

**입력 (Collector → Risk Analyzer, `schemas/collector_output.schema.json` 요구사항)**
- `package.name`, `package.ecosystem`, `package.version` (필수)
- `package.latest_release_date`, `package.maintainer_count` (staleness 계산용)
- `package.vulnerabilities[].cve_id`, `.cvss_base_score` (PyPI JSON API `vulnerabilities` 필드에서 이미 확보 가능)
- `package.osv_ids[]` (CVE 미매핑 취약점 대응)
- `external_integrations[]` — 패키지가 쓰이는 컨텍스트(쉘 실행/네트워크/MCP 연동 등). **현재 미정의 시 Collector 담당과 신규 협의 필요**

**출력 (Risk Analyzer → Attack Path Engine, `schemas/risk_score.schema.json`)**
- 패키지별 `package_risk`(0~1), `permission_weight`(1.0~3.0), `risk_score`, `risk_level`(LOW/MEDIUM/HIGH), 세부 `signals`(cvss_norm, epss_score, typo_flag, staleness_score 등)
- 상세 산식 및 스키마 초안: `docs/design/02-risk-analyzer.md` 참고

## 참고자료

- `study_week1/architecture.html` — Risk Analyzer 섹션, "패키지 위험도 × 에이전트 권한" 공식
- `study_week1/README.md` — CVE/CVSS/타이포스쿼팅 용어 정리, 파이프라인 내 위치
- `study_week1/raw/06_jfrog_typosquatting.md`, `07_checkmarx_colorama.md` — 타이포스쿼팅 실제 사례
- `resources/curated_list.md` F 섹션(타이포스쿼팅·의존성 컨퓨전), W 섹션(EPSS/CVSS/NVD API, Risk Analyzer 필독)
- FIRST/CrowdStrike EPSS 설명, Intruder "EPSS vs CVSS" — CVSS 한계 보완용 실제 악용 확률 지표 개념
- `GIT_POLICY.md` — 스키마 변경 시 CODEOWNERS 승인 규칙

## 하위 이슈

(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)


# ============================================================
# 원본: docs/epics/03-ml-detector.md
# ============================================================

# [Epic] ML 이상탐지 (ml-detector) 모듈 구축

담당: ML탐지

## 목표

Dependency Collector가 만든 SBOM/의존성 메타데이터를 입력받아, Risk Analyzer의 규칙 기반 탐지가 놓치는 **신규·변종 악성 패키지**를 메타데이터/텍스트/코드 특징 기반 분류 모델(Random Forest 베이스라인)로 탐지하고, 그 결과를 `ml_result.schema.json` 형식으로 Attack Path Engine에 전달한다.

## 범위

**포함**
- PyPI 메타데이터/배포 파일 기반 feature extraction 파이프라인
- 공개 악성 패키지 데이터셋(DataDog `malicious-software-packages-dataset`, `lxyeternal/pypi_malregistry`) + 정상 패키지 목록으로 학습 데이터 구성
- Random Forest 분류 모델 학습·평가·저장
- Collector 출력을 입력으로 받아 추론 후 결과 JSON을 생성하는 inference 스크립트
- `schemas/ml_result.schema.json` 초안 작성 및 Attack Path Engine 담당자 리뷰 반영

**제외 (이번 학기 범위 밖)**
- npm/RubyGems 등 PyPI 외 생태계 지원
- 딥러닝/GNN 기반 고급 모델(참고자료에만 기록, 시간 남으면 향후 확장)
- 실시간/온라인 학습(모델 재학습은 수동 배치로 진행)

## 완료 조건 (Acceptance Criteria)

- [ ] Feature extraction 스크립트가 Collector 출력(SBOM)에서 표 형태 feature vector를 생성한다
- [ ] 학습 데이터셋(악성+정상)이 `ml-detector/data/`에 구성되고 다운로드/전처리 스크립트가 재현 가능하다
- [ ] Random Forest 모델이 hold-out test set에서 **Recall(탐지율) ≥ 90%, False Positive Rate < 10%**를 만족한다 (미달 시 하이퍼파라미터/피처 조정 이력을 문서화)
- [ ] 추론 스크립트가 임의의 Collector 출력에 대해 `ml_result.schema.json` 형식의 JSON을 생성한다
- [ ] `schemas/ml_result.schema.json`이 Attack Path Engine 담당자의 승인(CODEOWNERS 리뷰)을 받아 병합된다
- [ ] `ml-detector/README.md`에 실행 방법·모델 재학습 방법이 정리된다

## 입력/출력 인터페이스

- **입력**: `schemas/collector_output.schema.json`을 따르는 Collector의 SBOM/의존성 목록 JSON (패키지명, 버전, 배포 파일 위치/해시, PyPI 메타데이터 포함 여부는 Collector 담당과 확정 필요)
- **출력**: `schemas/ml_result.schema.json`(DRAFT, `docs/design/03-ml-detector.md` 참고) — 패키지별 flag 여부, confidence score, 트리거된 feature 목록. Attack Path Engine이 Risk Analyzer의 위험 점수와 함께 그래프 구축에 사용

## 참고자료

- 설계 상세: [`docs/design/03-ml-detector.md`](../design/03-ml-detector.md)
- 논문: [A Machine Learning-Based Approach For Detecting Malicious PyPI Packages (arXiv:2412.05259)](https://arxiv.org/pdf/2412.05259)
- 데이터셋: [DataDog/malicious-software-packages-dataset](https://github.com/DataDog/malicious-software-packages-dataset), [lxyeternal/pypi_malregistry](https://github.com/lxyeternal/pypi_malregistry)
- 튜토리얼: [DataCamp — Random Forest Classification in Python](https://www.datacamp.com/tutorial/random-forests-classifier-python), [Analytics Vidhya — Isolation Forest](https://www.analyticsvidhya.com/blog/2021/07/anomaly-detection-using-isolation-forest-a-complete-guide/)
- 배경: `study_week1/README.md`, `study_week1/architecture.html`(#ml 섹션), `resources/curated_list.md` E/K/Y 섹션
- Git 정책: `GIT_POLICY.md` (스키마 변경 시 CODEOWNERS 승인 규칙)

## 하위 이슈

(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)


# ============================================================
# 원본: docs/epics/04-attack-path.md
# ============================================================

# Epic: Attack Path Engine 구축

담당: 공격경로 / 시각화

## 목표

Risk Analyzer의 위험 점수와 ML의 이상탐지 결과, 에이전트 권한 정보를 하나의 그래프로 연결해 "의존성 → 에이전트 → 권한 → 공격경로"를 추적하고, 개별로는 저위험인 이슈들이 결합해 실제로 악용 가능한 경로("toxic combination")를 식별·우선순위화한다. 최종적으로 이 경로를 의도적으로 취약하게 만든 테스트 에이전트(PoC)에서 재현해 침해 시나리오를 검증한다.

## 범위

- NetworkX 기반 그래프 빌더: Risk Analyzer/ML JSON → `DiGraph` 변환
- 노드 타입(Package, Agent, Permission, Asset) / 엣지 타입(depends_on, grants, exposes 등) 스키마 확정
- 가중치 기반 경로 탐색 알고리즘(`shortest_simple_paths` 등) 및 toxic combination 판정 로직
- 경로 우선순위화(path_score 계산, 병목 노드 탐지)
- 침해 시나리오 자연어 설명 생성
- 취약 테스트 에이전트(PoC) 제작 및 경로 재현 검증
- `schemas/attack_graph.schema.json` 초안 작성 및 Dashboard 담당과 리뷰·확정
- Risk Analyzer·ML 담당과 입력 필드 계약 확정

**범위 제외**: 실제 Neo4j 등 그래프 DB 도입, 프로덕션급 대규모 그래프 최적화, 실시간 그래프 갱신(본 프로젝트는 배치 처리 기준)

## 완료조건

- [ ] Risk Analyzer·ML의 출력 스키마를 입력받아 그래프를 정상적으로 구성한다
- [ ] 최소 1개 이상의 toxic combination 경로를 실제 테스트 데이터(또는 PoC 에이전트)에서 식별한다
- [ ] 경로별 `path_score`로 우선순위가 매겨지고, 상위 경로에 대해 자연어 시나리오 설명이 생성된다
- [ ] `schemas/attack_graph.schema.json`이 Dashboard 담당의 승인을 받아 병합된다 (GIT_POLICY 3항 CODEOWNERS 규칙)
- [ ] PoC 취약 에이전트에서 설계한 경로가 실제로 재현됨을 시연한다

## 입력/출력 인터페이스

**입력 (Risk Analyzer)**: `purl`, `package_risk_score`(0~10), `vulnerability_ids`, `is_externally_reachable`, 패키지-에이전트 매핑(`agent_id`)

**입력 (ML 이상탐지)**: `agent_id`, `anomaly_score`(0~1), `anomaly_type`, 탐지 시각

**입력 (공통/Collector)**: 에이전트별 권한 목록(권한 타입, 대상 자산) — 현재 스키마 미확정, Collector·Risk Analyzer 담당과 협의 필요

**출력 (→ Dashboard)**: `schemas/attack_graph.schema.json` — 노드 배열, 엣지 배열, 우선순위화된 경로 배열(`path_score`, `is_toxic_combination`, `scenario` 텍스트 포함). 상세 초안은 `docs/design/04-attack-path.md` 참고.

## 참고자료

- `study_week1/architecture.html` — Attack Path Engine 섹션, Wiz 4단계 방법론(자산·위험 발견 → 그래프 매핑 → 경로 식별 → 우선순위화)
- `study_week1/README.md` — CNAPP, 공격경로/공격벡터/공격표면 구분
- `resources/curated_list.md` I절 — Wiz, PuppyGraph, Neo4j GraphGist, BloodHound 기반 그래프 예제
- `resources/curated_list.md` U절 — OpenSSF GUAC (SBOM+SLSA+취약점을 그래프 DB로 통합하는 실제 사례)
- `study_week1/raw/05_wiz_attack_path_analysis.md` — 원문
- `docs/design/04-attack-path.md` — 본 모듈 기술 설계 문서
- `GIT_POLICY.md` — 스키마 변경 시 CODEOWNERS 승인 규칙

## 하위 이슈

(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)


# ============================================================
# 원본: docs/epics/05-dashboard.md
# ============================================================

# [Epic] Dashboard — 위험자산·공격경로 웹 시각화

담당: 공격경로/시각화 · 최종 수정: 2026-09-06

## 목표

Attack Path Engine이 만든 `attack_graph.json`(의존성→에이전트→권한→공격경로 그래프)을 지도교수·쿤텍 자문단이 웹 브라우저에서 바로 열어 "어떤 자산이 위험하고 왜 위험한지, 그 위험이 어떤 경로로 실제 피해까지 이어지는지"를 직관적으로 판단할 수 있는 인터랙티브 대시보드를 만든다. 파이프라인의 마지막 단계로, 이 프로젝트 전체의 설득력을 좌우하는 화면이다.

## 범위

- Cytoscape.js 기반 그래프 뷰(노드 타입별 스타일링, `dagre`/`cola` 레이아웃 전환)
- risk_score 기준 필터링(슬라이더) 및 검색 기능
- 위험 자산/공격경로 리스트 뷰(정렬 가능한 테이블) ↔ 그래프 하이라이트 연동
- 노드/경로 클릭 시 상세 정보 패널(CVE, 버전, 권한명, 이상탐지 점수 등)
- 얇은 FastAPI 백엔드: `data/<run_id>/attack_graph.json` 읽기 + 스키마 검증 + 정적 파일 서빙
- PNG 내보내기(보고서용 캡처)
- **범위 밖**: 실시간 스트리밍 업데이트, 다중 사용자 인증/권한 관리, 그래프 데이터 자체의 재계산(위험 점수는 Attack Path Engine이 이미 계산해서 넘겨줌 — Dashboard는 표시만 담당)

## 완료 조건

- [ ] `schemas/attack_graph.schema.json`을 만족하는 샘플 JSON으로 그래프가 렌더링된다
- [ ] risk_score 슬라이더로 노드/엣지 필터링이 동작한다
- [ ] 위험 경로 리스트에서 항목 클릭 시 해당 경로가 그래프에서 하이라이트된다
- [ ] 노드 클릭 시 우측 패널에 상세 정보(타입별 필드)가 표시된다
- [ ] `dashboard/tests/test_schema_validation.py`가 `schemas/attack_graph.schema.json` 검증을 통과한다
- [ ] `python -m uvicorn` 한 줄 명령으로 로컬 실행 가능(빌드 도구 불필요)
- [ ] 지도교수/쿤텍 대상 시연에서 "노드 클릭 → 상세정보 → 경로 하이라이트"까지 데모 가능

## 입력 인터페이스

- **입력원**: Attack Path Engine (`attack-path/` 모듈)
- **입력 파일**: `data/<run_id>/attack_graph.json` (`schemas/attack_graph.schema.json` 준수)
- **필수 필드**(자세한 내용은 `docs/design/05-dashboard.md` 5절 참고):
  - `nodes[].id`, `type`(dependency/agent/permission/path_step), `label`, `risk_score`(0-100, Dashboard가 재계산하지 않음), `attributes`(CVE 목록, 패키지 버전, 권한명 등)
  - `edges[].id`, `source`, `target`, `type`
  - `paths[].path_id`, `node_sequence`, `edge_sequence`, `overall_risk_score`, `description`(사람이 읽을 한 줄 요약)
- **공통 메타**: `schema_version`, `run_id`, `generated_at`, `source_module` (00-overall.md 제안 규칙 준수)
- Dashboard는 이 파일 하나만 입력으로 받으며, 다운스트림 소비자가 없는 파이프라인의 종착 모듈이다(`GIT_POLICY.md` 참고).

## 참고자료

- `study_week1/architecture.html` — Dashboard 섹션(#dash), Figure 1 전체 아키텍처
- `resources/curated_list.md` — J절 "Dashboard 담당 — 시각화 라이브러리" (Cytoscape.js 공식 문서, 2026 비교 가이드)
- `docs/design/00-overall.md` — 파일 기반 핸드오프 원칙, 스키마 공통 메타 필드 제안
- `docs/design/05-dashboard.md` — 본 모듈 상세 설계(스택 선정 근거, INPUT 스키마, 파일 구조)
- `GIT_POLICY.md` — 모노레포 구조, CODEOWNERS, 스키마 변경 승인 규칙

## 하위 이슈

(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)


# ============================================================
# 원본: docs/epics/06-open-decisions.md
# ============================================================

# [Epic] 팀 차원 결정 사항 정리 (총괄 소유)

`docs/design/_cross_review_questions.md` §"총괄(PM)이 팀 차원에서 정리해야 할 것"에서 나온 항목들. 모듈 하나에 속하지 않고 전체 파이프라인에 영향을 주므로 총괄이 결정을 조율합니다. `docs/contracts/epic_schema.md` 형식이 아니라 **결정 기록(decision record)** 형식을 씁니다 — 구현 작업이 아니라 "선택"이 산출물이기 때문입니다.

## 결정 1 — 공통 메타 필드(`run_id`, `schema_version`) 4개 스키마 전부 강제 여부

**배경**: 현재 4개 `schemas/*.json` 모두 `schema_version`은 이미 갖고 있음. `run_id`는 `collector_output.schema.json`에는 있지만 나머지 3개에 필수로 못박혀 있는지 문서상 불명확.

**옵션**:
- (A) 4개 스키마 전부 `run_id`/`schema_version`을 required로 강제 → 파이프라인 재현성·디버깅 용이, 스키마 변경 필요
- (B) Collector만 `run_id` 생성, 나머지는 파일명/디렉터리 구조로 같은 실행을 추적(예: `data/<run_id>/`) → 스키마 변경 불필요, 대신 파일 배치 규칙을 별도 문서화해야 함

**권장안**: (A). 파일이 서로 흩어져도(S3 등) 실행을 역추적할 수 있어야 하고, 필드 하나 추가하는 비용이 훨씬 낮음.

**영향받는 모듈**: 전체 (schemas/ 4개 파일)
**결정 필요 시점**: M2(파이프라인 통합 테스트 이전)
**결정자**: 총괄 + 4개 모듈 담당자 전원 승인 (CODEOWNERS 규칙과 동일)

---

## 결정 2 — `pipeline/` 오케스트레이션 코드 소유권

**배경**: `00-overall.md` §2에서 "파일 기반 핸드오프 + 얇은 CLI"로 모듈을 연결한다고 했지만, 이 CLI/오케스트레이션 스크립트 자체를 누가 만들고 유지보수할지 미정.

**옵션**:
- (A) 총괄이 `pipeline/`을 전담 소유 (5개 모듈 담당자는 각자 모듈 CLI만 책임)
- (B) 각 모듈 담당자가 자기 모듈을 호출하는 부분만 기여, 총괄은 통합만

**권장안**: (B). 총괄 혼자 5개 모듈의 입출력을 다 알기 어렵고, 각 담당자가 자기 모듈의 CLI 인터페이스(`docs/design/0X-*.md` §"파일 구조")를 가장 잘 앎.

**영향받는 모듈**: 전체
**결정 필요 시점**: M3 (파이프라인 최초 통합)
**결정자**: 총괄

---

## 결정 3 — 중간 산출물(`data/`) 저장 위치: 로컬 vs 클라우드(S3 등)

**배경**: 모듈 간 핸드오프 파일(`data/<run_id>/collector_output.json` 등)을 로컬 디스크에만 둘지, 팀원 간 공유가 필요해 클라우드에 올릴지 미정. `.gitignore`에 이미 `data/`는 제외되어 있음(용량/보안).

**옵션**:
- (A) 로컬 전용 — 각자 자기 컴퓨터에서 전체 파이프라인을 돌려봄. 설정 단순, 팀원 간 결과 공유 어려움
- (B) 공유 스토리지(S3 등) — 한 명이 돌린 Collector 결과를 다른 모듈 담당자가 바로 씀. 설정 복잡, 비용/계정 관리 필요

**권장안**: 초기(M1~M3)는 (A)로 시작 — AI 구현 검증 단계에서는 로컬로 충분. 병렬 개발이 본격화되는 M4 이후 필요성 재검토.

**영향받는 모듈**: 전체
**결정 필요 시점**: M3 이전 (재검토는 M4)
**결정자**: 총괄 + 팀 전체 합의

---

## 참고: 이미 결정 완료된 항목 (재론의 불필요)

- **Permission 데이터 출처** — `docs/design/04-attack-path.md` "확정 사항 (교차검토 반영)" 1번에서 이미 확정 (Collector가 스캔, Attack Path Engine이 스키마 소유). 이 문서에서 다시 열지 않음.
- 나머지 교차검토 질문(1~15번)도 각 모듈 설계 문서의 "확정 사항" 섹션에서 전부 답변 완료.

## 하위 이슈

(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)

