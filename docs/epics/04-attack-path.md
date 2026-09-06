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
