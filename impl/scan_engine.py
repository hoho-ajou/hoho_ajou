"""
Agent Dependency Guard - core scan engine (MVP)

Implements pipeline stages 2~4 (+ rule-based stage 6):
  2. Fetch  - download wheel/sdist WITHOUT running install scripts
  3. Static analysis - entropy, dangerous keywords, install hooks, typosquat distance
  4. Vulnerability lookup - OSV.dev
  6. Verdict - weighted rule-based scoring -> ALLOW / NEEDS_HUMAN_REVIEW / BLOCK

Stage 5 (dynamic sandbox observation) and stage 7 (rollback) are NOT implemented here;
see INTERFACES.md for their stub signatures.
"""
from __future__ import annotations

import base64
import io
import json
import math
import re
import tarfile
import tempfile
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PYPI_JSON_URL = "https://pypi.org/pypi/{name}/json"
OSV_QUERY_URL = "https://api.osv.dev/v1/query"

# small embedded sample of popular package names for a lightweight typosquat check.
# production should replace this with the real top-N list (e.g. hugovk/top-pypi-packages).
POPULAR_PACKAGES = [
    "requests", "urllib3", "numpy", "pandas", "boto3", "pyyaml", "setuptools",
    "python-dateutil", "certifi", "idna", "charset-normalizer", "six",
    "click", "flask", "django", "pytest", "cryptography", "pillow",
    "protobuf", "grpcio", "aiohttp", "jinja2", "markupsafe", "attrs",
    "packaging", "wheel", "pip", "typing-extensions", "colorama", "chardet",
]

DANGEROUS_KEYWORDS = [
    "eval(", "exec(", "os.system(", "subprocess.", "pickle.loads(",
    "base64.b64decode(", "socket.socket(", "urllib.request.urlopen(",
    "__import__(", "compile(", "marshal.loads(",
]

# builtins whose bare form is the risky one (e.g. dynamic bytecode compile()) -
# but which also appear constantly as a harmless attribute (re.compile(),
# obj.exec(), pandas df.eval()). Require them NOT to be preceded by `.` so we
# don't flag the attribute-access form. Found via real false positive: requests
# 2.31.0 got BLOCKed because `re.compile(...)` substring-matched `compile(`.
_BARE_BUILTIN_KEYWORDS = {"eval(", "exec(", "compile(", "__import__("}


def _compile_keyword_pattern(kw: str) -> re.Pattern:
    if kw in _BARE_BUILTIN_KEYWORDS:
        return re.compile(r"(?<![\w.])" + re.escape(kw))
    return re.compile(re.escape(kw))


_KEYWORD_PATTERNS = {kw: _compile_keyword_pattern(kw) for kw in DANGEROUS_KEYWORDS}

# a package's own test suite legitimately exercises "dangerous" APIs (mocking
# sockets, testing pickle round-trips) - that code never runs for a consumer
# who just installs the package, so it shouldn't count as a risk signal.
# Found via the same requests false positive: 15 of 27 keyword hits were in
# tests/test_requests.py and tests/testserver/server.py.
_TEST_PATH_PATTERN = re.compile(r"(^|[\\/])tests?([\\/]|$)|(^|[\\/])(test_\w+|\w+_test)\.py$")


def _is_test_path(path: Path) -> bool:
    return bool(_TEST_PATH_PATTERN.search(str(path)))


INSTALL_HOOK_PATTERNS = [
    re.compile(r"cmdclass\s*=", re.IGNORECASE),
    re.compile(r"class\s+\w*install\w*\(", re.IGNORECASE),
    re.compile(r"run\(self\)"),
]

# chain-signal hard rules (4-1 in DESIGN.md: structural "A call near B call"
# patterns are deterministic, not ML territory). Verified against two real
# malware samples this session: pingdomv3 1.1.0 (decode_then_exec) and
# ultralytics/XMRig injection (download_then_execute). N=8 lines is a starting
# point, not derived from those samples' exact distance - tune empirically.
CHAIN_LINE_WINDOW = 8

_DECODE_PATTERNS = [re.compile(re.escape(kw)) for kw in ("base64.b64decode(", "marshal.loads(")]
_EXEC_PATTERNS = [re.compile(r"(?<![\w.])(eval|exec)\(")]
_DOWNLOAD_PATTERNS = [re.compile(re.escape(kw)) for kw in
                      ("urllib.request.urlopen(", "requests.get(", "requests.post(", "urlretrieve(")]
_EXECUTE_PATTERNS = [re.compile(re.escape(kw)) for kw in
                     ("subprocess.", "os.system(", "os.popen(", "Popen(")]


