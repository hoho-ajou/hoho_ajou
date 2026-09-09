# Dashboard 설계 문서 (05 — Dashboard)

담당: 공격경로/시각화 · 최종 수정: 2026-09-06

## 1. 시각화 라이브러리: Cytoscape.js 확정

`resources/curated_list.md` J절의 2026 비교 가이드(Cytoscape.js vs vis-network vs Sigma.js)와 WebSearch로 확인한 실제 보안 그래프 UI 사례(공격경로 시각화 툴들이 risk score로 정렬하고 클릭 시 경로를 하이라이트하는 패턴)를 근거로, 사전 검토된 **Cytoscape.js를 그대로 확정**합니다.

- 우리 그래프는 `의존성 → 에이전트 → 권한 → 공격경로`의 4단계 이종(heterogeneous) 노드 타입 + 계층적 흐름을 가지며, 노드 수는 학부 프로젝트 규모(수십~수백 개)로 대규모가 아닙니다. 이 규모에서는 Sigma.js(WebGL, 수만 개 노드 최적화)의 장점이 필요 없고, vis-network는 그래프 알고리즘·레이아웃 확장(`cytoscape-dagre`, `cytoscape-cola` 등)이 Cytoscape.js보다 빈약합니다.
- Cytoscape.js는 원래 생물정보학 네트워크 분석용으로 설계되어 "노드/엣지에 속성을 붙이고 그 속성으로 스타일·필터·경로탐색을 하는" 용도에 강하며, 보안 공격경로 시각화 연구·툴에서도 실제로 채택 사례가 있습니다. `dagre` 레이아웃이 우리의 단계적 흐름(의존성→...→경로)을 자연스러운 좌→우 계층 구조로 그려준다는 점이 결정적입니다.

## 2. 웹 스택: FastAPI(얇은 백엔드) + 정적 JS 프론트엔드

`docs/design/00-overall.md`는 "Dashboard만 JS(Node 20+)"로 잠정 제안했으나, 이를 다음과 같이 보완 제안합니다.

**결론: 아주 얇은 FastAPI 백엔드(Python) + 빌드 도구 없는 순수 JS(Cytoscape.js) 프론트엔드.**

이유:
- Dashboard의 입력은 `schemas/attack_graph.schema.json`을 따르는 JSON 파일 하나뿐입니다(00-overall.md의 파일 기반 핸드오프 원칙 그대로 계승). 백엔드가 하는 일은 (1) `data/<run_id>/attack_graph.json`을 읽어 스키마 유효성 검사 후 그대로 내려주기, (2) 사용 가능한 run 목록 제공, (3) 정적 파일 서빙뿐입니다.
- 이걸 Python(FastAPI)으로 하면 `pydantic` 모델을 `schemas/attack_graph.schema.json`과 1:1로 맞춰 다른 3개 모듈과 동일한 스키마 검증 관례(00-overall.md 4절의 "자기 모듈 출력이 schemas/*.schema.json을 통과하는지" 테스트 원칙)를 그대로 재사용할 수 있고, 팀 전체가 Python 3.11 통일 컨벤션을 따르므로 유지보수 부담이 적습니다. Node 백엔드를 새로 만들면 팀에서 유일하게 다른 런타임/CI 설정이 하나 더 늘어납니다.
- 프론트엔드는 React/Vue 등 프레임워크 없이 순수 JS + Cytoscape.js로 구성합니다. 지도교수·쿤텍에게 보여주는 최종 산출물이 "그래프를 그리고 클릭하면 정보가 뜨는" 수준이라 SPA 프레임워크는 과설계이며, 빌드 파이프라인이 없으면 `python -m http.server` 또는 FastAPI의 `StaticFiles`만으로 실행 가능해 발표/시연 리스크가 줄어듭니다.

## 3. 핵심 인터랙션 기능 (우선순위 순)

1. **위험도 기준 필터링** — 슬라이더로 risk_score 임계값을 조절하면 그 이하 노드/엣지를 dim 처리. 검토 대상을 빠르게 좁히는 것이 보안 리뷰의 핵심 동작이므로 최우선.
2. **경로(Path) 하이라이트** — 오른쪽 "위험 경로 목록"에서 경로를 클릭하면 그래프에서 해당 노드/엣지 시퀀스만 강조하고 나머지는 회색 처리 + 애니메이션 이동.
3. **노드 상세 패널** — 노드 클릭 시 우측 패널에 타입별 상세 정보(패키지명·버전·CVE 목록, 에이전트명, 권한명 등) 표시.
4. **검색** — 노드 라벨/CVE ID로 검색해 그래프 내 위치로 포커스 이동.
5. **레이아웃 전환** — 기본 `dagre`(계층형) ↔ `cola`(힘 기반, 전체 구조 탐색용) 토글.
6. **PNG 내보내기** — Cytoscape.js 내장 기능으로 현재 뷰를 이미지로 저장(보고서 삽입용).

