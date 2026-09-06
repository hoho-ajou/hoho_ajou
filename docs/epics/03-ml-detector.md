# [Epic] ML 이상탐지 (ml-detector) 설계 문서 완성

담당: ML탐지

## 목표

Dependency Collector가 만든 SBOM/의존성 메타데이터를 입력받아, Risk Analyzer의 규칙 기반 탐지가 놓치는 **신규·변종 악성 패키지**를 메타데이터/텍스트/코드 특징 기반 분류 모델(Random Forest 베이스라인)로 탐지하는 파이프라인의 **설계를 AI 구현 가능한 수준까지** 완성한다. 실제 모델 학습·추론 코드 작성은 이 Epic의 범위가 아니다.

## 범위

**포함 (`docs/design/03-ml-detector.md` 심화)**
- PyPI 메타데이터/배포 파일 기반 feature extraction 로직과 각 feature의 정의·계산식
- 공개 악성 패키지 데이터셋(DataDog `malicious-software-packages-dataset`, `lxyeternal/pypi_malregistry`) + 정상 패키지 목록으로 학습 데이터를 구성하는 절차
- Random Forest 분류 모델의 학습·평가 절차(하이퍼파라미터, 평가 지표 기준값 포함)
- Collector 출력을 입력으로 받아 추론 결과 JSON을 생성하는 inference 절차의 함수 시그니처
- `schemas/ml_result.schema.json` 필드와 모델 출력 매핑 확정

**제외 (이번 학기 범위 밖)**
- npm/RubyGems 등 PyPI 외 생태계 지원
- 딥러닝/GNN 기반 고급 모델(참고자료에만 기록, 시간 남으면 향후 확장)
- 실시간/온라인 학습(모델 재학습은 수동 배치로 진행)
- **실제 모델 학습·추론 코드 구현** — 설계 확정 이후 단계

## 완료 조건 (Acceptance Criteria)

- [ ] Feature extraction 로직의 함수 시그니처와 각 feature 정의가 `docs/design/03-ml-detector.md`에 표로 정리되어 있다
- [ ] 학습 데이터셋 구성 절차(다운로드처, 전처리 단계)가 재현 가능한 수준으로 문서화되어 있다
- [ ] Random Forest 모델의 목표 평가 지표(Recall ≥ 90%, False Positive Rate < 10% 등)와 미달 시 대응 방침이 명시되어 있다
- [ ] 추론 절차의 입력→출력 예시(Collector 출력 스니펫 → `ml_result.schema.json` 스니펫)가 최소 1개 있다
- [ ] "feature 추출 실패", "학습 데이터에 없는 신규 패키지" 등 최소 2개 엣지케이스가 표로 정리되어 있다
- [ ] `schemas/ml_result.schema.json`이 Attack Path Engine 담당자의 승인(CODEOWNERS 리뷰)을 받아 확정된다

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