def _line_numbers_matching(lines: list[str], patterns: list[re.Pattern]) -> list[int]:
    hits = []
    for i, line in enumerate(lines):
        if any(p.search(line) for p in patterns):
            hits.append(i)
    return hits


def _has_chain(text: str, group_a: list[re.Pattern], group_b: list[re.Pattern], window: int) -> bool:
    lines = text.splitlines()
    a_lines = _line_numbers_matching(lines, group_a)
    if not a_lines:
        return False
    b_lines = _line_numbers_matching(lines, group_b)
    if not b_lines:
        return False
    return any(abs(a - b) <= window for a in a_lines for b in b_lines)


@dataclass
class ScanFeatures:
    name: str
    version: str | None
    resolved_version: str | None = None
    fetch_ok: bool = False
    fetch_error: str | None = None

    max_entropy: float = 0.0
    keyword_hits: dict = field(default_factory=dict)
    keyword_total: int = 0
    has_install_hook: bool = False
    has_decode_then_exec: bool = False
    has_download_then_execute: bool = False
    file_count: int = 0
    py_file_count: int = 0

    min_edit_distance: int | None = None
    closest_popular_name: str | None = None

    osv_vulns: list = field(default_factory=list)
    osv_max_severity: str | None = None

    maintainer_count: int | None = None
    package_age_days: float | None = None
    has_readme: bool = False


@dataclass
class Verdict:
    verdict: str  # ALLOW | NEEDS_HUMAN_REVIEW | BLOCK
    score: float
    reasons: list
    features: ScanFeatures


def _levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def _shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    n = len(data)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


def fetch_pypi_metadata(name: str) -> dict:
    with urllib.request.urlopen(PYPI_JSON_URL.format(name=name), timeout=15) as resp:
        return json.loads(resp.read())


def fetch_distribution_without_install(name: str, version: str | None, dest_dir: Path) -> tuple[str | None, list[Path]]:
    """Download the sdist/wheel file(s) for a release, unpack them, but never execute
    setup.py or any install script. Returns (resolved_version, list_of_extracted_file_paths)."""
    meta = fetch_pypi_metadata(name)
    releases = meta.get("releases", {})
    resolved = version or meta.get("info", {}).get("version")
    if resolved not in releases or not releases[resolved]:
        return resolved, []

    # A release can ship many platform-specific wheels (manylinux/macos/windows x
    # several Python versions) on top of the sdist. Downloading & extracting all of
    # them wastes time for zero extra signal - one representative build is enough
    # for static analysis. Prefer: sdist > pure-python wheel (py3-none-any) > first
    # available file.
    candidates = releases[resolved]
    sdist = next((f for f in candidates if f.get("packagetype") == "sdist"), None)
    pure_wheel = next((f for f in candidates if f["filename"].endswith("-none-any.whl")), None)
    chosen = sdist or pure_wheel or candidates[0]

    extracted: list[Path] = []
    for file_info in [chosen]:
        url = file_info["url"]
        filename = file_info["filename"]
        with urllib.request.urlopen(url, timeout=30) as resp:
            raw = resp.read()
        local_path = dest_dir / filename
        local_path.write_bytes(raw)

        if filename.endswith(".whl") or filename.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                zf.extractall(dest_dir / (filename + ".unpacked"))
                extracted.extend((dest_dir / (filename + ".unpacked")).rglob("*"))
        elif filename.endswith((".tar.gz", ".tgz")):
            with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
                safe_members = [m for m in tf.getmembers() if not m.name.startswith("/") and ".." not in m.name]
                tf.extractall(dest_dir / (filename + ".unpacked"), members=safe_members)
                extracted.extend((dest_dir / (filename + ".unpacked")).rglob("*"))
    return resolved, extracted


