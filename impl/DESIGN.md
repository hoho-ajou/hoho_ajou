# Agent Dependency Guard — 설계 정리

이 문서는 지금까지 논의된 내용(타겟, 자산, 위협, 정적/ML 구분, 파이프라인, MVP 계획)을 하나로 모은 정리본이다.
개별 실측 근거(BigQuery, git bisect 비용, 실제 악성패키지 검증 등)는 `AASM_SESSION_SUMMARY.md` 참고.

### 프로젝트 목적/스코프 정의

Agent Dependency Guard는 **공급망 보안(AI 에이전트가 설치하는 의존성) + 에이전트 도구배선 설계결함(Profile)**에 한정한다.
"AI 에이전트가 개발 과정에서 만들어내는 위협인가"가 아니라 **"공급망(외부에서 들어오는 코드/패키지/서버) 또는 에이전트 자신의 권한/도구 설계 문제인가"**를 기준으로 스코프를 가른다.
시크릿 유출(T6)처럼 결이 비슷해 보여도 이 기준에 안 걸리면(= 외부에서 들어온 게 아니라 내부에서 새어나가는 문제, 이미 전용 도구가 존재하는 인접 도메인) 자산/위협 목록에는 남기되 **명시적으로 제외**한다.

---

## 1. 대상 (Target)

- **최종 타겟**: AI 에이전트/LLM 앱을 직접 개발하는 개발자 (LangChain/MCP/LLM SDK로 에이전트를 만드는 사람)
- **로드맵**
  - **v1(MVP)**: **에이전트 저장소 여부와 무관하게, Claude Code로 개발하면 누구나 쓰는 범용 자동 가드.** 설치 게이트(T1/T2) + 가드 자기보호 3종(T9/T10/T11)만 포함. **Profile(에이전트 도구배선 분석, A4b 대상)은 V1에서 완전히 제외** — "지금 에이전트를 만드는 중"이라는 전제 자체가 없는 범용 시나리오엔 적용 대상이 없음
  - **v2**: 좁은 최종 타겟(에이전트 개발자) 전용 확장 — Profile 전체(LLM-SDK 분류, 도구배선 스캔, 트리거 확장 등)를 이때 추가

---

## 2. 자산 (Assets) — 로컬 개발 환경 한정

| 구분 | ID | 자산 |
|---|---|---|
| 개발 환경 | A1 | 로컬 파일시스템(소스코드, 설정파일, `.env`) |
| | A2 | AI 코딩 에이전트의 실행 권한(shell/file/network 호출 능력) |
| | A3 | 자격증명(LLM API 키, 클라우드 크리덴셜, git 토큰, DB 크리덴셜) |
| | A4 | Claude Code 확장 메커니즘(Skill 정의, MCP 서버 설정/바이너리, Hook 스크립트·`settings.json`, `.mcp.json`/`~/.claude.json`) — **개발도구 자신의 MCP 배선** |
| | A4b | (구분) 개발자가 만드는 에이전트 앱 자체의 MCP 배선 — Anthropic Messages API `mcp_servers`/`mcp_toolset` 요청 파라미터, Claude Agent SDK `mcpServers`/`ClaudeAgentOptions(mcp_servers=...)` — **A4와 별개 메커니즘(코드 안에만 존재, 파일 공유 없음)**, Profile(T4)의 스캔 대상 |
| | A5 | 전역 설정/인증 파일(`~/.npmrc`, `~/.pip.conf`, `~/.gitconfig`, `~/.netrc`, `gh`/`npm login` 토큰) — 리포 단위가 아닌 머신 전체 blast radius |
| | A6 | 패키지 매니저 로컬 캐시(`~/.cache/pip`, `~/.npm`, `node_modules`) — 실측 결과 훅 우회는 안 되지만, 캐싱 인프라 부재로 인한 비용 이슈는 남아있음 |
| | A7 | Git 서명/인증 키(SSH 키, GPG 커밋 서명 키) |
| | A8 | AI 코딩 에이전트 자체의 설치본/업데이트 채널(CLI 바이너리) — 재귀적 공급망 리스크 |
| | A9 | 로컬 세션/대화 기록(`~/.claude/projects/*.jsonl`) — 시크릿 누적 저장 위치 |
| | A10 | 컨테이너/이미지 빌드 자산(Dockerfile, `docker pull` 대상) |
| 코드/저장소 | B1 | 개발 중인 애플리케이션 소스코드(에이전트 도구 배선 로직 포함) |
| | B2 | 의존성 트리 및 lock file |
| | B3 | CI/CD 파이프라인 설정 및 시크릿 |
| 외부 신뢰 | D1 | 패키지 레지스트리(PyPI/npm) 무결성 신뢰 |
| | D2 | (해당 시) 개발자 자체 패키지 퍼블리싱 계정 |

