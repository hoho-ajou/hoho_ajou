"""
Agent Dependency Guard - T9: untrusted/unknown MCP server registration guard.

Context (verified against Claude Code docs this session): interactive
sessions already get an approval prompt before a project-scoped MCP server's
first use, but non-interactive sessions (SDK/-p/cloud) load it without
prompting. This module closes the gap for the interactive case too, at the
point of *registration* (an Edit/Write to .mcp.json / ~/.claude.json),
instead of relying only on Claude Code's own first-use prompt.

A snapshot of the last-seen config is kept locally so only *new* server
entries are flagged - not ones already reviewed in a previous checkpoint.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

GUARD_DIR = Path(__file__).resolve().parent
SNAPSHOT_PATH = GUARD_DIR / "aasm_mcp_snapshot.json"

# starting allowlist: well-known, officially-published MCP servers. Empty-ish
# on purpose for V1 - the point isn't to pre-approve everything plausible,
# it's to flag anything NOT on this short, deliberately curated list so a
# human looks at it once. Grows over time as the team reviews real servers.
KNOWN_SOURCE_PREFIXES = [
    "@modelcontextprotocol/server-",
    "@anthropic-ai/",
]


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def _server_entries(config: dict[str, Any]) -> dict[str, Any]:
    return config.get("mcpServers", {})


def _server_source(entry: dict[str, Any]) -> str:
    """The string we check against the allowlist / scan for risk signals."""
    if "command" in entry:
        return " ".join([entry.get("command", "")] + entry.get("args", []))
    return entry.get("url", "")


def _is_known_source(source: str) -> bool:
    # source is "command arg1 arg2 ..." (e.g. "npx @modelcontextprotocol/server-filesystem")
    # or a bare url - check each token, not the joined string, since a known
    # package name is rarely the first token (npx/uvx/python -m usually is).
    # Found via testing: the joined-string startswith() never matched because
    # "npx " always came first.
    tokens = source.split()
    return any(tok.startswith(prefix) for tok in tokens for prefix in KNOWN_SOURCE_PREFIXES)


def check_new_mcp_servers(file_path: str) -> list[dict[str, Any]]:
    """Diffs the current config at file_path against the stored snapshot.

    Returns a list of {name, source, known} for entries that are new since
    the last checkpoint. Always updates the snapshot afterward, so an entry
    is only ever surfaced once (reviewed-or-not, it doesn't keep re-firing on
    every subsequent install checkpoint).
    """
    current = _load_json(Path(file_path))
    current_servers = _server_entries(current)

    snapshot = _load_json(SNAPSHOT_PATH)
    previous_servers = snapshot.get(file_path, {})

    new_entries = []
    for name, entry in current_servers.items():
        if name in previous_servers:
            continue
        source = _server_source(entry)
        new_entries.append({
            "name": name,
            "source": source,
            "known": _is_known_source(source),
        })

    snapshot[file_path] = current_servers
    SNAPSHOT_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False))

    return new_entries
