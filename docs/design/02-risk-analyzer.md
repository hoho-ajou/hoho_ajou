# Risk Analyzer 기술 설계 문서

> 담당: 위험분석 · 관련: `study_week1/architecture.html`(패키지 위험도 × 에이전트 권한), `study_week1/README.md`(CVE/CVSS/타이포스쿼팅 용어), `resources/curated_list.md` F(타이포스쿼팅)·W(EPSS/CVSS/NVD)

## 1. 배경 및 설계 목표

기존 학습자료는 "CVSS 참고", "패키지 위험도 × 에이전트 권한"이라는 **개념**만 제시하고 구체적 산식이 없다. 이 문서는 그 공백을 메우기 위한 실제 스코어링 알고리즘을 정의한다.

리서치 결과 두 가지를 반영했다:
- **타이포스쿼팅 임계값**: 실제 도구(anti-typosquatting류)는 인기 패키지 top-N(보통 top 10,000) 대비 Levenshtein distance ≤ 2를 기본 임계값으로 쓴다 — 과거 40건 타이포스쿼팅 사례 중 18건이 거리 2 이하였다는 근거. 단, 단순 거리 임계값만 쓰면 오탐이 많다는 지적이 있어 낮은 다운로드 수·최근 등록일 같은 보조 신호와 AND 조건으로 묶는다.
- **CVSS × EPSS 결합 주의점**: "CVSS 점수 × EPSS 확률"처럼 서수(ordinal)와 확률을 곱하는 단순 결합은 통계적으로 부적절하다는 지적이 있음(Cloudsmith/Intruder 자료). 대신 정규화(0~1) 후 가중합(weighted sum)으로 결합하고, EPSS는 "실제 악용 확률"이라는 별도 축으로 취급한다.

## 2. 스코어링 알고리즘

### 2.1 패키지 자체 위험도 (`package_risk`, 0~1)

```
package_risk = w1 * cvss_norm
             + w2 * epss_score
             + w3 * typo_flag
             + w4 * staleness_score

기본 가중치: w1=0.35, w2=0.30, w3=0.20, w4=0.15  (합 1.0, 조정 가능한 설정값)
```

- `cvss_norm = max(CVSS_base_score) / 10.0` — 패키지에 걸린 알려진 CVE 중 최고 심각도. CVE 없으면 0.
- `epss_score` — NVD/FIRST EPSS API 값(0~1) 그대로 사용. 여러 CVE가 있으면 최댓값.
- `typo_flag` (0/0.5/1 단계형) — 아래 2.2 알고리즘 결과.
- `staleness_score` — 아래 2.3 알고리즘 결과.

CVE가 전혀 없는 패키지도 typo_flag·staleness만으로 위험 신호를 낼 수 있게 설계(무CVE ≠ 무위험, xz-utils 사례 참고).

### 2.2 타이포스쿼팅 탐지 (`typo_flag`)

1. PyPI 인기 패키지 top-5,000 리스트(예: PyPI 다운로드 통계 기반)를 사전에 확보.
2. 대상 패키지명과 top-5,000 각 이름 사이 Levenshtein distance 계산(`python-Levenshtein` 등).
3. 최소 거리 `d_min`에 대해:
   - `d_min == 0` (정상 등록된 유명 패키지) → `typo_flag = 0`
   - `1 <= d_min <= 2` **AND** (다운로드 수 하위 or 등록 6개월 이내) → `typo_flag = 1` (고위험)
   - `d_min <= 2`이지만 보조 신호 없음 → `typo_flag = 0.5` (주의, 오탐 가능성 고려)
   - `d_min > 2` → `typo_flag = 0`
4. 대체/문자 치환형(`l`↔`1`, `rn`↔`m` 등 combosquatting) 패턴은 v2에서 정규식 규칙 추가 예정(범위 밖 명시).

### 2.3 유지보수 상태 (`staleness_score`, 0~1)

