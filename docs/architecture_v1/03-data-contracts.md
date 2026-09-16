# 데이터 공통 계약 (Data Contracts)

모듈 간 경계면 4개(`schemas/*.schema.json`)의 **원본, 필드별 설명, 어느 모듈이 어디서 쓰는지**를 한 문서에 모았습니다. 스키마를 쓰거나 고칠 때는 이 문서를 기준으로 참조/수정합니다.

- **원본(SSOT)은 여전히 `schemas/*.schema.json` 파일 자체**입니다 — 실제 검증(`scripts/validate_docs.py`)은 그 파일로 돕니다. 이 문서의 JSON 블록은 그 내용을 그대로 옮겨온 것이라, 스키마를 고치면 이 문서도 같이 고쳐야 합니다.
- 필드를 바꾸는 PR은 `CONTRIBUTING.md` §3에 따라 CODEOWNERS(아래 각 스키마의 담당자) 전원 승인이 필요합니다. 실제 담당자는 [`docs/governance/OWNERSHIP.md`](../governance/OWNERSHIP.md).
- 모든 값의 실제 예시는 [`04-sample-dataset.md`](04-sample-dataset.md) 참고.

---

## 1. `collector_output.schema.json` — Dependency Collector 출력

만드는 사람: R1(배승원) · 받아쓰는 사람: R2(유다호), R3(제유호)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CollectorOutput",
  "description": "[DRAFT — 담당자 실제 설계로 변경 가능] Dependency Collector 모듈 출력. CODEOWNERS: @baeseungwon1010 @daho-boop @jeyuho",
  "type": "object",
  "required": ["schema_version", "scan_id", "repo", "status", "dependencies", "summary"],
  "properties": {
    "schema_version": { "type": "string", "const": "0.1.0" },
    "scan_id": { "type": "string", "format": "uuid" },
    "repo": {
      "type": "object",
      "required": ["url", "scanned_at"],
      "properties": {
        "url": { "type": "string" },
        "commit_sha": { "type": ["string", "null"] },
        "scanned_at": { "type": "string", "format": "date-time" }
      }
    },
    "status": { "type": "string", "enum": ["success", "partial", "failed"] },
    "dependencies": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "ecosystem", "resolution_status"],
        "properties": {
          "name": { "type": "string" },
          "version": { "type": ["string", "null"] },
          "ecosystem": { "type": "string" },
          "source": { "type": "array", "items": { "type": "string", "enum": ["manifest", "import", "dockerfile"] } },
          "declared_in": { "type": "array", "items": { "type": "string" } },
          "resolution_status": { "type": "string", "enum": ["resolved", "unresolved"] },
          "pypi": {
            "type": "object",
            "properties": {
              "latest_version": { "type": ["string", "null"] },
              "summary": { "type": ["string", "null"] },
              "license": { "type": ["string", "null"] },
              "home_page": { "type": ["string", "null"] },
              "last_release_at": { "type": ["string", "null"], "format": "date-time" }
            }
          },
          "hashes": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": { "algo": { "type": "string" }, "value": { "type": "string" } }
            }
          },
          "distribution_files": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "filename": { "type": "string" },
                "url": { "type": "string" },
                "hashes": { "type": "array", "items": { "type": "object" } }
              }
            }
          },
          "vulnerabilities": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["id", "severity"],
              "properties": {
                "id": { "type": "string" },
                "aliases": { "type": "array", "items": { "type": "string" } },
                "severity": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "CRITICAL"] },
                "cvss_base_score": { "type": ["number", "null"], "minimum": 0, "maximum": 10 },
                "cvss_source": { "type": ["string", "null"], "enum": ["nvd", "osv", null] },
                "fixed_versions": { "type": "array", "items": { "type": "string" } },
                "osv_url": { "type": "string" }
              }
            }
          },
          "maintainers": {
            "type": "object",
            "properties": {
              "maintainer_count": { "type": ["integer", "null"] },
              "data_status": { "type": "string", "enum": ["ok", "not_available"] },
              "maintainer_accounts": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "username": { "type": "string" },
                    "account_created_at": { "type": ["string", "null"] },
                    "data_status": { "type": "string", "enum": ["ok", "not_collected"] }
                  }
                }
              }
            }
          },
          "external_integrations": {
            "type": "array",
            "items": { "type": "string", "enum": ["network", "shell", "mcp", "filesystem"] }
          }
        }
      }
    },
    "agent": {
      "type": "object",
      "description": "에이전트 단위 권한 정보. 필드 구조/enum 소유권은 Attack Path Engine, 값 채우기는 Collector 담당 (결정 기록 참고)",
      "properties": {
        "permissions": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["type", "target_asset"],
            "properties": {
              "type": { "type": "string", "description": "Attack Path Engine이 정의하는 enum (예: file_write, network_egress, api_key_access, shell_exec)" },
              "target_asset": { "type": "string" }
            }
          }
        }
      }
    },
    "integrations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "name": { "type": "string" },
          "detected_in": { "type": "string" },
          "transport": { "type": "string" }
        }
      }
    },
    "sbom": {
      "type": "object",
      "properties": {
        "format": { "type": "string" },
        "spec_version": { "type": "string" },
        "generator": { "type": "string" },
        "file_ref": { "type": "string" }
      }
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["stage", "code", "message"],
        "properties": {
          "stage": { "type": "string" },
          "code": { "type": "string" },
          "message": { "type": "string" },
          "package": { "type": ["string", "null"] }
        }
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_dependencies": { "type": "integer" },
        "resolved": { "type": "integer" },
        "unresolved": { "type": "integer" },
        "vulnerable_count": { "type": "integer" },
        "integrations_count": { "type": "integer" }
      }
    }
  }
}
```

### 필드 설명 및 사용처

| 필드 | 설명 | 어디에 쓰이는지 |
|---|---|---|
| `dependencies[].name`, `.version`, `.ecosystem` | 패키지 식별자(예: `pyyaml`, `5.3.1`, `PyPI`) | R2·R3 — 모든 계산의 기준 키 |
| `dependencies[].vulnerabilities[].cvss_base_score` | CVSS 기본 점수(0~10). OSV 응답을 Collector가 파싱해 인라인 포함(결정 기록 R1-결정1) | R2 — `signals.cvss_norm` 계산(÷10 정규화) |
| `dependencies[].vulnerabilities[].id` | CVE/OSV ID | R2 — `signals.cve_ids`, `vulnerability_ids` |
| `dependencies[].pypi.last_release_at` | 마지막 배포일 | R2 — `signals.staleness_score`, `months_since_last_release` 계산 |
| `dependencies[].maintainers.maintainer_count` | 메인테이너 수 | R2 — staleness 보조 신호 |
| `dependencies[].external_integrations[]` | 패키지 단위 외부 연동 태그(`network`/`shell`/`mcp`/`filesystem`, 결정 기록 R1-결정2) | R2 — `permission_weight` 계산 시 컨텍스트 |
| `dependencies[].distribution_files[]` | 배포 파일(sdist/wheel) 경로·해시(결정 기록 R1-결정4) | R3 — 정적 코드 분석 시 실제 파일 매칭 |
| `agent.permissions[]` | 에이전트 권한(타입+대상 자산). 값은 Collector, enum·구조는 R4 소유(결정 기록 R4-결정1) | R2 — `permission_weight` 계산 / R4 — `permission` 노드+`grants` 엣지 생성 (경계면 1을 건너뛰어 직접 전달) |
| `dependencies[]` 전체(배포일·다운로드 추정치 등) | 패키지 메타데이터 전반 | R3 — feature extraction 입력 |

---

## 2. `risk_score.schema.json` — Risk Analyzer 출력

만드는 사람: R2(유다호) · 받아쓰는 사람: R4(전선재)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RiskScoreOutput",
  "description": "[DRAFT — 담당자 실제 설계로 변경 가능] Risk Analyzer 모듈 출력. CODEOWNERS: @daho-boop @ryanjeon1",
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
            "description": "권한 등급 산정에 쓰인 권한 데이터의 출처. Risk Analyzer는 권한 목록을 직접 생성하지 않고 Attack Path Engine 소유 스키마를 참조한다.",
            "enum": ["attack_path_engine", "default_medium_fallback"]
          },
          "risk_score": { "type": "number", "minimum": 0, "description": "숫자형 원점수(0~3.0). Dashboard 등 정렬/시각화용." },
          "risk_level": { "type": "string", "enum": ["LOW", "MEDIUM", "HIGH"] },
          "vulnerability_ids": {
            "type": "array",
            "items": { "type": "string" },
            "description": "Attack Path Engine 요청으로 추가 — Dashboard의 attributes.cve_ids 채우기용 원본 CVE/OSV ID 목록"
          },
          "signals": {
            "type": "object",
            "properties": {
              "cvss_norm": { "type": "number", "minimum": 0, "maximum": 1 },
              "cve_ids": { "type": "array", "items": { "type": "string" } },
              "epss_score": { "type": "number", "minimum": 0, "maximum": 1 },
              "typo_flag": { "type": "number", "enum": [0, 0.5, 1] },
              "typo_nearest_match": { "type": ["string", "null"] },
              "staleness_score": { "type": "number", "minimum": 0, "maximum": 1 },
              "months_since_last_release": { "type": "number" }
            }
          }
        }
      }
    }
  }
}
```