---

## 3. 위협 (Threats) 및 스코프 배정

| ID | 위협 | 대상 자산 | 배정 | 비고 |
|---|---|---|---|---|
| T1 | 신규 악성/타이포스쿼팅 패키지 설치 | B2, A1, A3 | **v1** | 설치 게이트 |
| T2 | 기존 정상 패키지 계정탈취 후 악성배포 | B2 | **v1** | 레지스트리 이진탐색 아직 미통합(known gap) |
| T3 | CI/빌드 파이프라인 침투 | B3, B2 | **분리됨** | 사례 (a) 침투 결과 레지스트리에 악성 패키지가 올라간 경우(예: CI에서 토큰 탈취) → 로컬 설치 시점에 **T1/T2로 완전 흡수**, 별도 항목 불필요. 사례 (b) GitHub Actions 등 CI 러너에서만 실행되고 로컬에 설치가 전혀 안 일어나는 경우(예: tj-actions/changed-files) → **스코프 밖(확정)**, T7/T8과 동급 — v1/v2 구분이 아니라 로컬 개발단계 게이트라는 아키텍처 자체의 구조적 한계 |
| T4 | LLM 출력 → 위험 싱크 직결(프롬프트 인젝션→RCE) | A2, A1, A4b | **v2 전체(Profile 대상이라 V1 범용가드엔 미포함)** | Agent SDK 공식문서로 확인: `bypassPermissions`/`allowedTools`로 자동승인된 툴은 `canUseTool` 콜백에 도달 못 함, 하드 게이트는 `PreToolUse` 훅만 가능 — Hook 기반 설계 근거 자체는 유효하지만, 이 위협의 스캔 대상(A4b, 개발자가 짜는 에이전트 코드)은 "에이전트를 만드는 중"이 전제라 V1 범용가드 범위 밖. v2에서 Profile과 함께 구현 |
| T5 | MCP 서버 과다권한 설정 | A4, A4b | **A4 부분은 V1(T9 로직과 통합) / A4b 부분은 v2** | A4(`.mcp.json`/`~/.claude.json`, Claude Code 자체 MCP)는 누구나 해당되므로 V1에 포함, 사실상 T9와 같은 훅이 처리. A4b(코드 내 `mcp_servers`/`ClaudeAgentOptions` 등, 개발자가 짜는 에이전트 앱의 MCP)는 Profile 대상이라 v2 |
| T6 | 시크릿 노출(LLM 컨텍스트/커밋/로그, A3/A9) | A3, A9 | **스코프 밖(확정)** | 프로젝트 목적 기준(0장) 위반: 외부에서 들어오는 위협이 아니라 내부에서 새어나가는 문제. gitleaks/trufflehog 등 전용 도구 존재. 자산/위협 목록에는 유지하되 명시적으로 제외 |
| T7 | 레지스트리 자체 무결성 훼손(Dependency Confusion) | D1 | **스코프 밖(확정)** | 기존 결정 유지 |
| T9 | 악성/신뢰 불가 MCP 서버 등록 | A4 | **v1(단순 allowlist) / v2(평판 스코어링)** | T5와 달리 "권한 과다"가 아니라 "출처 자체가 의심"인 케이스. **공식 문서로 확인**: Claude Code는 대화형 세션에서만 프로젝트 스코프 MCP 서버에 승인 프롬프트+workspace trust를 요구하고, **비대화형 세션(SDK/`-p`/cloud)에서는 승인 없이 자동 로드**됨 — 이게 정확히 Guard가 메워야 할 gap. 구현은 T1 스캔 로직 재사용 가능: `.mcp.json`/`~/.claude.json`에 대한 Write/Edit을 PreToolUse 훅으로 감지 → 신규 서버 엔트리를 allowlist/엔트로피·키워드로 스캔 |
| T10 | Skill/Hook 스크립트 자체 변조 | A4 | **v1(체크섬/diff)** | 프로젝트 최초 설치 시점 `.claude/hooks/*`/`SKILL.md`의 sha256을 매니페스트로 저장, 이후 체크포인트마다 현재 체크섬과 비교해 불일치 시 REVIEW. 저장소 clone·템플릿 복사 경로로 오염 유입 가능 |
| T11 | 가드 자체 무력화(self-tampering) | A4 | **v1(스코프 좁힘)** | **스코프**: Claude Code 툴 호출(Bash/Edit/Write)을 통해 보호 경로(`settings.json`/`.claude/hooks/`/`agent-dependency-guard/`)가 건드려지는 경우만. 원인(개발자의 정당한 유지보수 vs 프롬프트 인젝션에 넘어간 에이전트 vs 그 외)은 구분하지 않고 **행위 기반으로 원인 불문 게이트** — Hook은 "왜"가 아니라 "무엇"만 봄, 이게 Hook 방식의 본질적 장점이라 프롬프트 인젝션을 별도로 탐지/방어할 필요가 없음(그건 모델 레벨 문제로 스코프 밖). **구조적 약점**: 훅 자신의 설계 원칙이 미인식 입력/에러 시 fail-open이라 직접 끄지 않고 에러만 나게 만들어도 무력화와 동일한 효과 — 보호 대상은 `settings.json`뿐 아니라 훅이 의존하는 전체 파일. **명확한 스코프 제외**: 이미 승인/미탐지 통과된 악성 패키지의 설치 스크립트(`setup.py`)가 OS 레벨에서 직접 파일을 쓰는 경로는 Claude Code 툴 호출이 아니라서 T11이 원천적으로 못 봄 — 이건 T11의 결함이 아니라 **T1(`install_hook` 탐지) 정확도에 종속되는 별개 문제**로 명시. **v1 탐지**: 기존 `PreToolUse(Bash)`에 보호 경로 대상 수정 명령(`sed`/`>`/`mv`/`rm`/`cp` 덮어쓰기) 패턴 추가 + `PreToolUse(Edit\|Write)` 신설(Profile 실현가능성 실측에서 검증된 것과 동일 구조, 즉시 재사용 가능). **판정**: 무조건 REVIEW(정당한 유지보수와 공격을 자동 구분 불가하므로 항상 사람 확인 강제) |
| T8 | 배포 후 프로덕션 공격표면 | C1-C3 | **스코프 밖** | 팀 전체 AASM 파이프라인(Attack Path Engine) 몫, Guard는 개발단계 게이트 |

