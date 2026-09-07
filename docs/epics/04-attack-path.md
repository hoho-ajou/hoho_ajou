# [Epic] Attack Path Engine 설계 문서 완성

## 목표

Risk Analyzer의 위험 점수와 ML의 이상탐지 결과, 에이전트 권한 정보를 하나의 그래프로 연결해 "의존성 → 에이전트 → 권한 → 공격경로"를 추적하고, 저위험 이슈들이 결합해 실제로 악용 가능한 경로("toxic combination")를 식별·우선순위화하는 로직의 **설계를 AI 구현 가능한 수준까지** 완성한다. PoC 제작·실제 코드 구현은 범위 밖이다.

## 범위

`docs/design/04-attack-path.md`를 심화 작성한다:
- NetworkX 기반 그래프 빌더 함수 시그니처
- 경로 탐색·toxic combination 판정 알고리즘 의사코드
- 경로 우선순위화(`path_score`) 공식화
- 침해 시나리오 자연어 설명 생성 규칙
- PoC 검증 시나리오 목록 설계(제작 자체는 범위 밖)

**범위 밖**: 그래프 DB 도입, 대규모 그래프 최적화, 실시간 갱신, **그래프 빌더·PoC 에이전트 실제 구현**

## 완료조건

- [ ] 그래프 빌더 함수 시그니처와 노드/엣지 생성 규칙이 명시되어 있다
- [ ] 경로 탐색·toxic combination 알고리즘이 의사코드 수준으로 서술되어 있고, 입력→출력 예시가 최소 1개 있다
- [ ] `path_score` 계산 공식이 명시되고 예시로 검증되어 있다
- [ ] 최소 2개 엣지케이스가 표로 정리되어 있다
- [ ] `schemas/attack_graph.schema.json`과 설계 문서의 필드가 100% 일치하며 Dashboard 승인을 받아 확정된다
- [ ] PoC 검증 시나리오 목록이 설계 문서에 정리되어 있다

## 공통계약

- `docs/contracts/sample_dataset.md` — 전 모듈 공통 예시 시나리오
- `docs/contracts/interface_map.md` — 필드 단위 흐름 정리
- 입력: `schemas/risk_score.schema.json`, `schemas/ml_result.schema.json`, `collector_output.schema.json`의 `agent.permissions[]`
- 출력: `schemas/attack_graph.schema.json` — CODEOWNERS 대상 (Dashboard 승인 필요)

## 담당 문서

`docs/design/04-attack-path.md`

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
