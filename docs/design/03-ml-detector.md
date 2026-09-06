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
