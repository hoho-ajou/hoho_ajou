# Pull Request 공통 스키마

`.github/PULL_REQUEST_TEMPLATE.md`가 실제로 GitHub에서 채워지는 양식이고, 이 문서는 그 각 필드가 왜 필요하고 무엇을 채워야 "충분한지"를 정의하는 계약입니다. 이 기준을 만족해야 리뷰 가능한 것으로 간주합니다.

## 필드별 요구사항

| 필드 | 최소 요구사항 |
|---|---|
| 변경 내용 | 무엇을 바꿨는지 불릿 3개 이내. "리팩터링" 같은 추상적 표현 금지 — 어떤 파일의 어떤 동작이 바뀌었는지 |
| 변경 이유 | 왜 필요한지 1~2문장. 어떤 문제·요청과 연결되는지(하위 이슈의 완료조건과 맞아야 함), 안 하면 뭐가 안 되는지 |
| 관련 이슈 | `Closes #<하위 이슈 번호>` 필수. 이슈 없는 PR은 반려 (범위가 불명확한 작업이라는 뜻) |
| 스키마 변경 여부 | `schemas/*.json`을 건드렸으면 체크 후 CODEOWNERS 대상 담당자 리뷰 승인이 머지 조건 (`CONTRIBUTING.md` §3) |
| 테스트 방법 | 실행한 커맨드 + 실제 출력(또는 스크린샷). "잘 됩니다" 금지 — `pytest tests/test_x.py -v` 결과 붙여넣기 수준 |
| 체크리스트 | 로컬 동작 확인 + 문서 업데이트 여부. 둘 다 체크 안 되어 있으면 머지 보류 |

## 커밋 메시지 규칙 (Conventional Commits, `CONTRIBUTING.md` §4 재확인)

```
<type>(<module>): <설명>

[선택: 본문]

Closes #<이슈번호>
```

- `type`: `feat` / `fix` / `docs` / `refactor` / `test` / `chore`
- `module`: `collector` / `risk-analyzer` / `ml-detector` / `attack-path` / `dashboard` / `schemas` / `pipeline`
- 하나의 커밋은 하나의 하위 이슈에 대응 (여러 이슈를 한 커밋에 묶지 않음)

## 머지 조건

1. 체크리스트 전항목 체크
2. `schemas/` 변경 시 CODEOWNERS 승인
3. CI(추후 `.github/workflows/` 추가 시) 통과
4. 최소 1인 리뷰 승인 (2인 이하 소규모 모듈은 총괄이 대신 리뷰 가능)
