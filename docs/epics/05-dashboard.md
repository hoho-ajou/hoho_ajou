# [Epic] Dashboard 설계 문서 완성

담당: 공격경로/시각화 · 최종 수정: 2026-09-06

## 목표

Attack Path Engine이 만든 `attack_graph.json`(의존성→에이전트→권한→공격경로 그래프)을 지도교수·쿤텍 자문단이 웹 브라우저에서 바로 열어 "어떤 자산이 위험하고 왜 위험한지, 그 위험이 어떤 경로로 실제 피해까지 이어지는지"를 직관적으로 판단할 수 있는 인터랙티브 대시보드의 **설계를 AI 구현 가능한 수준까지** 완성한다. 실제 프론트엔드/백엔드 코드 작성은 이 Epic의 범위가 아니다.

## 범위

**포함 (`docs/design/05-dashboard.md` 심화)**
- Cytoscape.js 기반 그래프 뷰 설계(노드 타입별 스타일링 규칙, `dagre`/`cola` 레이아웃 전환 조건)
- risk_score 기준 필터링(슬라이더)·검색 기능의 동작 규칙
- 위험 자산/공격경로 리스트 뷰 ↔ 그래프 하이라이트 연동 방식
- 노드/경로 클릭 시 상세 정보 패널에 표시할 타입별 필드 목록(CVE, 버전, 권한명, 이상탐지 점수 등)
- 얇은 FastAPI 백엔드 API 설계: `data/<run_id>/attack_graph.json` 읽기 + 스키마 검증 + 정적 파일 서빙 엔드포인트 목록
- PNG 내보내기 방식 설계

**범위 밖**: 실시간 스트리밍 업데이트, 다중 사용자 인증/권한 관리, 그래프 데이터 자체의 재계산(위험 점수는 Attack Path Engine이 이미 계산해서 넘겨줌 — Dashboard는 표시만 담당), **실제 프론트엔드/백엔드 코드 구현**

## 완료 조건

- [ ] 그래프 뷰·필터링·리스트 연동·상세 패널, 각 기능의 동작 규칙이 `docs/design/05-dashboard.md`에 구체적으로(입력 이벤트 → 화면 변화) 서술되어 있다
- [ ] `schemas/attack_graph.schema.json`을 만족하는 샘플 JSON 예시와 그 예시가 화면에 어떻게 렌더링되어야 하는지 매핑이 있다
- [ ] FastAPI 백엔드의 엔드포인트 목록(경로, 메서드, 요청/응답 형식)이 명시되어 있다
- [ ] "그래프가 비어있는 경우", "risk_score가 없는 노드" 등 최소 2개 엣지케이스가 표로 정리되어 있다
- [ ] 지도교수/쿤텍 대상 시연 시나리오("노드 클릭 → 상세정보 → 경로 하이라이트")가 화면 흐름으로 문서화되어 있다

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
