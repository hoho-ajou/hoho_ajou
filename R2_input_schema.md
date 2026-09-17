### 모듈

Risk Analyzer (R2)

### 상위 이슈

Relates to #10

### 작업 내용

- R1(Collector)이 전달하는 패키지 기본 메타데이터(이름, 버전 등) 입력 규격 확정
- R2의 "타이포스쿼팅 및 악성코드 정적 분석"을 수행하기 위해 필요한 필수 입력 필드 정합성 검증
-  R2에서 최종 위험도 산정에 필수적인 핵심 필드 정합성 검사

### 입력 예시

**R1이 전달하는 입력 예시 (R2가 분석에 직접 활용할 핵심 데이터 위주)**
*참고: 당장 R2에서 쓰이지 않는 정보들은 그대로 R4에게 전달할 계획*

```json
{
  "scan_id": "123e4567-e89b-12d3-a456-426614174000",
  "dependencies": [
    {
      "name": "requests",
      "version": "2.31.0",
      "ecosystem": "PyPI",
      "pypi": {
        "last_release_at": "2023-05-22T10:00:00Z"
      },
      "distribution_files": [
        {
          "local_path": "/app/data/scans/123e4567/requests/"
        }
      ]
    }
  ]
}
```


### 완료조건 (Acceptance Criteria)

- [ ] R1 담당자와 입력 JSON 스키마(`collector_output.schema.json`) 협의 완료
- [ ] R2 타이포스쿼팅 검사에 필수적인 필드(`name`, `version`, `ecosystem`)가 누락 없이 정의되었는지 확인
- [ ] R2가 악성 코드 정적 분석을 수행할 수 있도록 소스 코드 참조 경로(`distribution_files` 내 `local_path`)를 R1이 제공하기로 스키마 협의 완료
- [ ] 패키지 관리 중단 여부를 판단하기 위한 `pypi.last_release_at` 필드 제공 확인

### 엣지케이스

- 필수 값 누락: R1에서 `name`, `version`이 누락되거나 원본 파일 경로(`local_path`)가 없어 정적 분석이 불가능한 경우, 해당 분석 단계를 스킵하고 기본/최저 점수로 처리
- 지원하지 않는 생태계: `ecosystem`이 `PyPI`가 아닌 다른 생태계가 들어왔을 때, 파이썬 전용 타이포스쿼팅 로직을 하지 않고 스킵
- 부가 정보 누락: `pypi.last_release_at` 정보가 `null`이거나 존재하지 않을 경우, 해당 패키지는 최신 업데이트 상태로 간주(방치 패키지 위험도 점수 미부여)
### 참고자료

_No response_