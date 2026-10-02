---
name: agent-dependency-guard
description: Scans a Python/Node package for supply-chain risk (typosquatting, known CVEs via OSV, obfuscated/entropy-heavy code, suspicious install hooks) before it gets installed, and reports ALLOW / NEEDS_HUMAN_REVIEW / BLOCK with reasons. Use whenever the user asks to check, scan, vet, or audit a package before installing it, or whenever you (Claude) are about to run `pip install`/`npm install` for a package you were not explicitly told to install by name+version (i.e. you chose it yourself while solving a task) - proactively scan those before running the install.
---

# Agent Dependency Guard

## When to use this

- User says "이 패키지 설치해도 안전해?", "scan this package", "이거 설치 전에 확인해줘"
- You (the agent) are about to `pip install` / `npm install` a package **that you chose yourself**
  (not one the user explicitly named) as part of solving some other task. Scan it first,
  proactively, before running the install - this is the main point of this skill existing.
- A `PreToolUse` hook (see `hooks/pretooluse_check.py`) already intercepts raw `pip install`/
  `npm install` Bash commands automatically and can block/flag them before they run - this
  skill is for the cases the hook doesn't cover (already-installed packages, "should I trust X",
  packages referenced only in a manifest file you're about to add).

## What it does NOT do

- It does **not** run the package's install scripts or import its code (no dynamic execution -
  see stage 5 in `INTERFACES.md` for the planned sandboxed-execution extension, not implemented yet).
- It does **not** guarantee safety - `ALLOW` means "no known red flags found by this MVP's rules",
  not "verified safe". Treat `NEEDS_HUMAN_REVIEW` as "ask the user before proceeding", and `BLOCK`
  as "do not install without the user explicitly overriding".

## How to use it

Run the scanner directly and read the JSON result:

```bash
python3 <path-to-this-skill>/scan_engine.py <package_name> [version]
```

Example:

```bash
python3 scan_engine.py pyyaml 5.3.1
```

```json
{
  "verdict": "BLOCK",
  "score": 0.6,
  "reasons": [
    "OSV 취약점 2건 발견 (최고 심각도: None)",
    "위험 키워드 194회 검출: {...}",
    "setup.py에 커스텀 install hook 존재",
    "[하드룰] install hook + 위험 키워드 동시 존재 → 최소 리뷰 필요"
  ]
}
```

## What to do with the result

- `ALLOW` → proceed with the install normally.
- `NEEDS_HUMAN_REVIEW` → **stop and tell the user** the specific reasons before installing;
  do not silently proceed even if you think the reasons look minor.
- `BLOCK` → do not install. Tell the user why (surface the `reasons` verbatim) and ask how they
  want to proceed. Never bypass a `BLOCK` on your own judgment.

## Batch-checking a manifest

If you're about to add several new packages to `requirements.txt`/`package.json`, scan each one:

```bash
for pkg in pkg1 pkg2==1.2.3 pkg3; do
  python3 scan_engine.py "${pkg%%==*}" "$(echo "$pkg" | grep -oP '(?<===).*' || true)"
done
```

## Related files in this skill directory

- `scan_engine.py` - the actual scan/scoring logic (stages 2-4 + 6 of the pipeline)
- `mcp_server.py` - the same logic exposed as an MCP-style tool (`scan_package(name, version)`)
- `hooks/pretooluse_check.py` - automatic Bash-command interception (see `SETTINGS_SNIPPET.json`)
- `SCORING.md` - why the weights/thresholds are what they are
- `INTERFACES.md` - stubs for the not-yet-implemented dynamic-sandbox and rollback stages
