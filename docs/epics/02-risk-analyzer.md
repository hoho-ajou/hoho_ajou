# [Epic] Risk Analyzer 설계 문서 완성

## 목표

Dependency Collector가 만든 SBOM·의존성 목록을 입력받아, 패키지별로 "패키지 자체 위험도(CVE/CVSS/EPSS + 타이포스쿼팅 + 유지보수 상태) × 에이전트 권한 가중치" 공식으로 위험 점수를 산출하는 로직의 **설계를 AI 구현 가능한 수준까지** 완성한다. 실제 스코어링 파이프라인 코드 작성은 범위 밖이다.

## 범위

`docs/design/02-risk-analyzer.md`를 심화 작성한다:
- CVSS 정규화, EPSS 결합, 타이포스쿼팅 탐지, staleness 점수, 권한 가중치 — 5개 계산 로직의 공식과 시그니처
- 최종 위험 점수·등급 산출 공식과 `schemas/risk_score.schema.json` 필드 매핑

**범위 밖**: ML 기반 탐지(ML 이상탐지 담당), 그래프 구성(Attack Path Engine 담당), combosquatting 등 고급 규칙, **실제 코드 구현**

## 완료조건

- [ ] 5개 계산 로직 각각의 함수 시그니처와 공식이 명시되어 있다
- [ ] 각 계산 로직마다 최소 1개의 구체적 입력값 → 출력값 예시가 있다
- [ ] 타이포스쿼팅 탐지 규칙이 알려진 사례(colorama/colorizr류)로 검증되어 있다
- [ ] 최소 3개 엣지케이스가 표로 정리되어 있다
- [ ] `schemas/risk_score.schema.json`과 설계 문서의 공식·필드가 100% 일치하며 Attack Path Engine 승인 완료
- [ ] Collector 출력에서 필요한 입력 필드가 Collector 설계 문서와 교차 확인되어 불일치가 없다

## 공통계약

- `docs/contracts/sample_dataset.md` — 전 모듈 공통 예시 시나리오
- `docs/contracts/interface_map.md` — 필드 단위 흐름 정리
- 입력: `schemas/collector_output.schema.json`
- 출력: `schemas/risk_score.schema.json` — CODEOWNERS 대상 (Attack Path Engine 승인 필요)

## 담당 문서

`docs/design/02-risk-analyzer.md`

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
