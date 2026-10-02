#!/usr/bin/env python3
"""
Agent Dependency Guard - PreToolUse hook for Claude Code (MVP)

Wire this into .claude/settings.json as a PreToolUse hook on the Bash tool.
It reads the hook event JSON from stdin, checks whether the command being
run is a package-manager install, and if so scans the package(s) before
letting the command proceed.

Claude Code PreToolUse hook contract (verified against
https://code.claude.com/docs/en/hooks.md):
  - stdin: JSON with at least {"tool_name": "Bash", "tool_input": {"command": "..."}}
  - stdout: JSON with a nested permission decision:
        {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                 "permissionDecision": "deny",
                                 "permissionDecisionReason": "..."}}
    (no output / exit 0)  # fall through to normal permission flow
  - exit code 2 ALSO blocks unconditionally, regardless of stdout JSON (belt-and-braces;
    not used here since we want the reason to reach the user, which requires the JSON form)

This script only *inspects* the command; it never rewrites it. If the
package manager syntax evolves beyond what INSTALL_PATTERNS covers, this
hook fails open (falls through) rather than silently blocking unrelated
commands - false negatives are safer than accidentally blocking a
developer's unrelated Bash command.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scan_engine import scan_package  # noqa: E402
from guard_paths import command_touches_protected_path  # noqa: E402
from integrity import check_integrity  # noqa: E402

# name/version extraction is intentionally conservative: unrecognized syntax
# (e.g. `pip install -e .`, extras `pkg[extra]`, VCS urls) is left alone and
# falls through to normal permission handling rather than guessing.
INSTALL_PATTERNS = [
    re.compile(r"\bpip3?\s+install\s+(?!-e\b)(?P<args>[^|&;]+)"),
    re.compile(r"\bnpm\s+install\s+(?P<args>[^|&;]+)"),
    re.compile(r"\bnpm\s+i\s+(?P<args>[^|&;]+)"),
]

PKG_TOKEN = re.compile(r"^([A-Za-z0-9_.\-]+)(?:==|@)?([A-Za-z0-9_.\-]*)$")


def extract_packages(command: str) -> list[tuple[str, str | None]]:
    packages = []
    for pattern in INSTALL_PATTERNS:
        m = pattern.search(command)
        if not m:
            continue
        for token in m.group("args").split():
            if token.startswith("-"):
                continue
            m2 = PKG_TOKEN.match(token)
            if not m2:
                continue
            name, version = m2.group(1), m2.group(2) or None
            packages.append((name, version))
    return packages


def main() -> None:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw)
    except Exception:
        return  # malformed input -> fall through, don't block

    if event.get("tool_name") != "Bash":
        return

    command = event.get("tool_input", {}).get("command", "")

    def respond(decision: str, reason: str) -> None:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": decision,
                "permissionDecisionReason": reason,
            }
        }, ensure_ascii=False))

    # T11: a command that writes to a protected guard path is the
    # higher-priority finding - check it before deciding whether this is
    # even an install command at all.
    if command_touches_protected_path(command):
        respond("ask", "Agent Dependency Guard: 가드 보호 경로에 대한 수정 명령이 감지되었습니다 "
                "(설정/훅 스크립트 변경). 정당한 유지보수인지 확인 후 진행하세요.\n"
                f"명령어: {command}")
        return

    packages = extract_packages(command)
    if not packages:
        return  # not an install command -> fall through

    blocked, review, allowed = [], [], []
    for name, version in packages:
        result = scan_package(name, version)
        entry = {"name": name, "version": version, "verdict": result.verdict,
                  "score": result.score, "reasons": result.reasons}
        if result.verdict == "BLOCK":
            blocked.append(entry)
        elif result.verdict == "NEEDS_HUMAN_REVIEW":
            review.append(entry)
        else:
            allowed.append(entry)

    # T10: this install checkpoint doubles as the integrity checkpoint -
    # compare the guard's own files against their manifest every time.
    integrity_findings = check_integrity()

    if blocked:
        respond("deny", "Agent Dependency Guard가 설치를 차단했습니다:\n" +
                json.dumps(blocked, ensure_ascii=False, indent=2))
        return

    if review or integrity_findings:
        # NEEDS_HUMAN_REVIEW -> "ask": surfaces Claude Code's normal allow/deny
        # prompt to the human instead of silently blocking (deny) or letting
        # the agent decide on its own (allow). Verified against official docs:
        # ask shows the interactive permission prompt with this reason text.
        reason_parts = []
        if review:
            reason_parts.append("사람 검토가 필요한 패키지:\n" +
                                 json.dumps(review, ensure_ascii=False, indent=2))
        if integrity_findings:
            reason_parts.append("가드 자체 무결성 이상:\n" +
                                 json.dumps(integrity_findings, ensure_ascii=False, indent=2))
        respond("ask", "Agent Dependency Guard:\n" + "\n".join(reason_parts))
        return

    # all ALLOW, no integrity findings -> fall through silently (no stdout)
    # so the command proceeds normally


if __name__ == "__main__":
    main()
