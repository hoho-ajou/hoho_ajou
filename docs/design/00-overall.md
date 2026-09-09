# AASM 전체 설계 문서 (00 — Overall)

담당: PM/총괄 · 최종 수정: 2026-09-06

## 1. 저장소 구조 근거

`CONTRIBUTING.md`가 이미 모노레포 구조(`collector/ risk-analyzer/ ml-detector/ attack-path/ dashboard/ schemas/ docs/`)를 확정했습니다. 4인 학부 프로젝트에서 멀티레포는 버전 동기화·CI 중복 설정 비용이 이득보다 큽니다. 여기에 다음을 추가 제안합니다.

```
aasm/
├── pipeline/            # ⭐ 신규 제안: 모듈을 순서대로 실행하는 오케스트레이터
├── collector/
├── risk-analyzer/
├── ml-detector/
├── attack-path/
├── dashboard/
├── schemas/
├── data/                # ⭐ 신규 제안: 단계별 중간 산출물(JSON) 저장소, .gitignore 처리
└── docs/
```

`pipeline/`과 `data/`가 architecture.html에는 명시되지 않았지만, 실제로 팀이 코드를 짜기 시작하면 "누가 다음 모듈을 호출하는가"가 반드시 필요합니다. Syft→Grype 같은 실제 SCA 도구 체인도 "이전 단계가 JSON 파일을 만들고 다음 단계가 그 파일을 읽는" 방식으로 동작합니다(파일 기반 핸드오프가 업계에서도 검증된 패턴). 우리도 동일한 방식을 채택합니다.

## 2. 오케스트레이션: 파일 기반 핸드오프 + 얇은 CLI

**결론: 공유 DB나 메시지 큐 대신, `schemas/`로 형식이 고정된 JSON 파일을 로컬 디스크에 순서대로 쌓는 방식 + 이를 순서대로 호출하는 얇은 Python CLI(`pipeline/run.py`)를 둡니다.**

이유:
- 학부 4인 프로젝트에 DB/큐 인프라는 과설계입니다. Collector→(Risk Analyzer, ML 병렬)→Attack Path→Dashboard는 선형+한 번의 fan-out/fan-in 구조뿐이라 파일 핸드오프로 충분합니다.
- 각 모듈은 독립 실행 가능해야 합니다(모듈 담당자가 자기 모듈만 테스트할 때 다른 모듈이 안 떠 있어도 됨) → "함수를 직접 import해서 호출"이 아니라 "표준 입출력 JSON 파일"을 계약으로 삼습니다.
- `pipeline/run.py`는 각 모듈을 서브프로세스(또는 함수 호출)로 실행하고, 모듈 간 데이터는 `data/<run_id>/collector_output.json` 형태로 저장합니다. 대략:

```
1. collector.main(repo_path)         -> data/<run_id>/collector_output.json
2. (병렬) risk_analyzer.main(...)    -> data/<run_id>/risk_score.json
          ml_detector.main(...)     -> data/<run_id>/ml_result.json
3. attack_path.main(risk_score.json, ml_result.json) -> data/<run_id>/attack_graph.json
4. dashboard가 attack_graph.json을 읽어 웹으로 렌더링
```

- 3단계는 2단계 두 산출물이 **모두** 끝나야 시작 가능(fan-in) — `pipeline/run.py`가 이 대기 로직을 담당합니다. 각 모듈은 서로의 존재를 몰라도 되고, `pipeline/`만 이 순서를 압니다.
- 클라우드 환경(AWS EC2)에서는 이 CLI를 cron 또는 수동 트리거로 실행하는 것으로 충분하며, 마이크로서비스화는 이번 학기 범위 밖입니다.

## 3. `schemas/` 4개 파일의 역할 (상세 스펙은 각 담당자가 작성)

- `collector_output.schema.json` — Collector 산출물. SBOM(CycloneDX 준용) + 의존성 목록 + 탐지된 MCP/외부 연동 도구 리스트를 담는 최상위 구조. Risk Analyzer/ML의 입력.
- `risk_score.schema.json` — 패키지별 위험 점수(CVSS 참고), 타이포스쿼팅 등 정적 필터링 플래그. Attack Path Engine 입력의 절반.
- `ml_result.schema.json` — 패키지별 이상탐지 스코어/라벨. Attack Path Engine 입력의 나머지 절반.
- `attack_graph.schema.json` — 노드(의존성/에이전트/권한)와 엣지(연결)로 구성된 그래프. Dashboard 입력.

각 스키마는 최소 `run_id`, `generated_at`, `source_module`, `schema_version` 공통 메타 필드를 갖도록 통일할 것을 제안합니다. 상세 필드는 module owner가 정의하되, `schemas/` 변경은 CONTRIBUTING.md의 CODEOWNERS 규칙(만드는 사람+받는 사람 전원 승인)을 그대로 따릅니다.

## 4. 프로젝트 공통 컨벤션

- **언어/런타임**: Python 3.11+ 통일(Collector/Risk Analyzer/ML 모두 Python 생태계 도구 사용 전제). Dashboard만 JS(Node 20+).
- **의존성 관리**: 모듈별 `requirements.txt` 또는 `pyproject.toml` 개별 관리(모노레포 안에서도 모듈 독립성 유지).
- **로깅**: 표준 `logging` 모듈, 포맷 `%(asctime)s [%(levelname)s] %(name)s: %(message)s`, 모듈명은 폴더명과 동일하게(`collector`, `risk_analyzer` 등)로 통일해 나중에 로그를 합쳐 봐도 출처가 바로 보이게 합니다.
- **설정 관리**: 모듈 루트에 `config.yaml` 또는 `.env`(민감정보용), 하드코딩 금지. API 키(PyPI는 불필요하지만 향후 OSV rate limit 등 대비)는 `.env` + `.gitignore`.
- **테스트**: 각 모듈 `tests/` 폴더, `pytest` 통일. 최소 기준: 스키마 검증 테스트(자기 모듈 출력이 `schemas/*.schema.json`을 통과하는지) 1개는 필수 — 이게 사실상 우리 프로젝트의 "통합 테스트" 역할을 대신합니다.
- **CI**: GitHub Actions로 PR마다 `pytest` + 스키마 검증 실행 권장(4인 규모라 최소한으로 시작, M3 즈음 도입).

## 5. 이번 검토에서 확인한 리스크

CNAPP류 상용 도구는 보통 이 오케스트레이션 계층을 명시적인 컴포넌트로 갖고 있는데(Syft→Grype 파이프라인처럼 파일 기반 핸드오프가 실제로 검증된 패턴), 우리 architecture.html에는 이 계층이 그림에 드러나 있지 않아 이번 문서에서 `pipeline/`으로 명시했습니다. M2(설계) 마일스톤에서 이 문서를 팀 전체가 리뷰하고 확정하는 것을 제안합니다.