def static_analysis(files: list[Path], features: ScanFeatures) -> None:
    keyword_hits: dict[str, int] = {}
    max_entropy = 0.0
    py_count = 0
    total_count = 0

    decode_then_exec = False
    download_then_execute = False

    for path in files:
        if not path.is_file():
            continue
        total_count += 1
        if path.suffix == ".py":
            py_count += 1
            is_test = _is_test_path(path)
            try:
                text = path.read_text(errors="ignore")
            except Exception:
                continue

            # keyword/entropy/chain signals only reflect code a consumer of the
            # package would actually run - not the package's own test suite.
            if not is_test:
                for kw, pat in _KEYWORD_PATTERNS.items():
                    n = len(pat.findall(text))
                    if n:
                        keyword_hits[kw] = keyword_hits.get(kw, 0) + n

                if _has_chain(text, _DECODE_PATTERNS, _EXEC_PATTERNS, CHAIN_LINE_WINDOW):
                    decode_then_exec = True
                if _has_chain(text, _DOWNLOAD_PATTERNS, _EXECUTE_PATTERNS, CHAIN_LINE_WINDOW):
                    download_then_execute = True

                for block in re.findall(r"[A-Za-z0-9+/=]{80,}", text):
                    try:
                        decoded = base64.b64decode(block, validate=True)
                        e = _shannon_entropy(decoded)
                    except Exception:
                        e = _shannon_entropy(block.encode())
                    max_entropy = max(max_entropy, e)

            for pat in INSTALL_HOOK_PATTERNS:
                if pat.search(text) and path.name in ("setup.py",):
                    features.has_install_hook = True

        if path.name.lower() == "readme" or path.name.lower().startswith("readme."):
            features.has_readme = True

    features.file_count = total_count
    features.py_file_count = py_count
    features.keyword_hits = keyword_hits
    features.keyword_total = sum(keyword_hits.values())
    features.max_entropy = round(max_entropy, 3)
    features.has_decode_then_exec = decode_then_exec
    features.has_download_then_execute = download_then_execute


def typosquat_check(name: str, features: ScanFeatures) -> None:
    best = None
    best_dist = None
    for pop in POPULAR_PACKAGES:
        d = _levenshtein(name.lower(), pop.lower())
        if best_dist is None or d < best_dist:
            best_dist = d
            best = pop
    features.min_edit_distance = best_dist
    features.closest_popular_name = best


