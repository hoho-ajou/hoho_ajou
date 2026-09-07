# 전체 파이프라인 인터페이스 맵

`schemas/*.json`이 각 경계면의 정확한 구조(기계가 읽는 것)라면, 이 문서는 **"어느 모듈의 어느 필드가 다음 모듈의 어느 필드로 흘러가는지"를 한 페이지에서 훑어보는 인간용 지도**입니다. 예시 값은 `docs/contracts/sample_dataset.md`에서 그대로 가져왔습니다.

## 경계면 1 — Collector → Risk Analyzer / ML

| Collector 출력 필드 | 받는 쪽 | 쓰이는 곳 | 예시 값 |
|---|---|---|---|
| `dependencies[].name`, `.version`, `.ecosystem` | Risk Analyzer, ML | 패키지 식별자, 모든 계산의 기준 키 | `pyyaml`, `5.3.1`, `PyPI` |
| `dependencies[].vulnerabilities[].cvss_base_score` | Risk Analyzer | `signals.cvss_norm` 계산 (÷10 정규화) | `9.8` → `0.98` |
| `dependencies[].vulnerabilities[].id` | Risk Analyzer | `signals.cve_ids`, `vulnerability_ids` | `CVE-2020-14343` |
| `dependencies[].pypi.last_release_at` | Risk Analyzer | `signals.staleness_score`, `months_since_last_release` 계산 | `2020-03-18` → 78개월 → `0.9` |
| `dependencies[].maintainers.maintainer_count` | Risk Analyzer | staleness 보조 신호 | `3` |
| `agent.permissions[]` | Risk Analyzer | `permission_weight` 계산 (Attack Path Engine 정의 enum 참조) | `shell_exec` → `2.5` |
| `dependencies[]` 전체(배포일·다운로드 추정치 등) | ML | feature extraction 입력 | `torch-utils-ext`의 `last_release_at` → `days_since_first_release=6` |

## 경계면 2 — Risk Analyzer / ML → Attack Path Engine

| 출처 | 필드 | 쓰이는 곳 | 예시 값 |
|---|---|---|---|
| Risk Analyzer | `packages[].risk_score`, `.risk_level` | 그래프 `dependency` 노드의 `risk_score`(0-100로 재정규화) | `2.3`(0~3 척도) → 노드 `risk_score: 92` |
| Risk Analyzer | `packages[].vulnerability_ids` | 노드 `attributes.cve_ids` | `["CVE-2020-14343"]` |
| ML | `results[].is_flagged`, `.confidence_score` | `flagged_anomalous` 엣지 생성 여부 및 `risk_contribution` | `is_flagged: true` → `e2` 엣지 생성 |
| ML | `results[].triggered_features` | 노드 `attributes.ml_triggered_features` (그대로 매핑, 변환 없음) | `days_since_first_release` 등 |
| Collector (경계면 1을 건너뛰어 직접 전달) | `agent.permissions[]` | `permission` 노드 + `grants` 엣지 생성 | `shell_exec` → `perm:shell_exec` 노드 |

## 경계면 3 — Attack Path Engine → Dashboard

| Attack Path Engine 출력 필드 | Dashboard에서 쓰이는 곳 | 비고 |
|---|---|---|
| `nodes[].risk_score` (0-100) | 노드 색상/크기 (재계산 없이 그대로 표시) | Dashboard는 정규화하지 않음 — 이미 끝난 상태로 받음 |
| `nodes[].attributes` | 상세 정보 패널 필드 | 타입별로 다른 키 (cve_ids/ml_triggered_features 등) |
| `paths[].node_sequence`, `.edge_sequence` | 경로 하이라이트 시 강조할 노드/엣지 id 목록 | `nodes[].id`/`edges[].id`를 실제로 참조 — 참조 무결성 필수 |
| `paths[].description` | 경로 리스트 뷰의 한 줄 요약 | 사람이 읽는 자연어 |

## 왜 별도 문서인가

`schemas/*.json`은 "한 경계면"만 각자 정의합니다(파일 자체가 그렇게 나뉘어 있음). 전체 체인을 한 번에 보려면 4개 파일 + 4개 설계 문서를 오가야 하는데, 이 문서 하나로 "값이 실제로 어떻게 변환되며 흘러가는지"를 끝까지 추적할 수 있게 하는 게 목적입니다. **스키마 자체의 진실 공급원은 여전히 `schemas/*.json`이고, 이 문서는 그걸 대체하지 않습니다** — 필드 정의가 바뀌면 스키마 파일을 먼저 고치고 이 문서를 따라서 갱신하세요.