### 필드 설명 및 사용처

| 필드 | 설명 | 어디에 쓰이는지 |
|---|---|---|
| `packages[].risk_score` | 패키지 최종 위험도 원점수(0~3.0) | R4 — 그래프 `dependency` 노드의 `risk_score`(0-100로 재정규화) |
| `packages[].risk_level` | 위험 등급(LOW/MEDIUM/HIGH) | R4/Dashboard — 시각화·룰 분기 |
| `packages[].vulnerability_ids` | 원본 CVE/OSV ID 목록 | R4 — 노드 `attributes.cve_ids` |
| `packages[].signals.cvss_norm` | CVSS를 0~1로 정규화한 값 | Risk Analyzer 내부 위험도 산정식 입력 |
| `packages[].signals.typo_flag` / `.typo_nearest_match` | 타이포스쿼팅(유사 이름) 탐지 결과. Levenshtein 거리 기반 | Risk Analyzer 내부 위험도 산정식 입력 |
| `packages[].signals.staleness_score` | 유지보수 방치 정도(0~1, 마지막 릴리스 이후 경과 개월 기반) | Risk Analyzer 내부 위험도 산정식 입력 |
| `packages[].permission_weight` | 에이전트 권한 위험도에 따른 가중치(1.0~3.0). `agent.permissions[]` 참조해 계산 | Risk Analyzer 내부 위험도 산정식 입력 |

