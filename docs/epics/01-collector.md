# [Epic] Dependency Collector 설계 문서 완성

## 목표

AI 에이전트 저장소를 스캔해서 (1) 의존성 목록, (2) LangChain·MCP 등 외부 연동 도구, (3) PyPI 메타데이터·취약점, (4) 표준 SBOM을 자동으로 뽑아내는 파이프라인 입구 모듈의 **설계를, AI가 그대로 구현할 수 있는 수준까지** 완성한다. 실제 코드 구현은 설계 확정 이후 단계에서 진행한다.

## 범위

`docs/design/01-collector.md`를 심화 작성한다:
- 매니페스트 파싱, import 스캔+diff, Dockerfile 파싱 — 의존성 추출
- LangChain·MCP 외부 연동 탐지
- PyPI/OSV 메타데이터·취약점 조회
- CycloneDX SBOM 생성
- 위 결과를 하나의 표준 출력 객체로 병합·검증·저장하는 순서

**범위 밖**: 비-PyPI 생태계 취약점 심층 분석, 컨테이너 OS 패키지 상세 분석, reachability 분석, **실제 코드 구현**

## 완료조건

- [ ] 매니페스트 파서·import 스캐너·Dockerfile 파서·연동 탐지기·PyPI/OSV 조회·SBOM 생성, 각 기능의 함수 시그니처(입력 타입 → 출력 타입)가 명시되어 있다
- [ ] 각 기능마다 최소 1개 이상의 구체적 입력→출력 예시가 있다
- [ ] 최소 4개 이상의 엣지케이스가 "상황 → 기대 동작" 표로 정리되어 있다
- [ ] 출력 스키마가 `schemas/collector_output.schema.json`과 필드 단위로 100% 일치한다
- [ ] Risk Analyzer·ML 담당자 리뷰를 거쳐 설계 문서가 확정된다

## 공통계약

- `docs/contracts/sample_dataset.md` — 전 모듈 공통 예시 시나리오
- `docs/contracts/interface_map.md` — 필드 단위 흐름 정리
- `schemas/collector_output.schema.json` — CODEOWNERS 대상 (Risk Analyzer·ML 승인 필요)

## 담당 문서

`docs/design/01-collector.md`

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