> T3/T6/T9/T10/T11 배정 전부 확정됨.

---

## 4. 정적 규칙 vs ML — 구분 기준: "명확한 건 정적으로, 불명확한 건 ML"

### 4-1. 정적 규칙(Deterministic)으로 처리

객관적 사실 확인이거나, 존재/부재를 규칙으로 명확히 정의할 수 있는 것들.

| 항목 | 이유 |
|---|---|
| OSV/CVE 조회 + CRITICAL 등급 하드 BLOCK | 외부 신뢰 DB와의 단순 매치, 판단 여지 없음 |
| `install_hook` 존재 여부(`cmdclass=`, `run(self)` 등) | 코드 패턴의 존재/부재는 이분법 |
| 버전 공백/삭제 이력 | 레지스트리 API 조회로 나오는 팩트 |
| `package_age_days`, `maintainer_count`, `has_readme` 등 메타데이터 | 팩트 값, 해석 없이 그대로 사용 |
| LLM Provider SDK import 탐지(openai/anthropic/... 문자열) | Profile의 1차 분류(에이전트 프로젝트 여부), 존재 여부 판단만 필요 |
| MCP 설정 파일의 권한 범위 파싱 | 설정 스키마상 명시된 권한 필드를 그대로 읽는 것 |
| `decode_then_exec`/`download_then_execute`/`environment_gate` **체인 구조** | "A 호출 직후 B 호출"이라는 구조 자체는 AST/정규식으로 명확히 정의 가능(실제로 pingdomv3/ultralytics 실사례에서 검증됨) |
| Hook/Skill 파일 자체의 변경 감지(T10) | 체크섬/diff 존재 여부는 이분법 |
| 타이포스쿼팅 편집거리(레벤슈타인) | 계산식이 고정, 임계값만 있으면 됨 |
| 소스코드 내 MCP 배선 패턴(`mcp_servers`/`mcp_toolset`, `ClaudeAgentOptions(mcp_servers=...)`, `options.mcpServers`) | 문자열/AST 패턴 존재 여부, Profile 1차 탐지 |
| **`permissionMode: bypassPermissions`(또는 동등 설정) + MCP 배선 동시 존재** | Agent SDK 문서로 확인된 실제 우회 경로("자동승인된 툴은 검증 콜백에 안 감") — install_hook+keyword 조합과 같은 구조의 하드룰 |

