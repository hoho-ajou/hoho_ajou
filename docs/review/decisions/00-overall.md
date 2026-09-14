# 결정 기록 — 전체 파이프라인 오케스트레이션 & 모듈 간 계약 확립

## 상위 이슈

[#1](https://github.com/hoho-ajou/hoho_ajou/issues/1) — 오케스트레이션 방식과 모듈 간 인터페이스를 설계 문서 수준에서 확정

## 하위 이슈 분할

(하위 이슈 생성 전 — 담당자가 생성 후 채움)

## 결정 사항

### 결정 1 — 오케스트레이션 방식: 파일 기반 핸드오프 + 얇은 CLI

**결정하려 했던 것**: 모듈 간 통신을 공유 DB/메시지 큐로 할지, 파일 기반으로 할지.

**근거**: 4인 학부 프로젝트 규모에서 DB/큐 인프라는 과설계. Collector→(Risk Analyzer, ML 병렬)→Attack Path→Dashboard는 선형+한 번의 fan-out/fan-in 구조뿐이라 파일 핸드오프로 충분하며, 각 모듈이 독립 실행 가능해야 한다(담당자가 자기 모듈만 테스트할 때 다른 모듈이 안 떠 있어도 됨).

**최종 결정**: `schemas/`로 형식이 고정된 JSON 파일을 로컬 디스크에 순서대로 쌓고, 이를 순서대로 호출하는 얇은 Python CLI(`pipeline/run.py`)를 둔다. 모듈 간 데이터는 `data/<run_id>/*.json` 형태로 저장.

**(참고)** 이 CLI가 실제로 서브프로세스 호출인지 함수 호출인지는 아직 미정 — 총괄이 구현 착수 전 결정.

### 결정 2 — 분석 대상 확정: PyPI 생태계 + LangChain(+MCP) 에이전트

**결정하려 했던 것**: 어떤 패키지 레지스트리, 어떤 AI 에이전트 프레임워크를 분석 대상으로 삼을지. (팀 계획서 §4 "대상 범위 확정(PyPI+에이전트 1종)"의 실제 내용)

**전제**: 에이전트 프레임워크마다 도구 선언 방식(데코레이터/클래스/설정파일), import 네임스페이스, 연동 표준이 전부 달라 범용 탐지기를 만들기 어렵다. 4인 학부 프로젝트 규모에서는 여러 조합을 동시에 지원할 수 없어 하나로 고정해야 한다.

#### 2-1. 레지스트리: PyPI vs npm

| 기준 | PyPI | npm |
|---|---|---|
| AI 에이전트 생태계 연관성 | LangChain 등 주요 프레임워크의 원조 언어(아래 2-2 참고, 후보 7개 중 6개가 Python 기반) | 부차적 버전만 존재 |
| 실제 공급망 공격 사례 | "Mini Shai-Hulud" 웜(2026년 5월)이 PyPI의 `mistralai`(Mistral AI 공식 SDK), `guardrails-ai`를 악성 버전으로 감염시켜 PyPI가 두 프로젝트를 격리 조치함[^1] | 웜의 최초 발원지(npm 패키지 170개+ 감염) — 사례 총량은 더 크지만 물량 공세형이라 개별 패키지 맥락 분석 가치는 상대적으로 낮음 |
| 데이터 접근성 | PyPI JSON API(메타데이터+취약점) + OSV로 보완 용이 | 별도 조사 필요 |
| ML 학습용 악성 샘플 | `lxyeternal/pypi_malregistry`(PyPI 전용, 10,000+건) 확보 | PyPI 전용만큼 딱 맞는 데이터셋 없음 |
| 팀 스택 정합성 | Collector/Risk Analyzer/ML을 Python 3.11+로 통일한 것과 일치 | 스택 통일 방침과 어긋남 |

**근거**: 실제 공격 사례 총량은 npm이 크지만, 나머지 4개 기준(생태계 연관성·데이터 접근성·ML 샘플·스택 정합성)이 전부 PyPI를 가리키고, 이 4개가 "이번 학기 안에 파이프라인을 끝까지 완성할 수 있는가"와 직결되는 실행 가능성 기준이다.

> ⚠️ **정확성 주의**: `mistralai`/`guardrails-ai`는 LangChain으로 만들어진 패키지가 아니다. 이 사례는 "PyPI가 AI 툴링을 노린 실제 공급망 공격의 무대였다"는 **PyPI 선정 근거**로만 유효하며, 아래 2-2(LangChain 선정)의 근거로 전용해서는 안 된다.

#### 2-2. 에이전트 프레임워크: LangChain vs 후보군

후보: LangChain, LlamaIndex, CrewAI, AutoGen, Semantic Kernel, OpenHands, Haystack (AI 에이전트 개발에 쓰이는 대표 프레임워크)

| 기준 | LangChain | 나머지 6개 |
|---|---|---|
| 언어/생태계 | Python(PyPI) 기반 — JS 버전은 부차적 | 6개 중 Semantic Kernel 제외 전부 Python(PyPI) 전용이거나 부차적 |
| 범용성 | 범용(도구+메모리+에이전트) | RAG 특화(LlamaIndex, Haystack) 또는 멀티에이전트 오케스트레이션 특화(CrewAI, AutoGen) 또는 협소한 용도(코딩 전용 OpenHands) |
| MCP 공식 지원 여부 | 공식 어댑터 패키지 `langchain-mcp-adapters`(PyPI 실존 확인) + LangChain 1.4.0부터 `langchain[mcp]` extra 네이티브 지원(2026-09 PyPI JSON API 직접 조회로 확인) | 개별 확인 안 함(범용성 기준에서 이미 제외되는 후보들이라 우선순위 낮음) |
| 대표성/인기도(GitHub 스타 수, 2026-09 실측) | **146,273** | OpenHands 87,828 · AutoGen 60,975 · CrewAI 58,500 · LlamaIndex 52,153 · Semantic Kernel 28,556 · Haystack 26,506 — 전부 LangChain의 60% 미만 |
| 학습 자료 풍부함 | 스타 수 격차로 미루어 판단(정성적 추정, 별도 측정은 안 함) | 상대적으로 적을 것으로 추정 |

**근거**: 범용성·MCP 공식 지원·대표성(스타 수) 3개 기준에서 LangChain이 명확히 우위다. 학습 자료 항목은 실측이 아닌 정성적 추정임을 명시한다.

> ⚠️ **자체 정정 (편향 발견 및 수정)**: 처음에는 "GitHub topic:langchain+topic:mcp 동시 태그 저장소 1,275개"를 "LangChain이 MCP와 가장 잘 맞는다"는 근거로 제시했으나, 사용자 지적으로 재검증한 결과 이는 편향된 해석이었다. 같은 방식으로 다른 프레임워크의 **MCP 채택 비율**(해당 프레임워크 topic 전체 대비 +mcp 겹침 비율)을 조회하면:
>
> | 프레임워크 | topic 전체 | +mcp 겹침 | 채택 비율 |
> |---|---|---|---|
> | LangChain | 25,344 | 1,275 | 5.0% |
> | CrewAI | 2,413 | 321 | 13.3% |
> | AutoGen | 829 | 119 | 14.4% |
> | OpenHands | 82 | 17 | 20.7% |
> | Semantic Kernel | 471 | 34 | 7.2% |
> | LlamaIndex(`llamaindex`+`llama-index` 합산) | 1,600 | 90 | 5.6% |
> | Haystack | 226 | 6 | 2.7% |
>
> **LangChain의 MCP 채택 "비율"은 오히려 CrewAI·AutoGen·OpenHands보다 낮다.** 절대 개수(1,275)가 큰 건 LangChain의 전체 저장소 모수(25,344개)가 다른 후보보다 10~30배 많기 때문이지, MCP와 특별히 더 잘 맞아서가 아니다.
>
> **따라서 이 수치는 "LangChain이 MCP 친화적"이라는 근거로는 폐기하고, "PyPI+LangChain+MCP 조합 저장소가 절대량으로 1,275개 확보되어, 팀 목표(에이전트 샘플 5종+)를 채우는 데 지장이 없다"는 표본 확보 가능성 근거로만 재사용한다.** 채택 비율이 더 높은 CrewAI/AutoGen/OpenHands를 대신 택하지 않은 이유는 ①범용성(도구 호출 기반 에이전트라는 프로젝트 정의에 CrewAI/AutoGen의 멀티에이전트 오케스트레이션 특화, OpenHands의 코딩 전용이 덜 맞음)과 ②절대 표본 수(비율은 높아도 총량 자체가 훨씬 적음 — 특히 OpenHands는 17개뿐)가 여전히 LangChain 쪽으로 기울기 때문이다.

**반례 확인 (OpenClaw)**: "에이전트+외부 확장 요소로 인한 공급망 위험"이라는 위협 모델 자체는 LangChain뿐 아니라 OpenClaw(개인용 AI 어시스턴트, ClawHub 스킬 레지스트리로 확장) 같은 다른 에이전트 생태계에도 동일하게 존재함을 확인했다. 다만 OpenClaw는 TypeScript(npm) 기반이고 확장 단위가 pip 의존성이 아니라 자체 스킬/플러그인 레지스트리라 탐지 로직을 처음부터 새로 짜야 한다 — "위협 모델은 범용이지만 탐지 구현은 대상마다 새로 만들어야 한다"는 전제를 재확인했고, 향후 확장 과제 후보로 남겨둔다.

**최종 결정**: 분석 대상을 **PyPI 패키지 생태계 + LangChain(+MCP) 기반 AI 에이전트**로 확정. 그 외 레지스트리·프레임워크는 이번 학기 스코프에서 제외하고 확장 과제로 남긴다.

**대상의 정의(오해 방지)**: "AI로 만들어진 저장소"(AI 코딩 도구로 작성된 코드)가 아니라 "AI 에이전트를 구현한 저장소"(코드 자체가 LangChain을 import하고 실행하는 저장소)를 의미한다. 저장소가 사람이 짰는지 AI 도구로 짰는지는 분석 대상 여부와 무관하다.

## 근거 문서

`docs/design/00-overall.md` §2, `docs/contracts/sample_dataset.md`(LangChain 기반 example-agent 시나리오)

[^1]: "Mini Shai-Hulud" 공급망 공격, 2026년 5월. [The Hacker News](https://thehackernews.com/2026/05/mini-shai-hulud-compromises.html), [OX Security](https://www.ox.security/blog/shai-hulud-here-we-go-again-170-packages-hit-across-npm-pypi/), [Orca Security](https://orca.security/resources/blog/tanstack-npm-supply-chain-worm/)
