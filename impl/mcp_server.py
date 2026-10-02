"""
Agent Dependency Guard - MCP server (MVP)

Exposes one tool:
    scan_package(name: str, version: str | None) -> {verdict, score, reasons}

Run standalone for a quick manual check:
    python3 mcp_server.py requests
    python3 mcp_server.py pyyaml 5.3.1

Wire into Claude Code / any MCP client via stdio transport:
    python3 mcp_server.py --serve
"""
from __future__ import annotations

import json
import sys

from scan_engine import scan_package


def scan_package_tool(name: str, version: str | None = None) -> dict:
    result = scan_package(name, version)
    return {
        "verdict": result.verdict,
        "score": result.score,
        "reasons": result.reasons,
        "resolved_version": result.features.resolved_version,
    }


def _run_stdio_server() -> None:
    """Minimal JSON-RPC-over-stdio loop so this can be wired as an MCP tool
    without requiring the official MCP SDK to be installed. Each line in is
    {"name": <pkg>, "version": <ver or null>}; each line out is the tool result."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            out = scan_package_tool(req.get("name"), req.get("version"))
        except Exception as e:
            out = {"error": str(e)}
        sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    if "--serve" in sys.argv:
        _run_stdio_server()
    else:
        pkg = sys.argv[1] if len(sys.argv) > 1 else "requests"
        ver = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(scan_package_tool(pkg, ver), ensure_ascii=False, indent=2))