### 4-2. ML 후보 — 불명확/복합/통계적 판단이 필요

개별 신호는 정적으로 뽑아내되, **그 신호들을 어떻게 종합 판단할지**가 문맥·통계에 의존하는 것들. 실측으로 확인된 두 실패 사례(pingdomv3 미탐, requests 오탐)가 전부 여기 해당.

| 항목 | 이유 |
|---|---|
| **entropy/keyword 등 연속값의 최종 결합(스코어링)** | 지금 고정 가중합(`WEIGHTS`)이 두 방향 모두 실패(실제 악성 pingdomv3를 ALLOW로 미탐, 정상 requests를 BLOCK로 오탐)한 것을 실측으로 확인 — 고정 규칙이 아니라 학습된 분류기가 필요한 영역 |
| 정상 라이브러리의 "정당한 키워드 사용" vs 악성 코드 구분 | `socket.socket(`/`compile(`을 requests가 쓰는 것과 악성 패키지가 쓰는 것을 키워드 카운트만으로 구분 불가 — 문맥 의존 |
| 레지스트리 버전 이력의 궤적 이상탐지(선형보간 대비 급증 등) | 통계적 이상치 판단, 고정 임계값으로는 패키지마다 정상 범위가 다름 |
| 메인테이너/이메일 변경의 "정상 교체 vs 탈취" 구분 | 단순 불연속 존재 여부(정적으로 확인 가능)와 달리, "이 변경 패턴이 자연스러운가"는 통계적 판단 |
| Agent/MCP 데이터플로(taint): LLM 출력이 위험 싱크까지 도달하는 경로 | "진짜 위험 경로"와 "우연히 비슷해 보이는 안전 경로"를 그래프 구조만으로 못 자름 — 라벨 데이터 필요(현재 미확보) |
| 코드 난독화 정도 종합 판단(AST 구조 이상, 변수명 무작위성 등) | 여러 약한 신호의 복합 판단, 단일 규칙으로 표현 어려움 |
| 신규/무명 MCP 서버의 평판 스코어링(T9의 v2 단계) | 단순 allowlist(v1)로 못 끝나는 회색지대 — 그레이존 판단은 ML 영역 |

**원칙**: ML은 "개별 신호 추출"이 아니라 "신호들의 종합 판단"에만 투입한다. 신호 추출 자체(entropy 계산, 키워드 카운트, 체인 패턴 매치)는 계속 정적 로직으로 하고, 그 출력을 규칙 기반 가중합 대신 학습된 분류기(Random Forest 등, 계획 상 중기 과제)에 넣는 구조로 간다.

---

## 5. 전체 파이프라인

**훅 등록 지점은 총 3개** — 아래에서 각각 무엇을 보는지 먼저 정리:

