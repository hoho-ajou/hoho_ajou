# 역할 이슈(Role Issue) 공통 스키마

`docs/roles/*.md`는 전체 Epic([#1](https://github.com/hoho-ajou/hoho_ajou/issues/1))을 승계받는 R1~R4 각자의 상위 이슈입니다. Epic처럼 별도로 "닫는" 개념은 없고, Epic #1 산하에서 각자 진행 상황을 담습니다.

## 필수 섹션 (순서 고정)

```markdown
# [R<N>] <모듈명> 설계

## 상위 이슈
Part of #1

## 목표
(이 역할이 끝나면 무엇이 가능해지는지)

## 범위
(이 역할이 어디까지 담당하는지 — 무엇을 하고 안 하는지의 경계만)

## 완료조건
(참/거짓을 판정할 수 있는 조건)

## 참고 자료 (강제 아님 — 출발점)
(관련 schemas/*.schema.json DRAFT, sample_dataset.md 등)

## 담당 문서
(docs/design/0X-*.md, 결정 기록 링크)

## 하위 이슈
(담당자가 프로젝트 진행 상황에 맞춰 직접 세분화하여 생성 예정 — 여기서는 만들지 않습니다)
```

Epic(`docs/contracts/epic_schema.md`)과 같은 원칙을 씁니다 — 큰 틀만 주고, 데이터 스키마·구현 방식은 담당자가 직접 설계합니다.

## OWNERSHIP.md와의 관계

`docs/governance/OWNERSHIP.md`는 R1~R4 요약 표만 갖고, 상세 목표/범위/완료조건은 이 폴더(`docs/roles/`)가 SSOT입니다.
