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
| [`.github/ISSUE_TEMPLATE/subissue.md`](../.github/ISSUE_TEMPLATE/subissue.md) | 하위 이슈 생성 양식 (역할 R1~R4) | 보조 파일 |
| [`.github/ISSUE_TEMPLATE/pm-subissue.md`](../.github/ISSUE_TEMPLATE/pm-subissue.md) | 하위 이슈 생성 양식 (PM/전체, Epic 직속) | 보조 파일 |
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

## 이슈/PR 양식

이슈·PR 작성 형식은 실제 GitHub 템플릿(`.github/ISSUE_TEMPLATE/*.md`, `.github/PULL_REQUEST_TEMPLATE.md`)이 자기설명적이라 별도 규칙 문서를 두지 않습니다. 데이터 계약 스키마(`data_contracts.md`, `sample_dataset.md`, `schemas/*.json`)는 아래 "Architecture" 섹션 참고.

## 검토 업무와 기록

| 파일 | 쉽게 말하면 | 구분 |
|---|---|---|
| [`docs/review/ISSUE_TRACKER.md`](review/ISSUE_TRACKER.md) | 실제 GitHub Issue 번호·담당자·상태 | 쉬운 요약 |
| [`docs/review/decisions.md`](review/decisions.md) | 확정된 설계 결정 기록 — Epic 1개 + 역할 4개 섹션이 파일 하나에 |  기준 문서 |

## Architecture (기술 설계) 기준 문서 — `docs/architecture_v1/`

기술 설계·데이터 계약의 SSOT입니다. 예전에는 `docs/design/`+`docs/contracts/`로 흩어져 있었는데, 하나로 합쳤습니다(LLM에게 구현을 맡길 때 이 폴더 하나만 넘기면 되도록).

| 파일 | 쉽게 말하면 | 구분 |
|---|---|---|
| [`docs/architecture_v1/README.md`](architecture_v1/README.md) | 읽는 순서 안내 | 쉬운 요약 |
| [`design-00-overall.md`](architecture_v1/design-00-overall.md) | 전체 파이프라인 오케스트레이션, 공통 컨벤션 | 기준 문서 |
| [`architecture_diagram.md`](architecture_v1/architecture_diagram.md) | 전체 흐름 Mermaid 도면 | 쉬운 요약 |
| [`data_contracts.md`](architecture_v1/data_contracts.md) | 스키마 4개의 원본+필드 설명+사용처를 한 문서에 모음. 스키마를 참조/수정할 때는 여기부터 | 기준 문서 |
| [`sample_dataset.md`](architecture_v1/sample_dataset.md) | 전 모듈 공통 예시 시나리오 (스키마 검증 통과 확인됨) | 기준 문서 |
| [`design-01-collector.md`](architecture_v1/design-01-collector.md) | Dependency Collector 설계 | 기준 문서 |
| [`design-02-risk-analyzer.md`](architecture_v1/design-02-risk-analyzer.md) | Risk Analyzer 설계 | 기준 문서 |
| [`design-03-ml-detector.md`](architecture_v1/design-03-ml-detector.md) | ML 이상탐지 설계 | 기준 문서 |
| [`design-04-attack-path.md`](architecture_v1/design-04-attack-path.md) | Attack Path Engine 설계 | 기준 문서 |
| [`design-05-dashboard.md`](architecture_v1/design-05-dashboard.md) | Dashboard 설계 | 기준 문서 |
| [`schemas/README.md`](../schemas/README.md) | 스키마가 아직 DRAFT임을 명시, 담당 매핑 | 쉬운 요약 |
| [`schemas/*.schema.json`](../schemas) | 스키마 원본 (JSON Schema, **현재 DRAFT**, 검증 도구가 실제로 참조하는 파일) | 기준 문서 |

## 상위 이슈 (전체 Epic + 역할별)

전체 Epic(#1)과 R1~R4 상위 이슈(#9~12) 전부 GitHub Issue 자체가 원본입니다(별도 로컬 문서 없음). 요약표는 [`docs/governance/OWNERSHIP.md`](governance/OWNERSHIP.md).

## 무엇부터 읽으면 되나요?

1. [프로젝트 README](../README.md)에서 목적과 현재 상태를 확인합니다
2. [협업 가이드](../CONTRIBUTING.md)에서 이슈/PR 순서를 확인합니다
3. [역할과 담당자](governance/OWNERSHIP.md)에서 내 역할(R1~R4)을 찾습니다
4. [설계 문서 입구](architecture_v1/README.md)에서 내 모듈 기술 설계를 확인합니다
5. 모르는 단어는 [용어집](GLOSSARY.md)에서 찾습니다
