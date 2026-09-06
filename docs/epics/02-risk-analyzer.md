# [Epic] Risk Analyzer 모듈 구현

담당: 위험분석 | 관련 모듈: Risk Analyzer | 라벨: `risk-analyzer`, `schema`, `feature`

## 목표

Dependency Collector가 만든 SBOM·의존성 목록을 입력받아, 패키지별로 "패키지 자체 위험도(CVE/CVSS/EPSS + 타이포스쿼팅 + 유지보수 상태) × 에이전트 권한 가중치" 공식으로 위험 점수를 산출하고, 이를 표준 JSON으로 Attack Path Engine에 넘기는 것.

## 범위

**포함**
- CVSS 기반 취약점 심각도 정규화 (Collector가 수집한 CVE/CVSS 값 활용)
- EPSS(악용 예측 확률) API 연동 및 결합 로직
- 타이포스쿼팅 탐지: 인기 패키지 top-N 대비 Levenshtein distance 기반 규칙 + 보조 신호(다운로드 수, 등록일)
- 유지보수 상태 신호: 마지막 릴리즈일, 메인테이너 수 기반 staleness 점수
- 에이전트 권한 등급(LOW/MEDIUM/HIGH) 승수 반영
- 최종 위험 점수·등급을 `schemas/risk_score.schema.json` 형식으로 출력

**제외 (범위 밖)**
- ML 기반 신규/변종 악성 패키지 탐지 (ML 이상탐지 모듈 담당)
- 의존성-권한-공격경로 그래프 구성 (Attack Path Engine 담당)
- combosquatting(문자 치환형) 등 고급 타이포스쿼팅 규칙, 다국어/비-PyPI 생태계 지원 — v2 이후 별도 이슈로 분리

## 완료 조건 (Acceptance Criteria)

- [ ] `risk-analyzer/` 디렉토리에 스코어링 파이프라인 동작 (Collector 출력 JSON → risk_score.json)
- [ ] CVSS·EPSS·타이포스쿼팅·staleness 4개 신호가 각각 독립 모듈로 분리되어 단위 테스트 가능
- [ ] 최소 1개 실제 CVE 보유 패키지(예: 과거 취약점 있는 버전)로 점수 산출 검증
- [ ] 타이포스쿼팅 탐지가 알려진 사례(colorama/colorizr류 이름)를 최소 1건 이상 정탐
- [ ] `schemas/risk_score.schema.json` 초안 작성 및 Attack Path Engine 담당 리뷰·승인 완료 (GIT_POLICY.md CODEOWNERS 규칙)
- [ ] Collector 출력에 필요한 필드(아래 입력 인터페이스)가 실제로 채워지는지 Collector 담당과 교차 확인

## 입력/출력 인터페이스

**입력 (Collector → Risk Analyzer, `schemas/collector_output.schema.json` 요구사항)**
- `package.name`, `package.ecosystem`, `package.version` (필수)
- `package.latest_release_date`, `package.maintainer_count` (staleness 계산용)
- `package.vulnerabilities[].cve_id`, `.cvss_base_score` (PyPI JSON API `vulnerabilities` 필드에서 이미 확보 가능)
- `package.osv_ids[]` (CVE 미매핑 취약점 대응)
- `external_integrations[]` — 패키지가 쓰이는 컨텍스트(쉘 실행/네트워크/MCP 연동 등). **현재 미정의 시 Collector 담당과 신규 협의 필요**

**출력 (Risk Analyzer → Attack Path Engine, `schemas/risk_score.schema.json`)**
- 패키지별 `package_risk`(0~1), `permission_weight`(1.0~3.0), `risk_score`, `risk_level`(LOW/MEDIUM/HIGH), 세부 `signals`(cvss_norm, epss_score, typo_flag, staleness_score 등)
- 상세 산식 및 스키마 초안: `docs/design/02-risk-analyzer.md` 참고

## 참고자료

- `study_week1/architecture.html` — Risk Analyzer 섹션, "패키지 위험도 × 에이전트 권한" 공식
- `study_week1/README.md` — CVE/CVSS/타이포스쿼팅 용어 정리, 파이프라인 내 위치
- `study_week1/raw/06_jfrog_typosquatting.md`, `07_checkmarx_colorama.md` — 타이포스쿼팅 실제 사례
- `resources/curated_list.md` F 섹션(타이포스쿼팅·의존성 컨퓨전), W 섹션(EPSS/CVSS/NVD API, Risk Analyzer 필독)
- FIRST/CrowdStrike EPSS 설명, Intruder "EPSS vs CVSS" — CVSS 한계 보완용 실제 악용 확률 지표 개념
- `GIT_POLICY.md` — 스키마 변경 시 CODEOWNERS 승인 규칙

## 하위 이슈

(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