| 훅 | 매처 | 역할 | 범위 |
|---|---|---|---|
| `PostToolUse` | `Edit\|Write` | Profile 로거 — 모든 파일 수정을 append-only로 기록(분석 없음, 거의 무료). 실측으로 `structuredPatch`(diff)/`content`가 이미 이벤트에 포함됨을 확인 | **v2** |
| `PreToolUse` | `Bash` | (a) pip/npm install 명령 감지 → 패키지 스캔(T1/T2) (b) 보호 경로(`settings.json`/`.claude/hooks/`/`agent-dependency-guard/`) 대상 수정 명령(`sed`/`>`/`mv`/`rm`/`cp` 덮어쓰기) 감지 → T11 REVIEW | v1 |
| `PreToolUse` | `Edit\|Write` | (a) `file_path`가 `.mcp.json`/`~/.claude.json`이면 → 새 MCP 서버 엔트리 추출 → T9 allowlist 스캔 (b) `file_path`가 보호 경로면 → T11 REVIEW(Bash를 안 거치고 직접 편집하는 경우까지 커버) | v1 |

**Profile의 파이프라인 위치 (v2, 결정됨)**: Profile은 별도의 새 체크포인트를 만들지 않는다. `PostToolUse(Edit|Write)`가 평소에 조용히 로그만 쌓고(분석 없음), **기존 설치 체크포인트(`PreToolUse(Bash)`)가 발동하는 순간 그 누적 로그를 session_id로 묶어서 한꺼번에 배치 스캔**한다 — 패키지 스코어링과 Profile 스코어링이 같은 판정 지점에서 합쳐지는 구조. 이게 가능한 이유는 session_id가 한 세션 내내 안정적으로 유지된다는 걸 실측으로 확인했기 때문(6장 참고). **단, 이 구조는 "설치 이벤트 없이 위험한 코드를 바로 실행하는 경우"를 못 잡는다는 한계가 있고(안건 A), 이 gap을 메울 유휴/주기적 2차 트리거(안건 B) 도입 여부는 아직 열린 질문.**

**메인 체크포인트 흐름 (v1, 설치 게이트가 발동하는 순간)**:
```
Skill 설치(가이드/문서 제공)
   ↓
[체크포인트 트리거] PreToolUse(Bash) 훅 — pip/npm install 감지
   ↓
정적 분석(엔트로피/키워드/install_hook/체인 패턴/타이포스쿼팅)
   + T10 체크섬 비교(설치 시점 파일 vs 최초 설치 매니페스트)
   + (v2) Profile 배치 스캔(session_id로 묶은 누적 Edit/Write 로그)
   ↓
OSV 취약점 조회 + (v2) 레지스트리 버전 이력 이진탐색
   ↓
스코어링: 정적 하드룰(4-1) + ML 종합판단(4-2, 중기 과제 전까지는 룰 기반 가중합으로 대체)
   ↓
위험도 기반 판정: ALLOW(통과) / NEEDS_HUMAN_REVIEW(deny+사유 표시, 재확인 후 진행) / BLOCK(deny)
   ↓
승인 시 계속 진행, 거부 시 사유와 함께 차단
```

**독립 체크포인트** (메인 체크포인트를 기다리지 않고 즉시 REVIEW 발동 — 위 표의 (b)/T9/T11):
```
PreToolUse(Bash 또는 Edit/Write) — 보호 경로 수정 감지 → 즉시 REVIEW (T11)
PreToolUse(Edit/Write) — .mcp.json/~/.claude.json 수정 감지 → 신규 서버 즉시 스캔 → REVIEW/ALLOW (T9)
```
이 둘은 "설치"라는 이벤트를 기다리지 않는 이유가 있음 — 3장에서 정리했듯 T9/T11은 "다음 체크포인트가 오기 전에 안전망 자체가 사라질 수 있는" 성격이라, 설치 체크포인트와 별도로 즉시 게이트해야 함.

---

## 6. MVP(v1) 계획

