import type { Register } from 'claude-code'

// Prototype for three questions:
//   1. Can a tool.call hook put its own multi-choice dialog (allow / deny / details) before the tool runs?
//   2. After "deny", does the turn keep going (Claude receives the reason) instead of ending?
//   3. Can "details" show a rich view: H1 = a pane drawn with Markdown, H2 = details inside the question text.
// Reacts only to Bash commands containing the trigger word 새니대H (H1 / H2); everything else passes through.

const PANE = 'aasm-detail'

const ONE_LINE =
  '[AASM Guard] sample-pkg 0.1.0 — setup.py:6-7 base64 디코드 후 exec → 설치 시점에 자동 실행 → 개발자 PC 파일·자격증명 접근 가능(가능성)'

const DETAIL_MD = `## AASM Guard 상세 (프로토타입)

- **어디서**: sample-pkg 0.1.0 · setup.py:6-7 — base64 디코드 결과를 exec로 실행
- **어디를 통해서**: pip install 시 setup.py 자동 실행 (설치 시점, import 전)
- **어떤 위험까지**: 임의 코드 실행 → 개발자 PC의 파일·자격증명 접근 가능(가능성)

### 어디가 문제인가

\`\`\`python
  5  _blob = "cHJpbnQoJ2hlbGxvJyk="
  6  code = base64.b64decode(_blob)
  7  exec(code)
\`\`\`

### 왜 문제인가

디코드한 코드를 바로 실행하는 패턴. 실제 악성 패키지(pingdomv3)에서 관찰된 형태. 정상 용도일 수도 있으니 위치를 확인하세요.`

const DETAIL_PLAIN = [
  '어디서: sample-pkg 0.1.0 · setup.py:6-7 — base64 디코드 결과를 exec로 실행',
  '통해서: pip install 시 setup.py 자동 실행 (설치 시점, import 전)',
  '위험: 임의 코드 실행 → 개발자 PC의 파일·자격증명 접근 가능(가능성)',
  '문제 위치: 5 _blob = "cHJp..." / 6 code = base64.b64decode(_blob) / 7 exec(code)',
  '이유: 디코드한 코드를 바로 실행하는 패턴. 정상 용도일 수도 있음',
].join('\n')

export const register: Register = on => {
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const cmd: string = e.command ?? ''
    if (!cmd.includes('새니대H')) return next(e)

    const detailInQuestion = cmd.includes('새니대H2')
    let showedDetail = false

    for (let round = 0; round < 6; round++) {
      let question = `${ONE_LINE}\n\n어떻게 할까요?`
      if (detailInQuestion && showedDetail) {
        question = `${ONE_LINE}\n\n${DETAIL_PLAIN}\n\n어떻게 할까요?`
      }

      let choice: string
      try {
        choice = await $.ui.ask(question, {
          options: ['허용', '거부', '상세 보기'],
          header: 'AASM Guard',
        })
      } catch {
        // dialog dismissed: fail closed
        return { deny: '[AASM Guard] 확인 창이 닫혀 차단했습니다.' }
      }

      if (choice === '허용') return next(e)
      if (choice === '상세 보기') {
        showedDetail = true
        if (!detailInQuestion) {
          await $.ui.open({ id: PANE, title: 'AASM Guard 상세' })
        }
        continue
      }
      return { deny: `[AASM Guard] 사용자가 거부했습니다(${choice}): ${ONE_LINE}` }
    }

    return { deny: '[AASM Guard] 응답이 반복되어 차단했습니다.' }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Markdown } = $.ui.resolve(e)

    return (
      <Box flexDirection="column">
        <Markdown text={DETAIL_MD} />
      </Box>
    )
  })
}
