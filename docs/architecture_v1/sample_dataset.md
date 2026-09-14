# 공통 샘플 데이터셋

> ⚠️ **시뮬레이션 초안**: 아래 스키마가 실제 팀 검토로 확정되면 이 예시도 그에 맞춰 갱신해야 합니다. 지금은 참고용 출발점입니다.

4개 모듈(Collector → Risk Analyzer/ML → Attack Path Engine → Dashboard)이 각자 설계 문서에 넣는 입출력 예시가 서로 다른 패키지/에이전트를 가정하면, 실제로 이어붙였을 때 안 맞을 수 있습니다. 그래서 아래 **하나의 가상 시나리오**를 전 모듈이 공유하는 기준 예시로 씁니다. 각 설계 문서(`docs/design/0X-*.md`)의 "입출력 예시"는 가능하면 이 데이터를 그대로 인용하거나 확장해서 쓰세요.

## 시나리오

가상의 오픈소스 LangChain 기반 AI 에이전트 저장소 `example-agent`:
- `requirements.txt`에 `pyyaml==5.3.1`(알려진 취약점 있음), `langchain==0.1.0` 포함
- 코드에서 `langchain.tools.ShellTool`을 사용 (셸 실행 권한)
- `mcp.json`으로 로컬 파일시스템 MCP 서버에 연결 (`/home/user/data` 접근)
- `torch-utils-ext==0.0.3`이라는, PyPI에 정식 등록됐지만 다운로드 수가 비정상적으로 적고 배포된 지 일주일도 안 된 패키지를 사용 (ML이 신규/변종 악성 패키지로 플래그할 대상)

## 1. Collector 출력 (`schemas/collector_output.schema.json`)

```json
{
  "schema_version": "0.1.0",
  "scan_id": "a1b2c3d4-0000-4000-8000-000000000001",
  "repo": {
    "url": "https://github.com/example-org/example-agent",
    "commit_sha": "9f8e7d6",
    "scanned_at": "2026-09-07T02:00:00Z"
  },
  "status": "success",
  "dependencies": [
    {
      "name": "pyyaml",
      "version": "5.3.1",
      "ecosystem": "PyPI",
      "source": ["manifest", "import"],
      "declared_in": ["requirements.txt"],
      "resolution_status": "resolved",
      "pypi": { "latest_version": "6.0.1", "license": "MIT", "last_release_at": "2020-03-18T00:00:00Z" },
      "vulnerabilities": [
        {
          "id": "CVE-2020-14343",
          "aliases": ["GHSA-8q59-q68h-6hv4"],
          "severity": "CRITICAL",
          "cvss_base_score": 9.8,
          "cvss_source": "nvd",
          "fixed_versions": ["5.4"],
          "osv_url": "https://osv.dev/vulnerability/GHSA-8q59-q68h-6hv4"
        }
      ],
      "maintainers": { "maintainer_count": 3, "data_status": "ok" },
      "external_integrations": []
    },
    {
      "name": "langchain",
      "version": "0.1.0",
      "ecosystem": "PyPI",
      "source": ["manifest", "import"],
      "declared_in": ["requirements.txt"],
      "resolution_status": "resolved",
      "pypi": { "latest_version": "0.3.7", "license": "MIT", "last_release_at": "2024-01-05T00:00:00Z" },
      "vulnerabilities": [],
      "maintainers": { "maintainer_count": 12, "data_status": "ok" },
      "external_integrations": ["shell", "mcp"]
    },
    {
      "name": "torch-utils-ext",
      "version": "0.0.3",
      "ecosystem": "PyPI",
      "source": ["manifest"],
      "declared_in": ["requirements.txt"],
      "resolution_status": "resolved",
      "pypi": { "latest_version": "0.0.3", "license": null, "last_release_at": "2026-09-01T00:00:00Z" },
      "vulnerabilities": [],
      "maintainers": { "maintainer_count": 1, "data_status": "ok" },
      "external_integrations": []
    }
  ],
  "agent": {
    "permissions": [
      { "type": "shell_exec", "target_asset": "local_shell" },
      { "type": "file_write", "target_asset": "/home/user/data" }
    ]
  },
  "integrations": [
    { "type": "mcp", "name": "filesystem", "detected_in": "mcp.json", "transport": "stdio" }
  ],
  "sbom": { "format": "CycloneDX", "spec_version": "1.5", "generator": "cyclonedx-py", "file_ref": "data/a1b2c3d4/sbom.json" },
  "errors": [],
  "summary": { "total_dependencies": 3, "resolved": 3, "unresolved": 0, "vulnerable_count": 1, "integrations_count": 1 }
}
```

## 2. Risk Analyzer 출력 (`schemas/risk_score.schema.json`)