def query_osv(name: str, version: str | None) -> list[dict]:
    payload: dict[str, Any] = {"package": {"name": name, "ecosystem": "PyPI"}}
    if version:
        payload["version"] = version
    req = urllib.request.Request(
        OSV_QUERY_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        return data.get("vulns", [])
    except Exception:
        return []


def _severity_rank(vulns: list[dict]) -> str | None:
    # OSV's severity[].score is usually a bare CVSS vector string
    # ("CVSS:3.1/AV:N/...") with no literal "CRITICAL"/"HIGH" word in it, so a
    # substring search against it never matches. The actual human-readable
    # rating lives in database_specific.severity for GHSA-sourced advisories -
    # verified directly against OSV's real response for pyyaml 5.3.1
    # (CVE-2020-14343, a real CRITICAL RCE our CRITICAL hard-rule was silently
    # never catching because of this bug).
    order = {"CRITICAL": 3, "HIGH": 2, "MODERATE": 1, "LOW": 0}
    worst = None
    for v in vulns:
        candidates = []
        db_sev = v.get("database_specific", {}).get("severity")
        if db_sev:
            candidates.append(str(db_sev).upper())
        for sev in v.get("severity", []):
            candidates.append(str(sev.get("score", "")).upper())
        for s in candidates:
            for key in order:
                if key in s:
                    if worst is None or order[key] > order[worst]:
                        worst = key
    return worst


# ---------------- scoring weights (draft, see SCORING.md for rationale) ----------------
WEIGHTS = {
    "vuln": 0.30,
    "entropy": 0.15,
    "keyword": 0.15,
    "install_hook": 0.15,
    "typosquat": 0.15,
    "reputation": 0.10,
}

BLOCK_THRESHOLD = 0.6
REVIEW_THRESHOLD = 0.25


def compute_verdict(features: ScanFeatures) -> Verdict:
    reasons = []
    sub_scores = {}

    sub_scores["vuln"] = 1.0 if features.osv_vulns else 0.0
    if features.osv_vulns:
        reasons.append(f"OSV 취약점 {len(features.osv_vulns)}건 발견 (최고 심각도: {features.osv_max_severity})")

    sub_scores["entropy"] = min(1.0, features.max_entropy / 6.0)
    if features.max_entropy > 4.5:
        reasons.append(f"높은 엔트로피 블록 발견 (max_entropy={features.max_entropy})")

    # denominator scales with package size (py_file_count) so a handful of
    # legitimate keyword hits in a large codebase doesn't dilute to zero risk
    # for tiny packages, nor get a big codebase unfairly flagged for its sheer
    # size. Found via real false positive: requests (33 .py files) scored the
    # same fixed-denominator risk as a 1-file malicious package would for the
    # same raw count. Floor of 3 avoids a single-file package dividing by ~1.
    keyword_denominator = max(3, features.py_file_count * 2)
    sub_scores["keyword"] = min(1.0, features.keyword_total / keyword_denominator)
    if features.keyword_total > 0:
        reasons.append(f"위험 키워드 {features.keyword_total}회 검출(분모={keyword_denominator}): {features.keyword_hits}")

    sub_scores["install_hook"] = 1.0 if features.has_install_hook else 0.0
    if features.has_install_hook:
        reasons.append("setup.py에 커스텀 install hook 존재")

    if features.min_edit_distance is not None and features.min_edit_distance <= 2 and features.min_edit_distance > 0:
        sub_scores["typosquat"] = 1.0
        reasons.append(f"인기 패키지 '{features.closest_popular_name}'와 편집거리 {features.min_edit_distance} (타이포스쿼팅 의심)")
    else:
        sub_scores["typosquat"] = 0.0

    reputation_risk = 0.0
    if features.package_age_days is not None and features.package_age_days < 30:
        reputation_risk += 0.5
        reasons.append(f"최근 등록된 패키지 (age={features.package_age_days:.0f}일)")
    if not features.has_readme:
        reputation_risk += 0.3
    if features.maintainer_count == 0:
        reputation_risk += 0.2
    sub_scores["reputation"] = min(1.0, reputation_risk)

    total = sum(WEIGHTS[k] * sub_scores[k] for k in WEIGHTS)

    # hard overrides (chain-signal style rules from earlier feature design)
    if features.osv_max_severity == "CRITICAL":
        return Verdict("BLOCK", round(total, 3), reasons + ["[하드룰] CRITICAL 취약점 → 무조건 BLOCK"], features)

    if features.has_decode_then_exec:
        return Verdict("BLOCK", round(max(total, BLOCK_THRESHOLD), 3),
                        reasons + [f"[하드룰] decode_then_exec 체인 탐지 (디코드 호출 {CHAIN_LINE_WINDOW}줄 이내 exec/eval) → 무조건 BLOCK"],
                        features)

    if features.has_download_then_execute:
        return Verdict("BLOCK", round(max(total, BLOCK_THRESHOLD), 3),
                        reasons + [f"[하드룰] download_then_execute 체인 탐지 (다운로드 호출 {CHAIN_LINE_WINDOW}줄 이내 실행 호출) → 무조건 BLOCK"],
                        features)

    if features.has_install_hook and sub_scores["keyword"] > 0:
        total = max(total, REVIEW_THRESHOLD + 0.01)
        reasons.append("[하드룰] install hook + 위험 키워드 동시 존재 → 최소 리뷰 필요")

    if total >= BLOCK_THRESHOLD:
        verdict = "BLOCK"
    elif total >= REVIEW_THRESHOLD:
        verdict = "NEEDS_HUMAN_REVIEW"
    else:
        verdict = "ALLOW"

    return Verdict(verdict, round(total, 3), reasons, features)


def scan_package(name: str, version: str | None = None) -> Verdict:
    features = ScanFeatures(name=name, version=version)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            resolved, files = fetch_distribution_without_install(name, version, tmp_path)
            features.resolved_version = resolved
            features.fetch_ok = True
            static_analysis(files, features)
    except Exception as e:
        features.fetch_error = str(e)
        reasons = [f"fetch/분석 실패: {e}"]
        return Verdict("NEEDS_HUMAN_REVIEW", 0.5, reasons, features)

    typosquat_check(name, features)

    try:
        meta = fetch_pypi_metadata(name)
        info = meta.get("info", {})
        features.maintainer_count = 1 if info.get("maintainer") or info.get("author") else 0
        features.has_readme = features.has_readme or bool(info.get("description"))

        releases = meta.get("releases", {})
        upload_times = [
            f["upload_time_iso_8601"]
            for files in releases.values()
            for f in files
            if f.get("upload_time_iso_8601")
        ]
        if upload_times:
            from datetime import datetime, timezone
            earliest = min(datetime.fromisoformat(t.replace("Z", "+00:00")) for t in upload_times)
            features.package_age_days = (datetime.now(timezone.utc) - earliest).total_seconds() / 86400
    except Exception:
        pass

    features.osv_vulns = query_osv(name, features.resolved_version)
    features.osv_max_severity = _severity_rank(features.osv_vulns)

    return compute_verdict(features)


if __name__ == "__main__":
    import sys

    pkg = sys.argv[1] if len(sys.argv) > 1 else "requests"
    ver = sys.argv[2] if len(sys.argv) > 2 else None
    result = scan_package(pkg, ver)
    print(json.dumps({
        "verdict": result.verdict,
        "score": result.score,
        "reasons": result.reasons,
    }, ensure_ascii=False, indent=2))
