# 역할과 담당자

전체는 하나의 Epic([#1](https://github.com/hoho-ajou/hoho_ajou/issues/1), 총괄 소유)이고, 그 아래 5개 모듈을 4명이 R1~R4로 나눠 맡습니다. 각자 상위 이슈(GitHub Issue, Epic #1을 승계)를 갖고, 그 안에서 하위 이슈를 직접 만들어 진행합니다.

| 역할 | 담당자 | 담당 모듈 | 상위 이슈 | 담당 문서 | 결정 기록 | CODEOWNERS 대상 |
|---|---|---|---|---|---|---|
| 총괄(PM) | 배승원 ([@baeseungwon1010](https://github.com/baeseungwon1010)) — R1 겸임 | 전체 오케스트레이션 | [#1](https://github.com/hoho-ajou/hoho_ajou/issues/1) | `docs/architecture_v1/design-00-overall.md` | [결정 기록](../review/decisions.md#epic--전체-오케스트레이션) | — |
| R1 | 배승원 ([@baeseungwon1010](https://github.com/baeseungwon1010)) | Dependency Collector | [#9](https://github.com/hoho-ajou/hoho_ajou/issues/9) | `docs/architecture_v1/design-01-collector.md` | [결정 기록](../review/decisions.md#r1--dependency-collector) | `schemas/collector_output.schema.json` |
| R2 | 유다호 ([@daho-boop](https://github.com/daho-boop)) | Risk Analyzer | [#10](https://github.com/hoho-ajou/hoho_ajou/issues/10) | `docs/architecture_v1/design-02-risk-analyzer.md` | [결정 기록](../review/decisions.md#r2--risk-analyzer) | `schemas/risk_score.schema.json` |
| R3 | 제유호 ([@jeyuho](https://github.com/jeyuho)) | ML 이상탐지 | [#11](https://github.com/hoho-ajou/hoho_ajou/issues/11) | `docs/architecture_v1/design-03-ml-detector.md` | [결정 기록](../review/decisions.md#r3--ml-이상탐지) | `schemas/ml_result.schema.json` |
| R4 | 전선재 ([@ryanjeon1](https://github.com/ryanjeon1)) | Attack Path Engine + Dashboard | [#12](https://github.com/hoho-ajou/hoho_ajou/issues/12) | `docs/architecture_v1/design-04-attack-path.md`, `docs/architecture_v1/design-05-dashboard.md` | [결정 기록](../review/decisions.md#r4--attack-path-engine--dashboard) | `schemas/attack_graph.schema.json` |

R1은 총괄을 겸합니다(팀 구성상 4인이 5개 모듈+전체 조율을 나눠 맡음). 각 역할의 상세 목표·범위·완료조건은 위 상위 이슈(GitHub) 자체가 원본입니다.

## 스키마 승인 권한 (CODEOWNERS)

`schemas/*.json`을 바꾸는 PR은 위 표의 CODEOWNERS 대상 담당자 전원 승인이 있어야 병합됩니다. 실제 GitHub 아이디는 [`.github/CODEOWNERS`](../../.github/CODEOWNERS)에 반영되어 있습니다.
