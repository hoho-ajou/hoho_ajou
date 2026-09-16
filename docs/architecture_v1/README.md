# AASM Architecture v1

전체 파이프라인(Collector → Risk Analyzer/ML → Attack Path Engine → Dashboard)을 구현하는 데 필요한 문서를 한 디렉토리에 평평하게 모은 스냅샷입니다. LLM에게 구현을 맡길 때는 이 폴더 하나만 넘기면 됩니다.

기술 설계·데이터 계약의 SSOT입니다(예전에는 `docs/design/`, `docs/contracts/`로 흩어져 있었으나 이 폴더로 합쳤습니다). 중복 방지를 위해 역할 정의(GitHub Issue #9~12 자체가 원본)와 결정 기록(`docs/review/decisions.md`)은 여기 포함하지 않습니다 — 각 모듈 설계 문서의 "확정 사항" 절에 관련 결정이 이미 요약되어 있습니다.

## 구성

- `01-overall.md` — 전체 파이프라인 오케스트레이션, 공통 컨벤션
- `02-architecture-diagram.md` — 전체 흐름 Mermaid 도면
- `03-data-contracts.md` — 스키마 4개의 원본 + 필드 설명 + 사용처를 한 문서에 통합
- `04-sample-dataset.md` — 전 모듈 공통 예시 시나리오(스키마 검증 통과 확인됨)
- `05-collector.md` — Dependency Collector 기술 설계
- `06-risk-analyzer.md` — Risk Analyzer 기술 설계
- `07-ml-detector.md` — ML 이상탐지 기술 설계
- `08-attack-path.md` — Attack Path Engine 기술 설계
- `09-dashboard.md` — Dashboard 기술 설계

## 읽는 순서

1. `01-overall.md` → `02-architecture-diagram.md`
2. `03-data-contracts.md`, `04-sample-dataset.md` (모듈 간 실제 연결)
3. 필요한 모듈의 `05-collector.md` ~ `09-dashboard.md`
