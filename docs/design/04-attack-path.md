# Attack Path Engine — 기술 설계 문서

담당: 공격경로 / 시각화 · 작성일: 2026-09-06

## 1. 그래프 라이브러리 선택: NetworkX (Python)

Neo4j 대신 **NetworkX**를 선택합니다. 이유:

- **규모**: 학기 프로젝트 대상 그래프는 (패키지 수십 개 × 에이전트 수 개 × 권한 수십 개) 수준 — 메모리 내 그래프로 충분하고, 별도 DB 서버 운영 부담(설치·인증·백업)이 없습니다.
- **팀 통합 비용**: Risk Analyzer·ML·Collector가 모두 Python/JSON 기반이므로, `pip install networkx`만으로 같은 언어 안에서 그래프를 구성·순회할 수 있습니다. Neo4j를 쓰면 Cypher 학습, DB 서버 배포, JSON↔그래프 동기화 계층이 추가로 필요해 4인 팀 규모에서 리스크 대비 이득이 작습니다.
- **출력 호환성**: NetworkX는 `node_link_data()`로 표준 JSON(노드/엣지 배열)을 바로 뽑아낼 수 있어, Dashboard가 소비할 `attack_graph.schema.json`과 자연스럽게 맞습니다.
- **참고했지만 채택 안 한 것**: BloodHound·Wiz Security Graph는 실제로 Neo4j(Cypher)를 씁니다. `shortestPath()` Cypher 쿼리로 진입점→Domain Admin 최단경로를 찾는 방식([BloodHound Cypher 가이드](https://bloodhound.specterops.io/analyze-data/explore/cypher-search))인데, 우리는 이 방법론(가중치 최단경로로 toxic path 탐색)만 차용하고 실행 엔진은 NetworkX로 대체합니다. 데이터 규모가 커지면(자산 수천 개 이상) Neo4j로 이전 가능하도록 그래프 빌더와 알고리즘 계층을 분리해 둡니다.

## 2. 노드/엣지 스키마

| 노드 타입 | 속성 예시 |
|---|---|
| `Package` | `purl`, `name`, `version`, `ecosystem`, `risk_score`(Risk Analyzer 제공), `is_externally_reachable`(bool) |
| `Agent` | `agent_id`, `name`, `anomaly_score`(ML 제공) |
| `Permission` | `perm_id`, `type`(예: `file_write`, `network_egress`, `api_key_access`), `sensitivity`(0~10, "high-value" 여부 판단 기준) |
| `Asset` | `asset_id`, `type`(예: `secret_store`, `db`, `external_api`), `is_crown_jewel`(bool) |

| 엣지 타입 | 방향 | 의미 |
|---|---|---|
| `depends_on` | Agent → Package | 에이전트가 이 패키지에 의존 |
| `has_vulnerability` | Package → Package(취약점 노드 대신 속성으로 단순화 가능) | 위험 신호 존재 (또는 `risk_score` 속성으로 대체) |
| `grants` | Package/Agent → Permission | 이 컴포넌트가 이 권한을 실제로 보유/행사 |
| `exposes` | Permission → Asset | 이 권한이 이 자산에 접근 가능하게 함 |
| `flagged_anomalous` | ML 결과 → Agent (속성으로 병합 가능) | ML이 이상행동으로 표시 |

가중치(`weight`)는 각 엣지에 부여하며, `weight = 1 / (risk_score × anomaly_score 보정치)` 형태로 "위험할수록 가중치가 낮아(=최단경로 탐색 시 더 선호되게)" 설계합니다.

## 3. 경로 탐색 · 우선순위화 알고리즘

1. **그래프 구성**: Risk Analyzer·ML JSON을 읽어 `networkx.DiGraph()`에 위 노드/엣지 추가.
2. **진입점 정의**: `is_externally_reachable=True`인 `Package` 노드 전체를 소스 후보로.
3. **고가치 타깃 정의**: `is_crown_jewel=True`인 `Asset` 노드, 또는 `sensitivity >= 8`인 `Permission` 노드를 타깃으로.
4. **경로 탐색**: 각 (소스, 타깃) 쌍에 대해 `networkx.shortest_simple_paths(G, source, target, weight="weight")`로 가중치 기준 상위 K개 경로를 생성(Yen's 알고리즘 기반, BloodHound의 `shortestPath()`와 동일한 발상). 그래프가 작으므로 `all_simple_paths()`로 전수 탐색 후 정렬하는 방식도 병행 가능.
5. **"toxic combination" 판정**: 경로 길이(홉 수) 대신 **경로 내 최소 개별 위험도가 아니라 결합 위험도**를 본다 — `path_score = Σ(hop별 risk/anomaly) × exposure_multiplier(진입점이 외부 노출인가)`. 개별 hop이 전부 "중간 위험"이어도 path_score가 임계치를 넘으면 toxic으로 표시.
6. **우선순위화**: `path_score` 내림차순 정렬 → 상위 N개를 "critical path"로 태깅, `networkx.betweenness_centrality()`로 여러 경로에 공통으로 등장하는 병목 노드(예: 특정 권한)를 별도로 표시해 "이 노드 하나만 고쳐도 여러 경로가 끊긴다"는 인사이트 제공.
7. **PoC 검증**: 취약 테스트 에이전트에서 실제로 해당 경로(패키지 취약점 → 권한 획득 → 자산 접근)를 재현해 시나리오 설명 텍스트를 첨부.

## 4. 입력 필드 요구사항

- **Risk Analyzer로부터**: `purl`, `package_risk_score`(0~10), `vulnerability_ids`(CVE/OSV), `is_externally_reachable`, 해당 패키지를 사용하는 `agent_id` 매핑.
- **ML로부터**: `agent_id`, `anomaly_score`(0~1), `anomaly_type`(예: 비정상 API 호출 패턴), 탐지 시각.
- **Collector/공통**: 에이전트별 `permission` 목록(권한 타입, 대상 자산) — 이 필드가 현재 스키마에 없다면 Collector 또는 별도 설정 파일에서 받아야 함(팀 확인 필요).

## 5. `attack-path/` 폴더 구조 (제안)

```
attack-path/
├── graph_builder.py      # Risk Analyzer/ML JSON → networkx.DiGraph
├── path_finder.py        # shortest_simple_paths, toxic combination 판정
├── prioritizer.py        # path_score 계산, betweenness_centrality
├── scenario_writer.py    # 경로 → 자연어 침해 시나리오 텍스트 생성
├── poc/                  # 취약 테스트 에이전트 + 검증 스크립트
├── export.py             # node_link_data() → attack_graph.schema.json 형식으로 출력
└── tests/
```

## 6. 출력 스키마 초안 (`schemas/attack_graph.schema.json`, Dashboard 소비용)

```json
{
  "schema_version": "1.0",
  "run_id": "run-2026-09-06-01",
  "generated_at": "2026-09-06T00:00:00Z",
  "source_module": "attack-path",
  "nodes": [
    {
      "id": "pkg:pypi/flask@2.0.1", "type": "dependency", "label": "flask 2.0.1",
      "risk_score": 72,
      "attributes": {"package_version": "2.0.1", "cve_ids": ["CVE-XXXX"], "typosquat_flag": false}
    },
    {
      "id": "perm:api_key_access", "type": "permission", "label": "API Key Access",
      "risk_score": 80,
      "attributes": {"permission_name": "api_key_access", "target_asset": "asset:secret_store"}
    }
  ],
  "edges": [
    {"id": "e1", "source": "agent:orchestrator-1", "target": "pkg:pypi/flask@2.0.1", "type": "depends_on", "risk_contribution": 14}
  ],
  "paths": [
    {
      "path_id": "path-001",
      "node_sequence": ["pkg:pypi/flask@2.0.1", "agent:orchestrator-1", "perm:api_key_access", "asset:secret_store"],
      "edge_sequence": ["e1", "e2", "e3"],
      "overall_risk_score": 89,
      "description": "외부 노출된 flask 취약점(CVE-XXXX)을 통해 orchestrator-1 에이전트를 장악하면, 보유한 api_key_access 권한으로 secret_store까지 접근 가능"
    }
  ]
}
```

(초안이므로 Dashboard 담당 리뷰 후 필드명·타입 확정 필요)

## 확정 사항 (교차검토 반영)

> ⚠️ **시뮬레이션 초안**: 아래는 실제 팀 교차검토가 아니라 여러 모듈 관점을 미리 가정해서 만든 초안입니다. 실제 담당자와 교차검토 후 다르게 결론 나면 그 내용으로 갱신하세요 (근거는 `docs/review/decisions/0X-*.md`에).

**1. Permission 데이터 출처 (팀 전체 결정, 최중요):** 제시된 (a)/(b)/(c) 중 하나가 아니라 **(a)+(c) 혼합**을 채택합니다. Collector가 에이전트 코드를 정적 스캔하는 유일한 모듈이므로 실제 "이 에이전트가 이 권한을 행사한다"는 사실(`agent.permissions[]`: 권한 타입 + 대상 자산 문자열)은 Collector가 코드 스캔으로 채워 넣고, 그 필드의 **enum·구조 자체는 Attack Path Engine이 정의**합니다(그래프 노드/엣지로 직접 소비하는 쪽이 스키마를 소유해야 이후 그래프 빌더 변경 시 마찰이 없기 때문). Risk Analyzer·ML은 이 필드를 만들지 않고 참조만 합니다. Collector 담당자에게 `agent.permissions[]` 필드 추가를 요청 예정.

**2. 출력 형식 (Q15):** Dashboard 설계서(`05-dashboard.md` §5)가 이미 `nodes/edges/paths` 구조로 스키마를 확정했으므로 Cytoscape `elements:{nodes,edges}` 포맷으로 바꾸지 않습니다. Cytoscape 변환은 프론트엔드(`graphView.js`)가 로드 시 수행합니다.

**3. Risk Analyzer로부터 (Q8/9):** `02-risk-analyzer.md`가 이미 `risk_score`(숫자)와 `risk_level` 둘 다, 그리고 `signals{cvss_norm, epss_score, typo_flag, staleness_score}`를 제공하도록 확정되어 있어 요구사항을 충족합니다. 추가로 원본 `vulnerability_ids`(CVE 목록)도 함께 넘겨주시길 요청합니다 — Dashboard 노드 `attributes.cve_ids`를 채우려면 signals만으로는 부족합니다.

**4. ML로부터 (Q10/11):** `triggered_features`(feature+importance 배열) 구조는 그대로 `Agent` 노드의 `attributes.ml_anomaly_score` 및 상세 패널용 부가 정보로 바로 사용 가능하며 변환 불필요합니다. `confidence_score`는 별도 노드를 만들지 않고 가중합으로 결합합니다: `weight = 1 / (risk_score × confidence_score 보정치)` (§3 기존 설계 유지).

**5. Dashboard에게 (Q12-14):** 모든 `Package`/`Agent`/`Permission` 노드에 사전 계산된 `risk_score`(0-100 정규화), 모든 `paths[]`에 `overall_risk_score`를 채워 넘깁니다(Dashboard 재계산 없음 보장). 각 노드는 `label`(사람이 읽는 이름), 타입별 `attributes`(패키지 버전/CVE 목록/권한명·자산명/에이전트명/ML 이상점수)를 포함합니다. `export.py`가 `node_link_data()` 출력 직후 `node_sequence`/`edge_sequence`의 모든 id가 동일 파일 `nodes[].id`/`edges[].id`에 실제 존재하는지 검증하는 참조 무결성 체크를 통과해야만 파일을 씁니다(단위 테스트로 강제).
