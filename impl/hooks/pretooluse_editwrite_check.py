#!/usr/bin/env python3
"""
Agent Dependency Guard - PreToolUse hook for Edit|Write (Claude Code).

Two independent checks, both "ask" (not silent deny) since both need a human
to actually look, not an automatic block:
  - T9: file_path is an MCP config (.mcp.json / ~/.claude.json) -> diff
        against the stored snapshot, flag any new server entry not on the
        known-source allowlist.
  - T11: file_path is a protected guard path (settings.json, hook scripts,
        this package itself) being edited directly, bypassing Bash entirely.

Wire into .claude/settings.json as a PreToolUse hook on Edit|Write, same
contract as pretooluse_check.py (verified against
https://code.claude.com/docs/en/hooks.md).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from guard_paths import file_path_is_mcp_config, file_path_is_protected  # noqa: E402
from mcp_guard import check_new_mcp_servers  # noqa: E402


def ask(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }, ensure_ascii=False))


def main() -> None:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw)
    except Exception:
        return  # malformed input -> fall through, don't block

    if event.get("tool_name") not in ("Edit", "Write"):
        return

    file_path = event.get("tool_input", {}).get("file_path", "")
    if not file_path:
        return

    # T9 first: .mcp.json/~/.claude.json get the specific known-vs-unknown
    # server diff, not the generic T11 message (guard_paths deliberately
    # keeps these out of PROTECTED_PATH_FRAGMENTS so they reach here).
    if file_path_is_mcp_config(file_path):
        new_entries = check_new_mcp_servers(file_path)
        unknown = [e for e in new_entries if not e["known"]]
        if unknown:
            ask("Agent Dependency Guard: 신뢰 목록에 없는 MCP 서버가 새로 등록되었습니다:\n" +
                json.dumps(unknown, ensure_ascii=False, indent=2))
        # known entries, or no new entries at all -> fall through silently
        return

    if file_path_is_protected(file_path):
        ask(f"Agent Dependency Guard: 가드 보호 경로({file_path})에 대한 직접 수정이 감지되었습니다. "
            "정당한 유지보수인지 확인 후 진행하세요.")
        return


if __name__ == "__main__":
    main()
