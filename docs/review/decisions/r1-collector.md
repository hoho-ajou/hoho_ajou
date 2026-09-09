# 결정 기록 — Dependency Collector 설계

## 담당 역할

R1 (Dependency Collector, 총괄 겸임) — 자세한 목표/범위는 [`docs/governance/OWNERSHIP.md`](../../governance/OWNERSHIP.md) 참고

## 하위 이슈 분할

(하위 이슈 생성 전 — 담당자가 생성 후 채움)

## 결정 사항

### 결정 1 — 취약점 CVSS 점수를 Collector 단계에서 미리 채워 넣음

**결정하려 했던 것**: `vulnerabilities[]`에 CVE ID만 넣을지, `cvss_base_score`까지 인라인으로 넣을지 (Risk Analyzer가 재조회하지 않아도 되게).

**근거**: Risk Analyzer가 매 패키지마다 CVSS를 다시 조회하면 API 호출이 중복되고 느려짐.

**최종 결정**: OSV 응답의 `severity`(CVSS 벡터)를 Collector가 파싱해 `cvss_base_score`(숫자) + `cvss_source`(`nvd`/`osv`)로 `vulnerabilities[]`에 직접 포함. 파싱 불가 시 `cvss_base_score: null`.

### 결정 2 — 패키지 단위 `external_integrations[]` 필드 추가

**결정하려 했던 것**: 패키지가 shell/network/MCP 접근을 쓰는지 여부를 Risk Analyzer의 `permission_weight` 계산에 넘길 방법.

**근거**: Risk Analyzer가 권한 가중치를 계산하려면 패키지 단위로 연동 컨텍스트가 필요함.

**최종 결정**: 5단계 외부 연동 탐지 결과를 패키지 단위로도 태깅해 `dependencies[].external_integrations: ["network"|"shell"|"mcp"|"filesystem"]` 배열 추가 (top-level `integrations[]`는 별도 유지).

### 결정 3 — `latest_release_date`/`maintainer_count` 결측 처리

**결정하려 했던 것**: staleness score 계산에 쓰이는 이 필드들이 모든 패키지에 항상 존재함을 보장할 수 있는지.

**근거**: PyPI가 일부 패키지에 이 정보를 제공하지 않아 완전 보장은 불가능함.

**최종 결정**: 필드를 항상 present로 두되 값이 없으면 `null` + `data_status: "not_available"`로 명시해 Risk Analyzer가 결측을 구분할 수 있게 함.

### 결정 4 — 배포 파일 경로/해시 포함 (ML 요청)

**결정하려 했던 것**: SBOM에 배포 파일(sdist/wheel) 자체 경로·해시를 포함할지, 메타데이터만 넣을지.

**근거**: ML 이상탐지의 정적 코드 분석 feature 추출에 실제 파일 매칭이 필요함.

**최종 결정**: `distribution_files[]`에 파일명, 다운로드 URL, sha256 해시를 포함.

### 결정 5 — maintainer 계정 생성일은 기본 미수집

**결정하려 했던 것**: ML이 요청한 메인테이너 PyPI 계정 생성일까지 수집 범위에 넣을지.

**근거**: PyPI JSON API가 계정 생성일을 제공하지 않아 별도 유저 페이지 스크래핑이 필요하고 요청량이 커짐.

**최종 결정**: 기본 미수집. 대신 `maintainer_accounts[].account_created_at`을 `null` + `data_status: "not_collected"`로 스키마에 예약해두어, 추후 필요성이 확정되면 별도 수집기를 붙일 수 있게 함.

## 근거 문서

`docs/design/01-collector.md` "확정 사항 (교차검토 반영)"
