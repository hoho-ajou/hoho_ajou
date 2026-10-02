"""
Agent Dependency Guard - shared protected-path logic (T11: self-tampering guard).

Scope (per DESIGN.md T11): only Claude Code tool calls (Bash/Edit/Write) that
touch the files the guard itself depends on to run correctly - not just
settings.json, but the whole hook/scan_engine footprint, since the hook's own
fail-open design means breaking any of these has the same effect as disabling
it outright.
"""
from __future__ import annotations

import re
from pathlib import Path

# fragments matched against a raw path string (Bash command text or an
# Edit/Write tool_input.file_path) - deliberately broad substring matches,
# not exact paths, since both can appear relative, absolute, or ~-expanded.
# MCP config files are deliberately NOT in this list: they have their own,
# more specific T9 check (mcp_guard.check_new_mcp_servers) that distinguishes
# known from unknown servers, which a generic "protected path" flag would
# shadow - found via testing this exact collision (.mcp.json matched here
# first and the T9-specific message never fired).
PROTECTED_PATH_FRAGMENTS = [
    ".claude/settings.json",
    ".claude/settings.local.json",
    ".claude/hooks/",
    "agent-dependency-guard/",
]

# Bash-only: .mcp.json tampering via shell (sed/etc, not Edit/Write) has no
# diffing available, so it still falls under the generic T11 catch-all there.
BASH_PROTECTED_PATH_FRAGMENTS = PROTECTED_PATH_FRAGMENTS + [".mcp.json", ".claude.json"]

# command tokens that indicate the Bash command WRITES to whatever path it
# names, as opposed to just reading it (cat/grep/ls on a protected path is
# not a tampering attempt). Deliberately conservative: a write-looking token
# anywhere in the command is enough to flag, since under-flagging here is the
# expensive mistake (T11's whole point is "catch it before the safety net is
# gone").
_WRITE_INDICATOR = re.compile(
    r"\bsed\s+-i\b|\bmv\b|\brm\b|\bcp\b|\btruncate\b|\btee\b|\bchmod\b|>>?|\bdd\b"
)


def command_touches_protected_path(command: str) -> bool:
    """True if a Bash command both names a protected path and looks like it writes."""
    if not any(frag in command for frag in BASH_PROTECTED_PATH_FRAGMENTS):
        return False
    return bool(_WRITE_INDICATOR.search(command))


def file_path_is_protected(file_path: str) -> bool:
    """True if an Edit/Write tool_input.file_path targets a protected file."""
    return any(frag in file_path for frag in PROTECTED_PATH_FRAGMENTS)


def file_path_is_mcp_config(file_path: str) -> bool:
    """True if the path is specifically an MCP server config (T9's trigger)."""
    name = Path(file_path).name
    return name == ".mcp.json" or name == ".claude.json"