**V1 스코프 (범용 가드 — Profile 전체 제외)** — 전부 구현 및 실측 완료
- 설치 게이트: `scan_engine.py` + `hooks/pretooluse_check.py` — pyyaml==5.3.1 → BLOCK(CRITICAL CVE), requests==2.31.0 → ask(REVIEW, MODERATE CVE), `ls` → 통과
- `decode_then_exec`/`download_then_execute` 하드룰: 같은 파일 내 디코드/다운로드 호출과 실행 호출이 `CHAIN_LINE_WINDOW`(=8)줄 이내면 무조건 BLOCK — 숫자는 시작값, 실측하며 조정 예정
- entropy/keyword 정규화: 키워드 분모를 `max(3, py_file_count*2)`로 패키지 크기에 비례(이전 고정값 10 대비) + `tests?/` 경로/`test_*.py`는 애초에 집계 제외 — requests 키워드 27→4건으로 정상화
- 가드 자기보호 3종 구현: `guard_paths.py`(T11 보호경로 패턴) / `integrity.py`(T10 체크섬, 첫 호출 시 자동 매니페스트 생성) / `mcp_guard.py`(T9 allowlist+스냅샷 diff) / `hooks/pretooluse_editwrite_check.py`(T9+T11용 신규 Edit|Write 훅) / `SETTINGS_SNIPPET.json`에 두 번째 훅 등록 반영
- REVIEW 판정을 `deny`가 아니라 `ask`로 전환 — Claude Code의 표준 승인 팝업을 사람에게 직접 띄움(공식문서로 `ask` 값 존재 확인, 다지선다는 안 되고 허용/거부 이진 팝업만 가능)
- **Profile(PostToolUse 로깅, 에이전트 도구배선 분석)은 V1에서 완전히 제외 — v2로 이월**

**구현하며 실측으로 발견/수정한 버그 (설계 문서엔 없던 것)**
- OSV 심각도 파싱 버그: `severity[].score`가 CVSS 벡터 문자열(`CVSS:3.1/AV:N/...`)이라 "CRITICAL" 리터럴 매치가 원천적으로 불가능했음 — CRITICAL 하드룰이 한 번도 발동 못 하고 있었음. `database_specific.severity` 필드로 수정, pyyaml 5.3.1 실제 CRITICAL CVE로 재검증 완료
- 키워드 매칭이 `re.compile(`도 `compile(`로 오매치(앞에 `.`이 와도 무시) — bare builtin 4종만 `(?<![\w.])` 경계 추가로 수정
- MCP allowlist 체크가 `command+args`를 합친 문자열 전체로 `startswith` 비교해서 `"npx @modelcontextprotocol/server-..."`처럼 앞에 실행기가 붙으면 항상 실패 — 토큰 단위 비교로 수정
- `.mcp.json`이 T11의 일반 보호경로 목록에도 들어있어서 T9 전용 메시지(known/unknown 서버 구분)가 한 번도 안 뜨고 T11 메시지로 덮어써짐 — T9를 먼저 체크하도록 순서 수정, `.mcp.json`은 T11 일반 목록에서 제외

**알려진 한계(v1에서 의도적으로 미해결, v2로 이월)**
- Profile 전체(T4 잔여분, T5의 A4b 부분, LLM-SDK 분류, 도구배선 스캔) — "에이전트를 만드는 중"이 전제인 기능이라 범용 가드엔 적용 대상 자체가 없음
- (패키지,버전) 캐싱 인프라 부재 — 매 설치마다 전체 재스캔(성능 이슈, 보안 이슈는 아님 — A6 실측으로 확인됨)
- 룰 기반 스코어링 → ML(Random Forest) 전환 전까지는 오탐/미탐 둘 다 존재 가능(실측 확인된 기지 사실)
- T11 fail-open 구조 자체의 근본적 tension(보호 경로 밖 간접 파손 경로) — v1/v2 모두 완전 해결 어려움, 알려진 한계로 명시

**v2 계획 (에이전트 저장소 전용 확장)**
- Profile 전체 신규 구현: PostToolUse(Edit/Write) 로깅(실현가능성은 이 세션에서 실측 확인함 — session_id 상관관계 안정적, `structuredPatch`/`content`로 diff 데이터 확보 가능), LLM-SDK 분류, 도구배선 스캔(T4 잔여분, T5의 A4b 부분), 트리거 확장(안건 B: 유휴/주기적)
- 레지스트리 버전 이력 이진탐색+궤적분석을 `scan_engine.py`에 정식 통합
- (패키지,버전) 결과 캐싱 계층
- 실제 라벨 데이터 기반 ML(Random Forest)로 4-2 항목 전체 대체
- T9 정교화(MCP 서버 평판 스코어링)
- Risk Analyzer/Attack Path Engine/Dashboard(팀 전체 파이프라인)와의 통합
