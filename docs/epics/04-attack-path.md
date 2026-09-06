# Epic: Attack Path Engine 설계 문서 완성

담당: 공격경로 / 시각화

## 목표

Risk Analyzer의 위험 점수와 ML의 이상탐지 결과, 에이전트 권한 정보를 하나의 그래프로 연결해 "의존성 → 에이전트 → 권한 → 공격경로"를 추적하고, 개별로는 저위험인 이슈들이 결합해 실제로 악용 가능한 경로("toxic combination")를 식별·우선순위화하는 로직의 **설계를 AI 구현 가능한 수준까지** 완성한다. PoC 취약 에이전트 제작·실제 그래프 빌더 코드 구현은 이 Epic의 범위가 아니다.

## 범위

**포함 (`docs/design/04-attack-path.md` 심화)**
- NetworkX 기반 그래프 빌더의 함수 시그니처: Risk Analyzer/ML JSON → `DiGraph` 변환 절차
- 노드 타입(Package, Agent, Permission, Asset) / 엣지 타입(depends_on, grants, exposes 등) 스키마 확정 (완료 — `docs/design/_cross_review_questions.md` 참고)
- 가중치 기반 경로 탐색 알고리즘(`shortest_simple_paths` 등)과 toxic combination 판정 로직을 의사코드 수준으로 서술
- 경로 우선순위화(`path_score` 계산식, 병목 노드 탐지 기준) 공식화
- 침해 시나리오 자연어 설명을 생성하는 규칙/템플릿 설계
- PoC 취약 에이전트로 검증할 시나리오 목록 설계(제작 자체는 범위 밖)
- `schemas/attack_graph.schema.json` 필드 확정 및 Dashboard 담당과 리뷰 (완료)
- Risk Analyzer·ML 담당과 입력 필드 계약 확정 (완료)

**범위 제외**: 실제 Neo4j 등 그래프 DB 도입, 프로덕션급 대규모 그래프 최적화, 실시간 그래프 갱신(본 프로젝트는 배치 처리 기준), **그래프 빌더·PoC 에이전트 실제 코드/구현물 제작**

## 완료조건

- [ ] 그래프 빌더 함수 시그니처와 노드/엣지 생성 규칙이 `docs/design/04-attack-path.md`에 명시되어 있다
- [ ] 경로 탐색·toxic combination 판정 알고리즘이 의사코드 수준으로 서술되어 있고, 최소 1개의 구체적 입력 그래프 → 출력 경로 예시가 있다
- [ ] `path_score` 계산 공식이 명시되어 있고 예시로 검증되어 있다
- [ ] "그래프에 고립 노드만 있는 경우", "toxic combination이 없는 경우" 등 최소 2개 엣지케이스가 표로 정리되어 있다
- [ ] `schemas/attack_graph.schema.json`과 설계 문서의 필드가 100% 일치하며 Dashboard 담당의 승인을 받아 확정된다 (GIT_POLICY 3항 CODEOWNERS 규칙)
- [ ] PoC 검증 시나리오 목록(어떤 취약점 조합을 어떤 순서로 재현할지)이 설계 문서에 정리되어 있다 — 실제 제작은 후속 단계

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