```
months_since_last_release = (오늘 - last_release_date) / 30
staleness_score = min(1.0, months_since_last_release / 24)   # 24개월 이상 방치 시 1.0

maintainer_count == 1 이면 +0.2 (최대 1.0로 클램프)
```

### 2.4 에이전트 권한 가중치 (`permission_weight`, 1.0~3.0)

Attack Path Engine이 최종 그래프 단계에서 권한을 다루지만, Risk Analyzer는 **패키지가 호출되는 컨텍스트의 권한 등급**만 단순 곱셈 승수로 반영한다(상세 그래프 분석은 하지 않음).

| 권한 등급 | 예시 | weight |
|---|---|---|
| LOW | 순수 계산/포매팅 라이브러리 | 1.0 |
| MEDIUM | 파일시스템 읽기, 네트워크 호출 도구 | 1.8 |
| HIGH | 쉘 실행, API 키/시크릿 접근, 외부 MCP 서버 연동 | 3.0 |

권한 등급은 Collector가 산출한 `external_integrations`(MCP/도구 연동 목록)에서 도출하거나, 없으면 기본값 MEDIUM(1.8) 적용. **(교차검토 반영, Q6)** 권한 목록 자체의 정식 스키마·소유권은 Attack Path Engine이 가지며, Risk Analyzer는 그 스키마를 참조(consume)해 `permission_weight`만 계산한다. `permission_source: "attack_path_engine"`로 입력 출처를 명시한다 (아래 §5 출력 스키마 참고).

### 2.5 최종 위험 점수

```
risk_score = round(package_risk * permission_weight, 3)   # 이론상 0 ~ 3.0
risk_level = LOW (<1.0) / MEDIUM (1.0~2.0) / HIGH (>2.0)
```

## 3. 파일 구조 (`risk-analyzer/`)

```
risk-analyzer/
├── __init__.py
├── main.py                  # 진입점: collector 출력 로드 → 점수화 → risk_score.json 출력
├── config.py                 # 가중치(w1~w4), 임계값, permission_weight 표
├── scorers/
│   ├── cvss_epss.py          # NVD/EPSS API 조회 + 정규화
│   ├── typosquatting.py      # Levenshtein 기반 유사도 탐지
│   ├── staleness.py           # PyPI 메타데이터 기반 유지보수 신호
│   └── permission.py          # 권한 등급 매핑
├── data/
│   └── top_packages.json      # 인기 패키지 top-5000 이름 목록(사전 다운로드)
└── tests/
    └── test_scorers.py
```

## 4. Collector 스키마에 요청하는 INPUT 필드

`schemas/collector_output.schema.json`에 아래 필드가 **반드시** 있어야 함:

- `package.name`, `package.ecosystem` (예: "pypi") — 필수
- `package.version` — CVE 버전 매칭용, 필수
- `package.latest_release_date` (ISO8601) — staleness 계산용
- `package.maintainer_count` (int) — staleness 보정용
- `package.vulnerabilities[]` — 각 항목에 `cve_id`, `cvss_base_score` (Collector가 PyPI JSON API의 `vulnerabilities` 필드에서 이미 수집 가능)
- `package.osv_ids[]` — EPSS 조회 시 CVE ID로 매핑 안 되는 경우 대비
- `external_integrations[]` — 이 패키지가 사용되는 컨텍스트(예: "shell_exec", "network", "mcp_server") — 권한 가중치 산정에 필수. **현재 Collector 산출물에 없다면 신규 요청 필요.**

