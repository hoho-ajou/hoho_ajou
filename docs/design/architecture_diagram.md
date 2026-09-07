# 전체 아키텍처 설계 도면

`docs/design/00-overall.md` §2의 파이프라인 흐름을 그림으로 옮긴 것입니다. 텍스트 설명이 1차 자료(SSOT)이고, 이 도면은 그걸 빠르게 훑기 위한 보조 자료입니다.

## 1. 모듈 간 데이터 흐름 (fan-out/fan-in)

```mermaid
flowchart LR
    REPO[["AI 에이전트\n저장소"]] --> COL["Collector"]
    COL -->|collector_output.json| RA["Risk Analyzer"]
    COL -->|collector_output.json| ML["ML 이상탐지"]
    RA -->|risk_score.json| AP["Attack Path Engine"]
    ML -->|ml_result.json| AP
    COL -->|"agent.permissions[]"| AP
    AP -->|attack_graph.json| DASH["Dashboard"]

    style COL fill:#dbeafe
    style RA fill:#fef3c7
    style ML fill:#fef3c7
    style AP fill:#fecaca
    style DASH fill:#dcfce7
```

- Risk Analyzer와 ML은 Collector 출력을 **동시에(병렬)** 받아 각자 독립 실행
- Attack Path Engine은 **Risk Analyzer + ML 둘 다 끝나야** 시작 (fan-in)
- 각 화살표 라벨이 `schemas/*.json` 파일명 — 자세한 필드는 `docs/contracts/interface_map.md` 참고

## 2. Collector 내부 처리 순서

```mermaid
flowchart TD
    A["저장소 확보/검증"] -->|실패| FAIL["status: failed, 즉시 중단"]
    A -->|성공| B["매니페스트 파싱"]
    B --> C["import 스캔 + diff"]
    C --> D["Dockerfile 파싱"]
    D --> E["외부 연동 탐지\n(LangChain/MCP)"]
    E --> F["PyPI 메타데이터 조회"]
    F --> G{"vulnerabilities\n비어있음?"}
    G -->|예| H["OSV 배치 조회"]
    G -->|아니오| I["SBOM 생성"]
    H --> I
    I --> J["병합·검증·출력"]
```

## 3. 공격 경로 예시 (샘플 데이터셋 기준)

`docs/contracts/sample_dataset.md`의 시나리오를 그래프로 그리면:

```mermaid
flowchart LR
    PYYAML["pyyaml 5.3.1\nCVE-2020-14343\nrisk_score: 92"] -->|depends_on| AGENT["example-agent"]
    TORCH["torch-utils-ext 0.0.3\nML 이상탐지 flagged"] -->|flagged_anomalous| AGENT
    AGENT -->|grants| SHELL_PERM["셸 실행 권한"]
    SHELL_PERM -->|exposes| SHELL["로컬 셸\n(최종 자산)"]

    style PYYAML fill:#fecaca
    style TORCH fill:#fed7aa
    style SHELL fill:#fca5a5
```

굵은 경로(`p1`): `pyyaml` 취약점 → 에이전트 → 셸 실행 권한 → 로컬 셸 장악. `overall_risk_score: 91`

## 갱신 규칙

파이프라인 흐름이나 스키마 구조가 바뀌면 이 문서를 반드시 같이 갱신하세요 — 코드/스키마가 먼저고 도면이 나중입니다(도면이 SSOT가 아님).