## 4. 화면 구성 (3-뷰 구조)

- **그래프 뷰(메인)**: Cytoscape 캔버스, 상단에 run 선택 드롭다운 + 위험도 슬라이더 + 검색창.
- **위험 자산/경로 리스트 뷰(우측 패널 상단)**: risk_score 내림차순 정렬 테이블(경로/노드), 클릭 시 그래프 하이라이트와 연동.
- **노드/경로 상세 뷰(우측 패널 하단, 컨텍스트 전환)**: 선택된 노드 또는 경로의 전체 필드를 사람이 읽을 수 있는 형태로 표시.

## 5. Attack Path Engine에 요청하는 INPUT 스키마 (`schemas/attack_graph.schema.json`)

Dashboard는 아래 필드가 **반드시** 채워진 상태로 넘어와야 자체 재계산 없이 바로 렌더링할 수 있습니다.

```jsonc
{
  "schema_version": "1.0",
  "run_id": "string",
  "generated_at": "ISO8601 string",
  "source_module": "attack-path",
  "nodes": [
    {
      "id": "string (unique)",
      "type": "dependency | agent | permission | path_step",
      "label": "string (사람이 읽을 표시명, 필수)",
      "risk_score": "number 0-100 (Dashboard는 재계산하지 않음)",
      "attributes": {
        "package_version": "string, optional",
        "cve_ids": ["string", "..."],
        "typosquat_flag": "boolean, optional",
        "ml_anomaly_score": "number, optional",
        "permission_name": "string, optional",
        "agent_name": "string, optional"
      }
    }
  ],
  "edges": [
    { "id": "string", "source": "node id", "target": "node id",
      "type": "depends_on | grants_permission | enables_path",
      "risk_contribution": "number 0-100, optional" }
  ],
  "paths": [
    {
      "path_id": "string",
      "node_sequence": ["node id", "..."],
      "edge_sequence": ["edge id", "..."],
      "overall_risk_score": "number 0-100 (필수, 리스트 정렬 기준)",
      "description": "string (사람이 읽을 한 줄 요약, 필수)"
    }
  ]
}
```

## 6-1. 확정 사항 (교차검토 반영)

> ⚠️ **시뮬레이션 초안**: 아래는 실제 팀 교차검토가 아니라 여러 모듈 관점을 미리 가정해서 만든 초안입니다. 실제 담당자와 교차검토 후 다르게 결론 나면 그 내용으로 갱신하세요 (근거는 `docs/review/decisions/0X-*.md`에).

**질문 15 답변 (Attack Path Engine → Dashboard):** Attack Path Engine은 **범용 `nodes/edges/paths` JSON**(위 5절 스키마 그대로)만 출력하고, Cytoscape 전용 `elements` 포맷으로의 변환은 **Dashboard 프론트엔드가 렌더링 시점에** 수행합니다.

**이유:** (1) attack-path 모듈이 특정 시각화 라이브러리에 종속되지 않아 UI 라이브러리 교체 시 상류 스키마 변경이 불필요하고, (2) 범용 구조가 스키마 검증·유닛테스트하기 더 쉬우며, (3) 변환 로직 자체가 몇 줄 수준이라 Dashboard 쪽 부담이 거의 없습니다.

```js
// frontend/js/graphView.js
function toCytoscapeElements(graph) {
  const nodes = graph.nodes.map(n => ({
    data: { id: n.id, label: n.label, type: n.type, riskScore: n.risk_score, ...n.attributes }
  }));
  const edges = graph.edges.map(e => ({
    data: { id: e.id, source: e.source, target: e.target, type: e.type }
  }));
  return { nodes, edges };
}
cy.add(toCytoscapeElements(graph)); // graph = attack_graph.json
```

## 6. `dashboard/` 파일 구조 제안

```
dashboard/
├── backend/
│   ├── app.py                 # FastAPI 진입점, StaticFiles 마운트
│   ├── models.py              # attack_graph.schema.json에 대응하는 pydantic 모델
│   ├── routes/graph.py        # GET /api/runs, GET /api/graph/{run_id}
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/
│       ├── api.js             # fetch 래퍼
│       ├── graphView.js        # cytoscape 초기화·레이아웃·하이라이트
│       ├── riskList.js         # 위험 리스트 렌더링·정렬
│       └── detailPanel.js      # 노드/경로 상세 패널
├── tests/
│   └── test_schema_validation.py
└── README.md
```