```json
{
  "generated_at": "2026-09-07T02:05:00Z",
  "packages": [
    {
      "name": "pyyaml", "version": "5.3.1", "ecosystem": "PyPI",
      "package_risk": 0.92, "permission_weight": 2.5, "permission_source": "attack_path_engine",
      "risk_score": 2.3, "risk_level": "HIGH",
      "vulnerability_ids": ["CVE-2020-14343"],
      "signals": { "cvss_norm": 0.98, "cve_ids": ["CVE-2020-14343"], "epss_score": 0.87, "typo_flag": 0, "typo_nearest_match": null, "staleness_score": 0.9, "months_since_last_release": 78 }
    },
    {
      "name": "langchain", "version": "0.1.0", "ecosystem": "PyPI",
      "package_risk": 0.15, "permission_weight": 2.5, "permission_source": "attack_path_engine",
      "risk_score": 0.38, "risk_level": "LOW",
      "vulnerability_ids": [],
      "signals": { "cvss_norm": 0, "cve_ids": [], "epss_score": 0, "typo_flag": 0, "typo_nearest_match": null, "staleness_score": 0.05, "months_since_last_release": 8 }
    },
    {
      "name": "torch-utils-ext", "version": "0.0.3", "ecosystem": "PyPI",
      "package_risk": 0.4, "permission_weight": 1.0, "permission_source": "default_medium_fallback",
      "risk_score": 0.4, "risk_level": "MEDIUM",
      "vulnerability_ids": [],
      "signals": { "cvss_norm": 0, "cve_ids": [], "epss_score": 0, "typo_flag": 0.5, "typo_nearest_match": "torch-utils", "staleness_score": 0, "months_since_last_release": 0 }
    }
  ]
}
```

## 3. ML 이상탐지 출력 (`schemas/ml_result.schema.json`)

```json
{
  "schema_version": "0.1.0",
  "generated_at": "2026-09-07T02:05:00Z",
  "results": [
    {
      "package_name": "torch-utils-ext", "package_version": "0.0.3", "ecosystem": "PyPI",
      "is_flagged": true, "confidence_score": 0.83, "model": "random_forest_v1",
      "triggered_features": [
        { "feature": "days_since_first_release", "value": 6, "importance": 0.41 },
        { "feature": "maintainer_count", "value": 1, "importance": 0.27 },
        { "feature": "download_count_zscore", "value": -1.8, "importance": 0.19 }
      ]
    },
    {
      "package_name": "pyyaml", "package_version": "5.3.1", "ecosystem": "PyPI",
      "is_flagged": false, "confidence_score": 0.05, "model": "random_forest_v1",
      "triggered_features": []
    },
    {
      "package_name": "langchain", "package_version": "0.1.0", "ecosystem": "PyPI",
      "is_flagged": false, "confidence_score": 0.02, "model": "random_forest_v1",
      "triggered_features": []
    }
  ]
}
```

## 4. Attack Path Engine 출력 (`schemas/attack_graph.schema.json`)

```json
{
  "schema_version": "0.1.0",
  "run_id": "a1b2c3d4-0000-4000-8000-000000000001",
  "generated_at": "2026-09-07T02:10:00Z",
  "source_module": "attack-path",
  "nodes": [
    { "id": "dep:pyyaml", "type": "dependency", "label": "pyyaml 5.3.1", "risk_score": 92, "attributes": { "cve_ids": ["CVE-2020-14343"], "version": "5.3.1" } },
    { "id": "dep:torch-utils-ext", "type": "dependency", "label": "torch-utils-ext 0.0.3", "risk_score": 65, "attributes": { "ml_flagged": true, "ml_confidence": 0.83 } },
    { "id": "agent:example-agent", "type": "agent", "label": "example-agent", "risk_score": 88, "attributes": {} },
    { "id": "perm:shell_exec", "type": "permission", "label": "셸 실행 권한", "risk_score": 80, "attributes": { "permission_type": "shell_exec" } },
    { "id": "asset:local_shell", "type": "asset", "label": "로컬 셸", "risk_score": 95, "attributes": {} }
  ],
  "edges": [
    { "id": "e1", "source": "dep:pyyaml", "target": "agent:example-agent", "type": "depends_on", "risk_contribution": 30 },
    { "id": "e2", "source": "dep:torch-utils-ext", "target": "agent:example-agent", "type": "flagged_anomalous", "risk_contribution": 25 },
    { "id": "e3", "source": "agent:example-agent", "target": "perm:shell_exec", "type": "grants", "risk_contribution": 20 },
    { "id": "e4", "source": "perm:shell_exec", "target": "asset:local_shell", "type": "exposes", "risk_contribution": 25 }
  ],
  "paths": [
    {
      "path_id": "p1",
      "node_sequence": ["dep:pyyaml", "agent:example-agent", "perm:shell_exec", "asset:local_shell"],
      "edge_sequence": ["e1", "e3", "e4"],
      "overall_risk_score": 91,
      "description": "pyyaml의 임의 코드 실행 취약점(CVE-2020-14343)이 악용되면, 이 에이전트가 가진 셸 실행 권한을 통해 로컬 셸까지 완전히 장악될 수 있음"
    }
  ]
}
```

## 사용 규칙

- 각 설계 문서의 "입출력 예시"는 이 데이터를 그대로 쓰거나, 자기 모듈에 필요한 필드를 추가한 확장판을 써도 됩니다. 단 **패키지명/버전/CVE는 이 시나리오와 일치**시켜서, 나중에 4개 예시를 실제로 이어붙여 확인할 수 있게 하세요.
- 이 파일 자체가 스키마는 아닙니다 — 스키마 자체가 바뀌면(`schemas/*.json`) 이 예시도 같이 업데이트해야 합니다.