---

## 3. `ml_result.schema.json` — ML 이상탐지 출력

만드는 사람: R3(제유호) · 받아쓰는 사람: R4(전선재)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MLResultOutput",
  "description": "[DRAFT — 담당자 실제 설계로 변경 가능] ML 이상탐지 모듈 출력. CODEOWNERS: @jeyuho @ryanjeon1",
  "type": "object",
  "required": ["schema_version", "generated_at", "results"],
  "properties": {
    "schema_version": { "type": "string" },
    "generated_at": { "type": "string", "format": "date-time" },
    "results": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["package_name", "package_version", "ecosystem", "is_flagged", "confidence_score", "model", "triggered_features"],
        "properties": {
          "package_name": { "type": "string" },
          "package_version": { "type": "string" },
          "ecosystem": { "type": "string" },
          "is_flagged": { "type": "boolean" },
          "confidence_score": { "type": "number", "minimum": 0, "maximum": 1 },
          "model": { "type": "string" },
          "triggered_features": {
            "type": "array",
            "description": "importance 내림차순 정렬, 상위 5개로 cap. Attack Path Engine이 attributes.ml_triggered_features로 그대로 매핑.",
            "maxItems": 5,
            "items": {
              "type": "object",
              "required": ["feature", "value", "importance"],
              "properties": {
                "feature": { "type": "string" },
                "value": {},
                "importance": { "type": "number", "minimum": 0, "maximum": 1 }
              }
            }
          }
        }
      }
    }
  }
}
```

### 필드 설명 및 사용처

| 필드 | 설명 | 어디에 쓰이는지 |
|---|---|---|
| `results[].is_flagged` | 악성 여부 판정(bool) | R4 — `flagged_anomalous` 엣지 생성 여부 |
| `results[].confidence_score` | 판단 확신도(0~1) | R4 — `risk_contribution` 계산에 결합(사전 가중합 안 함, 결정 기록 R3-결정2) |
| `results[].triggered_features` | 판단에 기여한 feature 상위 5개(`feature`/`value`/`importance`) | R4 — 노드 `attributes.ml_triggered_features`(변환 없이 그대로 매핑) |

---

## 4. `attack_graph.schema.json` — Attack Path Engine 출력 (Dashboard 소비용)

만드는 사람: R4(전선재) · 받아쓰는 사람: R4 자신(Dashboard 프론트엔드)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AttackGraphOutput",
  "description": "[DRAFT — 담당자 실제 설계로 변경 가능] Attack Path Engine 모듈 출력 (Dashboard 소비용). CODEOWNERS: @ryanjeon1. 형식은 범용 nodes/edges/paths — Cytoscape 등 라이브러리별 변환은 소비 측(Dashboard) 프론트엔드가 수행.",
  "type": "object",
  "required": ["schema_version", "run_id", "generated_at", "nodes", "edges", "paths"],
  "properties": {
    "schema_version": { "type": "string" },
    "run_id": { "type": "string" },
    "generated_at": { "type": "string", "format": "date-time" },
    "source_module": { "type": "string", "const": "attack-path" },
    "nodes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "type", "label", "risk_score"],
        "properties": {
          "id": { "type": "string" },
          "type": { "type": "string", "enum": ["dependency", "agent", "permission", "asset"] },
          "label": { "type": "string", "description": "사람이 읽는 이름. Dashboard 표시용" },
          "risk_score": { "type": "number", "minimum": 0, "maximum": 100, "description": "사전 정규화(0-100) 완료 — Dashboard는 재계산하지 않음" },
          "attributes": {
            "type": "object",
            "description": "타입별 상세 정보 (패키지버전/cve_ids/권한명·자산명/에이전트명/ml_triggered_features 등)"
          }
        }
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "source", "target", "type"],
        "properties": {
          "id": { "type": "string" },
          "source": { "type": "string", "description": "nodes[].id 참조 — 참조 무결성 필수" },
          "target": { "type": "string", "description": "nodes[].id 참조 — 참조 무결성 필수" },
          "type": { "type": "string", "enum": ["depends_on", "grants", "exposes", "flagged_anomalous"] },
          "risk_contribution": { "type": "number" }
        }
      }
    },
    "paths": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path_id", "node_sequence", "edge_sequence", "overall_risk_score", "description"],
        "properties": {
          "path_id": { "type": "string" },
          "node_sequence": { "type": "array", "items": { "type": "string" }, "description": "nodes[].id 참조, 참조 무결성 필수 (export.py에서 검증 후 출력)" },
          "edge_sequence": { "type": "array", "items": { "type": "string" }, "description": "edges[].id 참조, 참조 무결성 필수" },
          "overall_risk_score": { "type": "number", "minimum": 0, "maximum": 100, "description": "사전 계산 완료" },
          "description": { "type": "string", "description": "사람이 읽는 침해 시나리오 한 줄 설명" }
        }
      }
    }
  }
}
```

### 필드 설명 및 사용처

| 필드 | 설명 | 어디에 쓰이는지 |
|---|---|---|
| `nodes[].risk_score` (0-100) | 사전 정규화된 위험도 | Dashboard — 노드 색상/크기(재계산 없이 그대로 표시) |
| `nodes[].attributes` | 타입별 상세 정보(cve_ids/ml_triggered_features 등) | Dashboard — 상세 정보 패널 |
| `paths[].node_sequence`, `.edge_sequence` | 경로를 구성하는 노드/엣지 id 순서 | Dashboard — 경로 하이라이트 시 강조할 노드/엣지. `nodes[].id`/`edges[].id`를 실제로 참조(참조 무결성 필수) |
| `paths[].description` | 침해 시나리오 한 줄 요약 | Dashboard — 경로 리스트 뷰 |

---

## 관련 문서

- 값 예시는 [`04-sample-dataset.md`](04-sample-dataset.md)
- 이 스키마들이 왜 지금 형태로 정해졌는지는 [`docs/review/decisions.md`](../review/decisions.md)
