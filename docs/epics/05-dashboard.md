# [Epic] Dashboard — 위험자산·공격경로 웹 시각화

담당: 공격경로/시각화 · 최종 수정: 2026-09-06

## 목표

Attack Path Engine이 만든 `attack_graph.json`(의존성→에이전트→권한→공격경로 그래프)을 지도교수·쿤텍 자문단이 웹 브라우저에서 바로 열어 "어떤 자산이 위험하고 왜 위험한지, 그 위험이 어떤 경로로 실제 피해까지 이어지는지"를 직관적으로 판단할 수 있는 인터랙티브 대시보드를 만든다. 파이프라인의 마지막 단계로, 이 프로젝트 전체의 설득력을 좌우하는 화면이다.

## 범위

- Cytoscape.js 기반 그래프 뷰(노드 타입별 스타일링, `dagre`/`cola` 레이아웃 전환)
- risk_score 기준 필터링(슬라이더) 및 검색 기능
- 위험 자산/공격경로 리스트 뷰(정렬 가능한 테이블) ↔ 그래프 하이라이트 연동
- 노드/경로 클릭 시 상세 정보 패널(CVE, 버전, 권한명, 이상탐지 점수 등)
- 얇은 FastAPI 백엔드: `data/<run_id>/attack_graph.json` 읽기 + 스키마 검증 + 정적 파일 서빙
- PNG 내보내기(보고서용 캡처)
- **범위 밖**: 실시간 스트리밍 업데이트, 다중 사용자 인증/권한 관리, 그래프 데이터 자체의 재계산(위험 점수는 Attack Path Engine이 이미 계산해서 넘겨줌 — Dashboard는 표시만 담당)

## 완료 조건

- [ ] `schemas/attack_graph.schema.json`을 만족하는 샘플 JSON으로 그래프가 렌더링된다
- [ ] risk_score 슬라이더로 노드/엣지 필터링이 동작한다
- [ ] 위험 경로 리스트에서 항목 클릭 시 해당 경로가 그래프에서 하이라이트된다
- [ ] 노드 클릭 시 우측 패널에 상세 정보(타입별 필드)가 표시된다
- [ ] `dashboard/tests/test_schema_validation.py`가 `schemas/attack_graph.schema.json` 검증을 통과한다
- [ ] `python -m uvicorn` 한 줄 명령으로 로컬 실행 가능(빌드 도구 불필요)
- [ ] 지도교수/쿤텍 대상 시연에서 "노드 클릭 → 상세정보 → 경로 하이라이트"까지 데모 가능

## 입력 인터페이스

- **입력원**: Attack Path Engine (`attack-path/` 모듈)
- **입력 파일**: `data/<run_id>/attack_graph.json` (`schemas/attack_graph.schema.json` 준수)
- **필수 필드**(자세한 내용은 `docs/design/05-dashboard.md` 5절 참고):
  - `nodes[].id`, `type`(dependency/agent/permission/path_step), `label`, `risk_score`(0-100, Dashboard가 재계산하지 않음), `attributes`(CVE 목록, 패키지 버전, 권한명 등)
  - `edges[].id`, `source`, `target`, `type`
  - `paths[].path_id`, `node_sequence`, `edge_sequence`, `overall_risk_score`, `description`(사람이 읽을 한 줄 요약)
- **공통 메타**: `schema_version`, `run_id`, `generated_at`, `source_module` (00-overall.md 제안 규칙 준수)
- Dashboard는 이 파일 하나만 입력으로 받으며, 다운스트림 소비자가 없는 파이프라인의 종착 모듈이다(`GIT_POLICY.md` 참고).

## 참고자료

- `study_week1/architecture.html` — Dashboard 섹션(#dash), Figure 1 전체 아키텍처
- `resources/curated_list.md` — J절 "Dashboard 담당 — 시각화 라이브러리" (Cytoscape.js 공식 문서, 2026 비교 가이드)
- `docs/design/00-overall.md` — 파일 기반 핸드오프 원칙, 스키마 공통 메타 필드 제안
- `docs/design/05-dashboard.md` — 본 모듈 상세 설계(스택 선정 근거, INPUT 스키마, 파일 구조)
- `GIT_POLICY.md` — 모노레포 구조, CODEOWNERS, 스키마 변경 승인 규칙

## 하위 이슈

(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
