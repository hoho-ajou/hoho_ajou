"""
Agent Dependency Guard - T10: Skill/Hook self-integrity check.

Computes sha256 of the guard's own files and compares against a manifest.
The manifest is created automatically on first use (no "install step" - the
first time a PreToolUse(Bash) install checkpoint fires, if no manifest
exists yet, the current state is trusted and recorded as the baseline).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

GUARD_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = GUARD_DIR / "aasm_manifest.json"

# the files whose integrity matters: the hooks themselves, the scan/guard
# modules they import, and the Skill definition. If any of these is missing
# or changed, the guard may no longer behave as installed - per DESIGN.md
# T11's "fail-open" note, a broken file is as dangerous as a disabled hook.
PROTECTED_FILES = [
    "hooks/pretooluse_check.py",
    "hooks/pretooluse_editwrite_check.py",
    "scan_engine.py",
    "guard_paths.py",
    "mcp_guard.py",
    "integrity.py",
    "SKILL.md",
]


def _sha256(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _current_hashes() -> dict[str, str | None]:
    return {rel: _sha256(GUARD_DIR / rel) for rel in PROTECTED_FILES}


def check_integrity() -> list[str]:
    """Returns a list of human-readable mismatch descriptions (empty = clean).

    First call with no manifest present creates one from the current state
    (trust-on-first-use) and returns no findings - there's nothing to compare
    against yet, and flagging the very first checkpoint would just be noise.
    """
    current = _current_hashes()

    if not MANIFEST_PATH.exists():
        MANIFEST_PATH.write_text(json.dumps(current, indent=2, ensure_ascii=False))
        return []

    try:
        manifest = json.loads(MANIFEST_PATH.read_text())
    except (OSError, json.JSONDecodeError):
        # manifest itself is unreadable/corrupted - that's a finding too.
        MANIFEST_PATH.write_text(json.dumps(current, indent=2, ensure_ascii=False))
        return ["무결성 매니페스트 파일이 손상되어 있었음 (재생성함)"]

    findings = []
    for rel, expected in manifest.items():
        actual = current.get(rel)
        if actual is None and expected is not None:
            findings.append(f"{rel} 파일이 삭제됨")
        elif actual != expected:
            findings.append(f"{rel} 파일의 체크섬이 설치 시점과 다름 (변조 의심)")
    return findings
