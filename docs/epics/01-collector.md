# [Epic] Dependency Collector 모듈 구축

## 목표

AI 에이전트 저장소를 스캔해서 (1) 의존성 목록, (2) LangChain·MCP 등 외부 연동 도구, (3) PyPI 메타데이터·취약점, (4) 표준 SBOM을 자동으로 뽑아내는 파이프라인 입구 모듈을 완성한다. 이 모듈의 산출물이 Risk Analyzer·ML 이상탐지의 입력이 되므로, 여기서 놓친 자산은 뒤 단계 전체가 못 본다.

## 범위

- 매니페스트 파싱(requirements.txt, pyproject.toml, Pipfile, package.json)
- 실제 import 스캔(pipreqs) 및 매니페스트와의 `--diff` 비교
- Dockerfile 파싱(베이스 이미지, `pip install`, `COPY requirements*`)
- LangChain·MCP 외부 연동 탐지(코드 내 import 패턴 + `mcp.json`류 설정 파일)
- PyPI JSON API 메타데이터·취약점 조회 (캐싱·재시도 포함)
- 취약점 정보 보완용 OSV 배치 조회
- CycloneDX 포맷 SBOM 생성(`cyclonedx-py` 활용)
- 위 모든 결과를 하나의 표준 출력 객체로 병합·검증·저장

**범위 밖**: 비-PyPI 생태계(npm 등)의 취약점 심층 분석, 컨테이너 OS 패키지(apt 등)의 상세 취약점 분석, reachability 분석(어떤 취약 함수가 실제 호출되는지) — 이는 추후 로드맵 또는 Risk Analyzer 영역.

## 완료조건

- [ ] 임의의 공개 GitHub AI 에이전트 저장소(requirements.txt 유무와 무관)를 입력하면 의존성 목록이 생성된다
- [ ] LangChain/MCP 연동이 있는 저장소에서 해당 연동이 최소 1개 이상 탐지된다
- [ ] 각 의존성에 PyPI 메타데이터(버전·라이선스·해시)와 알려진 취약점 정보가 채워진다 (PyPI 미등록 패키지는 `unresolved`로 표시되고 파이프라인은 계속 진행된다)
- [ ] CycloneDX 형식 SBOM 파일이 생성된다
- [ ] 비공개/접근 불가 저장소, 매니페스트 부재, PyPI 조회 실패 등 예외 상황에서도 전체 프로세스가 죽지 않고 `partial`/`failed` 상태와 에러 목록을 포함한 결과를 반환한다
- [ ] 출력이 `schemas/collector_output.schema.json` DRAFT를 만족하며, Risk Analyzer·ML 담당자 리뷰를 거쳐 스키마가 확정된다

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