## 5. 출력 스키마 초안 (`schemas/risk_score.schema.json`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RiskScoreOutput",
  "type": "object",
  "required": ["generated_at", "packages"],
  "properties": {
    "generated_at": { "type": "string", "format": "date-time" },
    "packages": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "version", "ecosystem", "package_risk", "permission_weight", "permission_source", "risk_score", "risk_level", "signals"],
        "properties": {
          "name": { "type": "string" },
          "version": { "type": "string" },
          "ecosystem": { "type": "string" },
          "package_risk": { "type": "number", "minimum": 0, "maximum": 1 },
          "permission_weight": { "type": "number", "minimum": 1.0, "maximum": 3.0 },
          "permission_source": {
            "type": "string",
            "description": "권한 등급 산정에 쓰인 권한 데이터의 출처. Risk Analyzer는 권한 목록을 직접 생성하지 않고 Attack Path Engine 소유 스키마를 참조한다(Q6 결정).",
            "enum": ["attack_path_engine", "default_medium_fallback"]
          },
          "risk_score": { "type": "number", "minimum": 0, "description": "숫자형 원점수(0~3.0). Dashboard 등 정렬/시각화용." },
          "risk_level": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH"], "description": "risk_score를 사람이 읽기 쉬운 등급으로 변환. Attack Path Engine 그래프 노드 라벨/색상용." },
          "signals": {
            "type": "object",
            "properties": {
              "cvss_norm": { "type": "number" },
              "cve_ids": {
                "type": "array",
                "items": { "type": "string" },
                "description": "cvss_norm 계산에 쓰인 원본 CVE ID 목록 (Q8 결정: 정규화값 + 원본 목록 둘 다 포함, Dashboard의 attributes.cve 표시 요구사항(질문 13) 지원)"
              },
              "epss_score": { "type": "number" },
              "typo_flag": { "type": "number", "enum": [0, 0.5, 1] },
              "typo_nearest_match": { "type": ["string", "null"] },
              "staleness_score": { "type": "number" },
              "months_since_last_release": { "type": "number" }
            }
          }
        }
      }
    }
  }
}
```

이 스키마는 Attack Path Engine 담당의 리뷰가 필요하다(GIT_POLICY.md의 CODEOWNERS 규칙: `@위험분석담당 @공격경로담당`). 특히 `signals` 세부 필드가 그래프 노드 속성으로 그대로 쓰기 충분한지 확인 요청.

## 확정 사항 (교차검토 반영)

**Q6. 권한(Permission) 데이터 출처 → (c) Attack Path Engine이 정의·소유, Risk Analyzer는 참조(consume)만.**
Risk Analyzer의 `permission_weight`는 이미 권한 등급(LOW/MEDIUM/HIGH)을 **입력**으로 쓰는 소비자이지, 권한 목록(타입+대상 자산)의 원 출처가 아니다. 반대로 Attack Path Engine은 그래프 엣지(에이전트→자산 접근)를 만들기 위해 권한 데이터를 어차피 구조화해야 하므로, 스키마 소유권을 그쪽에 두고 Risk Analyzer·Collector는 그 스키마를 참조해 자기 필드에 매핑하는 것이 이중 정의를 막는다. 위 §2.4에 `permission_source` 필드를 추가해 출처를 명시했다.

**Q7. `is_externally_reachable` → Attack Path Engine이 직접 판단.**
이 값은 네트워크/그래프 위상(다른 노드와의 연결 관계)에 의존하는데, Risk Analyzer는 패키지 단위 정적 신호만 다루고 그래프 전체 구조를 보지 않는다. Risk Analyzer가 억지로 계산하면 그래프 구축 시점의 실제 연결 정보와 어긋날 위험이 있다.

**Q8. `signals` 서브 오브젝트 + 원본 CVE 목록 → 둘 다 포함.**
`cvss_norm`만으로는 Dashboard가 요구하는 "CVE 목록" 속성(질문 13)을 만들 수 없으므로 `signals.cve_ids[]`를 추가했다. 그래프 노드에는 `cvss_norm`(정렬/색상용)과 `cve_ids`(사람이 읽는 상세정보용)를 함께 붙인다.

**Q9. `risk_level` vs `risk_score` → 둘 다 유지(기존 설계 그대로).**
원래 스키마에 이미 `risk_score`(숫자, 정렬·임계값 비교용)와 `risk_level`(등급, 시각화·룰 분기용)이 모두 있었다. 별도 변경 불필요, 문서에 각 필드의 용도만 명시적으로 추가했다.
