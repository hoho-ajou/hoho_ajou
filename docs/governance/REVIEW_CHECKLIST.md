# 설계 문서 리뷰 체크리스트

설계 문서(`docs/design/0X-*.md`)를 "완료"로 표시하기 전, 작성자와 리뷰어가 공통으로 확인하는 항목입니다. **구현자가 읽어도 모호함이 없는지**가 기준입니다.

## 작성자 자가 점검

- [ ] 핵심 함수/클래스의 시그니처(입력 타입 → 출력 타입)가 명시되어 있다
- [ ] 최소 1개 이상의 구체적 입력→출력 예시가 있다 (가능하면 [`docs/contracts/sample_dataset.md`](../contracts/sample_dataset.md) 시나리오 재사용)
- [ ] 엣지케이스가 "상황 → 기대 동작" 표로 정리되어 있다 (해당 역할의 완료조건에 명시된 최소 개수 이상 — [`OWNERSHIP.md`](OWNERSHIP.md) 참고)
- [ ] 이 모듈이 내보내는/받는 필드가 관련 `schemas/*.schema.json`과 필드 단위로 100% 일치한다
- [ ] 다른 모듈에 새로 요청하는 입력 필드가 있다면, 그 모듈 담당자와 협의 완료

## 리뷰어 점검 (입력을 제공하는 쪽 / 받아쓰는 쪽 교차 리뷰)

- [ ] 내가 이 모듈에 넘기는 필드가 문서에 정확히 반영되어 있는가
- [ ] 문서만 보고 내 모듈을 어떻게 연결해야 하는지 추측할 필요가 없는가
- [ ] 스키마 변경이 있다면 CODEOWNERS([`docs/governance/OWNERSHIP.md`](OWNERSHIP.md)) 대상 전원이 승인했는가

## 리뷰 결과 반영

- 승인된 중요 결정은 [`docs/review/decisions/`](../review/decisions/README.md)에 결정 기록으로 남깁니다.
- 진행 상태는 [`docs/review/ISSUE_TRACKER.md`](../review/ISSUE_TRACKER.md)에 반영합니다.
