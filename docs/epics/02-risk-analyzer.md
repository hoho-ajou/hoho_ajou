# [Epic] Risk Analyzer 설계 문서 완성

담당: 위험분석 | 관련 모듈: Risk Analyzer | 라벨: `risk-analyzer`, `schema`, `design`

## 목표

Dependency Collector가 만든 SBOM·의존성 목록을 입력받아, 패키지별로 "패키지 자체 위험도(CVE/CVSS/EPSS + 타이포스쿼팅 + 유지보수 상태) × 에이전트 권한 가중치" 공식으로 위험 점수를 산출하는 로직의 **설계를 AI 구현 가능한 수준까지** 완성하는 것. 실제 스코어링 파이프라인 코드 작성은 이 Epic의 범위가 아니다.

## 범위

**포함 (`docs/design/02-risk-analyzer.md` 심화)**
- CVSS 기반 취약점 심각도 정규화 공식과 계산 함수 시그니처
- EPSS(악용 예측 확률) API 연동 절차 및 CVSS와의 결합 공식
- 타이포스쿼팅 탐지: 인기 패키지 top-N 대비 Levenshtein distance 기준값과 보조 신호(다운로드 수, 등록일) 결합 규칙
- 유지보수 상태 신호: 마지막 릴리즈일, 메인테이너 수 기반 staleness 점수 계산식
- 에이전트 권한 등급(LOW/MEDIUM/HIGH) 승수 반영 공식
- 최종 위험 점수·등급 산출 공식과 `schemas/risk_score.schema.json` 필드 매핑

**제외 (범위 밖)**
- ML 기반 신규/변종 악성 패키지 탐지 (ML 이상탐지 모듈 담당)
- 의존성-권한-공격경로 그래프 구성 (Attack Path Engine 담당)
- combosquatting(문자 치환형) 등 고급 타이포스쿼팅 규칙, 다국어/비-PyPI 생태계 지원 — v2 이후 별도 이슈로 분리
- **실제 스코어링 파이프라인 코드 구현** — 설계 확정 이후 단계

## 완료 조건 (Acceptance Criteria)

- [ ] CVSS·EPSS·타이포스쿼팅·staleness·권한가중치 5개 계산 로직 각각의 함수 시그니처와 공식이 `docs/design/02-risk-analyzer.md`에 명시되어 있다
- [ ] 각 계산 로직마다 최소 1개의 구체적 입력값 → 출력값 예시가 있다 (실제 CVE 보유 패키지 예시 포함)
- [ ] 타이포스쿼팅 탐지 규칙이 알려진 사례(colorama/colorizr류 이름)를 예시로 검증되어 있다
- [ ] "CVSS 값 없음", "EPSS 조회 실패", "메인테이너 정보 없음" 등 최소 3개 엣지케이스가 표로 정리되어 있다
- [ ] `schemas/risk_score.schema.json`과 설계 문서의 공식·필드가 100% 일치하며 Attack Path Engine 담당 리뷰·승인 완료 (GIT_POLICY.md CODEOWNERS 규칙)
- [ ] Collector 출력에서 필요한 입력 필드 목록이 Collector 설계 문서와 교차 확인되어 불일치가 없다

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
