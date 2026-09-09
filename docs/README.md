# AASM 문서 안내

이 폴더에는 AASM의 설계 문서와 팀 협업 기록이 들어 있습니다. 아직 실행 코드는 없는 **설계 검토 단계**입니다.

## 처음이라면 여기부터 읽으세요

1. [전체 문서 지도](DOCUMENT_GUIDE.md) — 각 파일이 무엇을 위한 것인지 알려줍니다
2. [용어집](GLOSSARY.md) — 모르는 용어를 확인합니다
3. [역할과 담당자](governance/OWNERSHIP.md) — 누가 어떤 모듈/Issue를 맡는지 봅니다
4. [실제 Issue 현황](review/ISSUE_TRACKER.md) — GitHub Issue와 진행 상태를 봅니다
5. [설계 문서 입구](design/README.md) — 전체 기술 흐름과 모듈별 문서를 안내합니다

## 문서 종류

- **기준 문서**: `docs/design/`(기술 설계), `docs/contracts/`(모듈 간 공통 계약), `docs/governance/`(역할·체크리스트). 실제 설계 의미는 이 문서들이 우선합니다.
- **검토 기록**: `docs/review/`. 실제 Issue 현황과 확정된 설계 결정을 기록합니다.
- **쉬운 요약**: `docs/GLOSSARY.md`, `docs/DOCUMENT_GUIDE.md`.

## 현재 상태

- `DESIGN_AUTHORED` — 초안 6개 모듈 설계 문서 + 4개 스키마 작성 완료
- `REVIEW_REQUIRED` — 각 담당자가 자기 모듈 문서를 [`governance/REVIEW_CHECKLIST.md`](governance/REVIEW_CHECKLIST.md) 기준으로 심화 중
- `NOT_IMPLEMENTED` — 실행 코드는 아직 없음
