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

**전제**: 에이전트 프레임워크마다 도구 선언 방식·설정파일 구조가 전부 달라 범용 탐지기를 만들기 어렵다. 4인 학부 프로젝트 규모에서는 하나로 고정해야 한다.

#### 2-1. 레지스트리: PyPI vs npm

| 기준 | PyPI | npm |
|---|---|---|
| AI 에이전트 생태계 연관성 | LangChain 등 주요 프레임워크의 원조 언어 | 부차적 버전만 존재 |
| 실제 공급망 공격 사례 | "Mini Shai-Hulud" 웜(2026년 5월)이 `mistralai`, `guardrails-ai`를 악성 버전으로 감염시켜 PyPI가 두 프로젝트를 격리 조치함[^1] | 웜의 최초 발원지(170개+ 감염) — 총량은 크지만 물량 공세형 |
| 데이터 접근성 | PyPI JSON API + OSV로 보완 용이 | 별도 조사 필요 |
| ML 학습용 악성 샘플 | `lxyeternal/pypi_malregistry`(PyPI 전용, 10,000+건) | 딱 맞는 데이터셋 없음 |
| 팀 스택 정합성 | Python 3.11+ 통일과 일치 | 어긋남 |

**근거**: 공격 사례 총량은 npm이 크지만, 나머지 4개 기준이 전부 PyPI를 가리키고 이번 학기 실행 가능성과 직결된다.

#### 2-2. 에이전트 프레임워크: LangChain vs 후보군

후보: LangChain, LlamaIndex, CrewAI, AutoGen, Semantic Kernel, OpenHands, Haystack

| 기준 | LangChain | 나머지 6개 |
|---|---|---|
| 언어/생태계 | Python(PyPI) | LlamaIndex·CrewAI·AutoGen·Haystack: Python. Semantic Kernel: C# 주력. OpenHands: TypeScript 주력 |
| 범용성 | 범용(도구+메모리+에이전트) | RAG 특화(LlamaIndex, Haystack) / 멀티에이전트 특화(CrewAI, AutoGen) / 코딩 전용(OpenHands) |
| MCP 공식 지원 | 공식 어댑터 `langchain-mcp-adapters` + `langchain[mcp]` extra (PyPI 확인) | — |
| GitHub 스타 수(2026-09 실측) | **146,273** | OpenHands 87,828 · AutoGen 60,975 · CrewAI 58,500 · LlamaIndex 52,153 · Semantic Kernel 28,556 · Haystack 26,506 |

**근거**: 범용성·MCP 공식 지원·대표성(스타 수) 3개 기준에서 LangChain이 명확히 우위다.

**MCP 채택 비율**은 topic 기준 LangChain 5.0%로 CrewAI(13.3%)·AutoGen(14.4%)보다 낮지만, 절대 저장소 수는 LangChain(1,275개)이 2위(CrewAI 321개)의 4배다. 표본 확보(목표 5종+)에는 절대량 기준이 맞다.

**최종 결정**: 분석 대상을 **PyPI 패키지 생태계 + LangChain(+MCP) 기반 AI 에이전트**로 확정. 그 외는 확장 과제로 남긴다.

**대상의 정의**: 분석 대상은 "AI로 만든 저장소"가 아니라 "LangChain을 import해 AI 에이전트를 구현한 저장소"다.

## 근거 문서

`docs/design/00-overall.md` §2, `docs/contracts/sample_dataset.md`(LangChain 기반 example-agent 시나리오)

[^1]: "Mini Shai-Hulud" 공급망 공격, 2026년 5월. [The Hacker News](https://thehackernews.com/2026/05/mini-shai-hulud-compromises.html)
