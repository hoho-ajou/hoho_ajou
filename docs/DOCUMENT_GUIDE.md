# AASM 전체 문서 지도

저장소의 각 파일이 무엇을 위한 것인지 설명합니다. 처음 참여했다면 [프로젝트 README](../README.md) → [협업 가이드](../CONTRIBUTING.md) → [용어집](GLOSSARY.md) 순서로 읽으세요.

## 기준 표시

- **기준 문서**: 설계 의미와 협업 규칙을 판단할 때 우선합니다.
- **쉬운 요약**: 기준 문서를 빠르게 찾고 이해하도록 돕습니다.
- **보조 파일**: Issue/PR 화면을 작동시키는 설정 파일입니다.

## 저장소 첫 화면과 협업

| 파일 | 쉽게 말하면 | 구분 |
|---|---|---|
| [`README.md`](../README.md) | 프로젝트 목적, 현재 상태, 전체 흐름을 소개 | 기준 문서 |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | 브랜치·이슈·PR·머지 규칙 | 기준 문서 |
| [`.github/ISSUE_TEMPLATE/subissue.yml`](../.github/ISSUE_TEMPLATE/subissue.yml) | 하위 이슈 생성 양식 | 보조 파일 |
| [`.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md) | PR 기본 양식 | 보조 파일 |
| [`.github/CODEOWNERS`](../.github/CODEOWNERS) | 스키마 변경 시 자동 리뷰어 지정 | 보조 파일 |

## 문서 안내와 공통 용어

| 파일 | 쉽게 말하면 | 구분 |
|---|---|---|
| [`docs/README.md`](README.md) | 설계 문서를 어디서부터 읽어야 하는지 | 쉬운 요약 |
| [`docs/DOCUMENT_GUIDE.md`](DOCUMENT_GUIDE.md) | 지금 이 파일 | 쉬운 요약 |
| [`docs/GLOSSARY.md`](GLOSSARY.md) | 스키마 필드와 직결된 용어 정의 | 쉬운 요약 |

## 협업·승인 규칙

| 파일 | 쉽게 말하면 | 구분 |
|---|---|---|
| [`docs/governance/OWNERSHIP.md`](governance/OWNERSHIP.md) | R1~R4 역할별 담당자, 목표/범위/완료조건, CODEOWNERS | 기준 문서 |
| [`docs/governance/REVIEW_CHECKLIST.md`](governance/REVIEW_CHECKLIST.md) | 설계 문서 리뷰 체크리스트 | 기준 문서 |

## 모듈 간 공통 계약

| 파일 | 쉽게 말하면 | 구분 |
|---|---|---|
| [`docs/contracts/epic_schema.md`](contracts/epic_schema.md) | 전체 Epic 공통 형식 | 기준 문서 |
| [`docs/contracts/role_issue_schema.md`](contracts/role_issue_schema.md) | R1~R4 역할 상위 이슈 공통 형식 | 기준 문서 |
| [`docs/contracts/subissue_schema.md`](contracts/subissue_schema.md) | 하위 이슈 공통 형식 | 기준 문서 |
| [`docs/contracts/pr_schema.md`](contracts/pr_schema.md) | PR 공통 형식·머지 조건 | 기준 문서 |
| [`docs/contracts/decision_record_schema.md`](contracts/decision_record_schema.md) | Epic·역할별 결정 기록 공통 형식 | 기준 문서 |
| [`docs/contracts/sample_dataset.md`](contracts/sample_dataset.md) | 전 모듈 공통 예시 시나리오 (스키마 검증 통과 확인됨) | 기준 문서 |
| [`docs/contracts/interface_map.md`](contracts/interface_map.md) | 필드가 모듈 사이로 흘러가는 전체 경로 | 쉬운 요약 |
| [`schemas/README.md`](../schemas/README.md) | 스키마가 아직 DRAFT임을 명시, 담당 매핑 | 쉬운 요약 |
| [`schemas/*.schema.json`](../schemas) | 모듈 간 데이터 계약 (JSON Schema, **현재 DRAFT** — 담당자가 실제 설계로 교체 가능) | 기준 문서 |

## 검토 업무와 기록

| 파일 | 쉽게 말하면 | 구분 |
|---|---|---|
| [`docs/review/ISSUE_TRACKER.md`](review/ISSUE_TRACKER.md) | 실제 GitHub Issue 번호·담당자·상태 | 쉬운 요약 |
| [`docs/review/decisions/README.md`](review/decisions/README.md) | 확정된 설계 결정 목록 (Epic 1개 + 역할 4개) | 기준 문서 |
| `docs/review/decisions/00-overall.md`, `r1~r4-*.md` | Epic·역할별 결정 기록 | 기준 기록 |

## Architecture (기술 설계) 기준 문서

| 파일 | 쉽게 말하면 | 구분 |
|---|---|---|
| [`docs/design/README.md`](design/README.md) | 설계 문서 읽는 순서 안내 | 쉬운 요약 |
| [`00-overall.md`](design/00-overall.md) | 전체 파이프라인 오케스트레이션, 공통 컨벤션 | 기준 문서 |
| [`01-collector.md`](design/01-collector.md) | Dependency Collector 설계 | 기준 문서 |
| [`02-risk-analyzer.md`](design/02-risk-analyzer.md) | Risk Analyzer 설계 | 기준 문서 |
| [`03-ml-detector.md`](design/03-ml-detector.md) | ML 이상탐지 설계 | 기준 문서 |
| [`04-attack-path.md`](design/04-attack-path.md) | Attack Path Engine 설계 | 기준 문서 |
| [`05-dashboard.md`](design/05-dashboard.md) | Dashboard 설계 | 기준 문서 |
| [`architecture_diagram.md`](design/architecture_diagram.md) | 전체 흐름 Mermaid 도면 | 쉬운 요약 |

## 상위 이슈 (전체 Epic + 역할별)

| 파일 | 구분 |
|---|---|
| [`docs/epics/00-overall.md`](epics/00-overall.md) | 전체 Epic — GitHub Issue #1 |
| [`docs/roles/r1-collector.md`](roles/r1-collector.md) | R1 상위 이슈 (Epic #1 승계) |
| [`docs/roles/r2-risk-analyzer.md`](roles/r2-risk-analyzer.md) | R2 상위 이슈 (Epic #1 승계) |
| [`docs/roles/r3-ml-detector.md`](roles/r3-ml-detector.md) | R3 상위 이슈 (Epic #1 승계) |
| [`docs/roles/r4-attack-path-dashboard.md`](roles/r4-attack-path-dashboard.md) | R4 상위 이슈 (Epic #1 승계) |

요약표는 [`docs/governance/OWNERSHIP.md`](governance/OWNERSHIP.md).

## 무엇부터 읽으면 되나요?

1. [프로젝트 README](../README.md)에서 목적과 현재 상태를 확인합니다
2. [협업 가이드](../CONTRIBUTING.md)에서 이슈/PR 순서를 확인합니다
3. [역할과 담당자](governance/OWNERSHIP.md)에서 내 역할(R1~R4)을 찾습니다
4. [설계 문서 입구](design/README.md)에서 내 모듈 기술 설계를 확인합니다
5. 모르는 단어는 [용어집](GLOSSARY.md)에서 찾습니다
