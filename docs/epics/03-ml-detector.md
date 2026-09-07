# [Epic] ML 이상탐지 (ml-detector) 설계 문서 완성

## 목표

Dependency Collector가 만든 SBOM/의존성 메타데이터를 입력받아, Risk Analyzer의 규칙 기반 탐지가 놓치는 **신규·변종 악성 패키지**를 분류 모델(Random Forest 베이스라인)로 탐지하는 파이프라인의 **설계를 AI 구현 가능한 수준까지** 완성한다. 실제 모델 학습·추론 코드 작성은 범위 밖이다.

## 범위

`docs/design/03-ml-detector.md`를 심화 작성한다:
- Feature extraction 로직과 각 feature의 정의·계산식
- 학습 데이터셋 구성 절차(공개 악성 패키지 데이터셋 + 정상 패키지)
- Random Forest 학습·평가 절차(하이퍼파라미터, 평가 지표 기준값)
- 추론 절차의 함수 시그니처와 `schemas/ml_result.schema.json` 필드 매핑

**범위 밖**: PyPI 외 생태계, 딥러닝/GNN 고급 모델, 실시간/온라인 학습, **실제 모델 학습·추론 코드 구현**

## 완료조건

- [ ] Feature extraction 함수 시그니처와 각 feature 정의가 표로 정리되어 있다
- [ ] 학습 데이터셋 구성 절차가 재현 가능한 수준으로 문서화되어 있다
- [ ] 목표 평가 지표(Recall/FPR 등)와 미달 시 대응 방침이 명시되어 있다
- [ ] 추론 절차의 입력→출력 예시가 최소 1개 있다
- [ ] 최소 2개 엣지케이스가 표로 정리되어 있다
- [ ] `schemas/ml_result.schema.json`이 Attack Path Engine 승인을 받아 확정된다

## 공통계약

- `docs/contracts/sample_dataset.md` — 전 모듈 공통 예시 시나리오
- `docs/contracts/interface_map.md` — 필드 단위 흐름 정리
- 입력: `schemas/collector_output.schema.json`
- 출력: `schemas/ml_result.schema.json` — CODEOWNERS 대상 (Attack Path Engine 승인 필요)

## 담당 문서

`docs/design/03-ml-detector.md`

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
