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
