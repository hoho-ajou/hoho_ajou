# [Epic] Dependency Collector 설계 문서 완성

## 목표

AI 에이전트 저장소를 스캔해서 (1) 의존성 목록, (2) LangChain·MCP 등 외부 연동 도구, (3) PyPI 메타데이터·취약점, (4) 표준 SBOM을 자동으로 뽑아내는 파이프라인 입구 모듈의 **설계를, AI가 그대로 구현할 수 있는 수준까지** 완성한다. 실제 코드 구현은 이 Epic이 아니라 설계 확정 이후 단계에서 진행한다. 이 모듈의 산출물이 Risk Analyzer·ML 이상탐지의 입력이 되므로, 설계에서 놓친 케이스는 뒤 단계 전체가 못 본다.

## 범위

`docs/design/01-collector.md`를 아래 수준까지 심화 작성한다:
- 매니페스트 파싱(requirements.txt, pyproject.toml, Pipfile, package.json) 각각의 함수 시그니처와 파싱 실패 시 동작
- import 스캔(pipreqs) 결과와 매니페스트 `--diff` 비교 로직의 구체적 절차
- Dockerfile 파싱(베이스 이미지, `pip install`, `COPY requirements*`) 대상 패턴
- LangChain·MCP 외부 연동 탐지 규칙(코드 내 import 패턴 + `mcp.json`류 설정 파일 파싱)
- PyPI JSON API 메타데이터·취약점 조회 절차(캐싱·재시도 정책 포함)
- 취약점 정보 보완용 OSV 배치 조회 절차
- CycloneDX 포맷 SBOM 생성 절차(`cyclonedx-py` 활용)
- 위 모든 결과를 하나의 표준 출력 객체로 병합·검증·저장하는 순서

**범위 밖**: 비-PyPI 생태계(npm 등)의 취약점 심층 분석, 컨테이너 OS 패키지(apt 등)의 상세 취약점 분석, reachability 분석(어떤 취약 함수가 실제 호출되는지) — 이는 추후 로드맵 또는 Risk Analyzer 영역. **실제 코드 구현 자체도 이번 Epic의 범위 밖.**

## 완료조건

- [ ] 매니페스트 파서·import 스캐너·Dockerfile 파서·연동 탐지기·PyPI/OSV 조회·SBOM 생성, 각 기능의 함수 시그니처(입력 타입 → 출력 타입)가 `docs/design/01-collector.md`에 명시되어 있다
- [ ] 각 기능마다 최소 1개 이상의 구체적 입력→출력 예시(실제 파일 내용 또는 JSON 스니펫)가 있다
- [ ] "매니페스트 없음", "PyPI 미등록 패키지", "비공개/접근 불가 저장소", "PyPI/OSV 조회 실패" 등 최소 4개 이상의 엣지케이스가 "상황 → 기대 동작(`partial`/`failed` 상태와 에러 코드)" 표로 정리되어 있다
- [ ] 출력 스키마가 `schemas/collector_output.schema.json`과 필드 단위로 100% 일치한다
- [ ] Risk Analyzer·ML 담당자 리뷰를 거쳐 설계 문서가 확정된다 (`docs/design/_cross_review_questions.md`에 반영된 사항 재확인)

## 출력 인터페이스

`docs/design/01-collector.md`의 DRAFT 스키마 참고. 핵심 구조만 요약:

```
{
  schema_version, scan_id, repo, status,
  dependencies: [{ name, version, ecosystem, source, resolution_status, pypi{...}, hashes[], vulnerabilities[] }],
  integrations: [{ type, name, detected_in, transport? }],
  sbom: { format, spec_version, generator, file_ref },
  errors: [{ stage, code, message, package? }],
  summary: { total_dependencies, resolved, unresolved, vulnerable_count, integrations_count }
}
```

이 스키마는 `GIT_POLICY.md` §3에 따라 `schemas/collector_output.schema.json`으로 최종 확정 전 **Risk Analyzer·ML 담당자 전원 승인**이 필요한 CODEOWNERS 대상 파일입니다.

## 참고자료

- `study_week1/README.md` §5 (Dependency Collector 구현 가이드), §6 (MCP 딥다이브)
- `study_week1/architecture.html` #collector 섹션
- `study_week1/raw/10_pypi_requirements_parser.md`, `14_pipreqs_github.md`, `15_pypi_json_api_docs.md`, `16_cyclonedx_python_github.md`, `17_osv_api_query_endpoint.md`
- `docs/design/01-collector.md` (본 에픽의 상세 설계 및 스키마 DRAFT)
- `GIT_POLICY.md` §3 (스키마 계약·CODEOWNERS 규칙)

## 하위 이슈

(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
