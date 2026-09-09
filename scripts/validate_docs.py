#!/usr/bin/env python3
"""Validate AASM docs consistency: schema examples + internal markdown links + epic sections.

Run: python3 scripts/validate_docs.py
"""
import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("jsonschema not installed: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def check_sample_dataset_against_schemas() -> None:
    path = ROOT / "docs/contracts/sample_dataset.md"
    content = path.read_text()
    blocks = re.findall(r"```json\n(.*?)\n```", content, re.S)
    schema_files = [
        "schemas/collector_output.schema.json",
        "schemas/risk_score.schema.json",
        "schemas/ml_result.schema.json",
        "schemas/attack_graph.schema.json",
    ]
    if len(blocks) != len(schema_files):
        errors.append(
            f"sample_dataset.md: expected {len(schema_files)} json blocks, found {len(blocks)}"
        )
        return
    for block, schema_path in zip(blocks, schema_files):
        schema = json.loads((ROOT / schema_path).read_text())
        data = json.loads(block)
        try:
            jsonschema.validate(data, schema)
        except jsonschema.ValidationError as e:
            errors.append(f"sample_dataset.md vs {schema_path}: {e.message} at {list(e.path)}")


def check_internal_links() -> None:
    md_files = list(ROOT.glob("**/*.md"))
    md_files = [f for f in md_files if ".git" not in f.parts]
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for f in md_files:
        content = f.read_text(errors="ignore")
        for link in link_re.findall(content):
            if link.startswith(("http://", "https://", "#")):
                continue
            target = link.split("#")[0]
            if not target:
                continue
            resolved = (f.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{f.relative_to(ROOT)}: broken link -> {link}")


def check_epic_sections() -> None:
    required = ["## 목표", "## 범위", "## 완료조건", "## 참고 자료", "## 담당 문서", "## 하위 이슈"]
    for d in ["docs/epics", "docs/roles"]:
        for f in sorted((ROOT / d).glob("*.md")):
            content = f.read_text()
            for section in required:
                if section not in content:
                    errors.append(f"{f.relative_to(ROOT)}: missing section '{section}'")


def main() -> int:
    check_sample_dataset_against_schemas()
    check_internal_links()
    check_epic_sections()
    if errors:
        print(f"{len(errors)} problem(s) found:\n")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
