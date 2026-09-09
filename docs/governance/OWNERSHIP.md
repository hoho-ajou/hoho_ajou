# 역할과 담당자

전체는 하나의 Epic([#1](https://github.com/hoho-ajou/hoho_ajou/issues/1), 총괄 소유)이고, 그 아래 5개 모듈을 4명이 R1~R4로 나눠 맡습니다. 각자 상위 이슈(`docs/roles/*.md`, Epic #1을 승계)를 갖고, 그 안에서 하위 이슈를 직접 만들어 진행합니다.

| 역할 | 담당자 | 담당 모듈 | 상위 이슈 | 담당 문서 | 결정 기록 | CODEOWNERS 대상 |
|---|---|---|---|---|---|---|
| 총괄(PM) | (미정) | 전체 오케스트레이션 | [#1](https://github.com/hoho-ajou/hoho_ajou/issues/1) | `docs/design/00-overall.md` | [00-overall.md](../review/decisions/00-overall.md) | — |
| R1 | 배승원 ([@baeseungwon1010](https://github.com/baeseungwon1010)) | Dependency Collector | [`docs/roles/r1-collector.md`](../roles/r1-collector.md) | `docs/design/01-collector.md` | [r1-collector.md](../review/decisions/r1-collector.md) | `schemas/collector_output.schema.json` |
| R2 | (미정) | Risk Analyzer | [`docs/roles/r2-risk-analyzer.md`](../roles/r2-risk-analyzer.md) | `docs/design/02-risk-analyzer.md` | [r2-risk-analyzer.md](../review/decisions/r2-risk-analyzer.md) | `schemas/risk_score.schema.json` |
| R3 | (미정) | ML 이상탐지 | [`docs/roles/r3-ml-detector.md`](../roles/r3-ml-detector.md) | `docs/design/03-ml-detector.md` | [r3-ml-detector.md](../review/decisions/r3-ml-detector.md) | `schemas/ml_result.schema.json` |
| R4 | (미정) | Attack Path Engine + Dashboard | [`docs/roles/r4-attack-path-dashboard.md`](../roles/r4-attack-path-dashboard.md) | `docs/design/04-attack-path.md`, `docs/design/05-dashboard.md` | [r4-attack-path-dashboard.md](../review/decisions/r4-attack-path-dashboard.md) | `schemas/attack_graph.schema.json` |

R1은 총괄을 겸합니다(팀 구성상 4인이 5개 모듈+전체 조율을 나눠 맡음). 각 역할의 상세 목표·범위·완료조건은 `docs/roles/*.md`가 SSOT입니다(형식: [`docs/contracts/role_issue_schema.md`](../contracts/role_issue_schema.md)).

## 스키마 승인 권한 (CODEOWNERS)

`schemas/*.json`을 바꾸는 PR은 위 표의 CODEOWNERS 대상 담당자 전원 승인이 있어야 병합됩니다. 실제 GitHub 아이디는 팀원이 확정되는 대로 [`.github/CODEOWNERS`](../../.github/CODEOWNERS)에 채웁니다.

## 갱신 규칙

팀원 역할이 확정되면 이 문서의 "(미정)"을 실제 이름/GitHub 아이디로 채우고, 같은 커밋에서 `.github/CODEOWNERS`도 함께 갱신합니다.
