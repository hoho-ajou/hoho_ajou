# 판정 엔진 스코어링 로직 (초안)

MVP는 스펙 요청대로 **룰 기반 + OSV 조회**로 시작합니다(임베딩/ML 분류기는 2단계 확장 — `INTERFACES.md` 참고). `scan_engine.py`의 `WEIGHTS`/`compute_verdict`가 이 문서의 구현체입니다.

## 가중치 (합 = 1.0)

| 요인 | 가중치 | 근거 |
|---|---|---|
| `vuln` (OSV 알려진 취약점) | 0.30 | 가장 객관적인 신호 — 이미 검증된 CVE라 오탐 위험이 제일 낮음 |
| `entropy` (코드 엔트로피) | 0.15 | 난독화/인코딩된 페이로드 탐지 |
| `keyword` (위험 API 사용 빈도) | 0.15 | eval/exec/subprocess/pickle 등 — 정상 코드에도 나타날 수 있어 단독으론 약함 |
| `install_hook` (커스텀 설치훅 존재) | 0.15 | 설치 시점 코드 실행 가능성 |
| `typosquat` (인기 패키지 대비 편집거리) | 0.15 | 이름 사칭 |
| `reputation` (신규 등록/README 없음/maintainer 없음) | 0.10 | 약한 보조 신호, 정상 신규 패키지도 해당될 수 있어 가중치 최저 |

## 임계값

- `score < 0.25` → **ALLOW**
- `0.25 <= score < 0.6` → **NEEDS_HUMAN_REVIEW**
- `score >= 0.6` → **BLOCK**

## 하드 룰 (가중합을 오버라이드)

1. **OSV 심각도 CRITICAL** → 총점과 무관하게 무조건 BLOCK. 다른 요인들이 아무리 낮아도, 알려진 치명적 취약점은 소프트 스코어링으로 완화되면 안 됨.
2. **install_hook 존재 + 위험 키워드 검출 동시 발생** → 최소 NEEDS_HUMAN_REVIEW로 상향. (AASM 논의에서 나온 "행위 체인" 개념 — 개별 신호보다 "설치 시점 코드 실행 + 위험 API 사용"의 조합이 훨씬 강한 신호라는 근거)

## 알려진 한계 (정직하게 명시)

- `keyword` 요인은 오탐이 잦습니다 — 정상 라이브러리도 내부적으로 `pickle`/`socket`을 씀(실제 테스트에서 `requests` 패키지가 키워드 35회 검출됨에도 ALLOW로 나온 건, 가중치 0.15에 클램프(/10)를 걸어놔서 개별 요인만으론 임계값을 못 넘게 설계했기 때문). 실제 운영 전 오탐률 실측 필요.
- `typosquat` 체크는 지금 하드코딩된 30개 남짓의 샘플 목록만 씁니다 — 실전에는 `hugovk/top-pypi-packages` 같은 전체 top-N 리스트로 교체해야 함(Risk Analyzer/R2가 이미 이 작업을 하고 있다면 중복 방지를 위해 그쪽 로직을 재사용하는 게 나을 수 있음).
- 가중치 숫자 자체는 추정치입니다. 실제 라벨링된 데이터(DataDog malicious-software-packages-dataset 등)로 검증 후 조정 필요.
