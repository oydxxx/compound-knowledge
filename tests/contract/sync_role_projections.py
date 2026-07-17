#!/usr/bin/env python3
"""Generate and verify Claude Code role projections from authoritative contracts."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins/compound-knowledge"

ROLE_PROJECTIONS = (
    (
        "knowledge-base-researcher",
        "skills/zs-plan/references/knowledge-base-researcher.md",
        "agents/research/knowledge-base-researcher.md",
    ),
    (
        "past-work-researcher",
        "skills/zs-plan/references/past-work-researcher.md",
        "agents/research/past-work-researcher.md",
    ),
    (
        "stale-knowledge-checker",
        "skills/zs-compound/references/stale-knowledge-checker.md",
        "agents/research/stale-knowledge-checker.md",
    ),
    (
        "strategic-alignment-reviewer",
        "skills/zs-review/references/strategic-alignment-reviewer.md",
        "agents/review/strategic-alignment-reviewer.md",
    ),
    (
        "data-accuracy-reviewer",
        "skills/zs-review/references/data-accuracy-reviewer.md",
        "agents/review/data-accuracy-reviewer.md",
    ),
)


def contract_body(content: str) -> str:
    """Remove a contract's YAML metadata while retaining its full behavior."""
    if not content.startswith("---\n"):
        raise ValueError("role contract must start with YAML frontmatter")
    _, separator, body = content[4:].partition("\n---\n")
    if not separator:
        raise ValueError("role contract frontmatter is not closed")
    return body.lstrip("\n")


def render_projection(role: str, source_relative: str) -> str:
    source = PLUGIN_ROOT / source_relative
    source_bytes = source.read_bytes()
    source_content = source_bytes.decode("utf-8")
    checksum = hashlib.sha256(source_bytes).hexdigest()
    return (
        "---\n"
        f"name: {role}\n"
        "description: \"由权威角色合同生成的 Claude Code 只读角色投影。\"\n"
        "model: inherit\n"
        f"source: {source_relative}\n"
        f"source_sha256: {checksum}\n"
        "projection: generated\n"
        "---\n\n"
        "<!-- 由 tests/contract/sync_role_projections.py 生成；请修改 source 指向的权威角色合同。 -->\n\n"
        + contract_body(source_content)
    )


def synchronize(write: bool) -> int:
    mismatches = []
    for role, source_relative, wrapper_relative in ROLE_PROJECTIONS:
        wrapper = PLUGIN_ROOT / wrapper_relative
        expected = render_projection(role, source_relative)
        actual = wrapper.read_text(encoding="utf-8") if wrapper.exists() else ""
        if actual != expected:
            mismatches.append(wrapper_relative)
            if write:
                wrapper.parent.mkdir(parents=True, exist_ok=True)
                wrapper.write_text(expected, encoding="utf-8")

    if mismatches and not write:
        print("Claude role projections are out of sync:", file=sys.stderr)
        for path in mismatches:
            print(f"- {path}", file=sys.stderr)
        print("Run: python3 tests/contract/sync_role_projections.py --write", file=sys.stderr)
        return 1
    if mismatches:
        print(f"Synchronized {len(mismatches)} Claude role projection(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--write", action="store_true", help="rewrite stale Claude projections"
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="fail when a Claude projection differs from its source contract",
    )
    args = parser.parse_args()
    return synchronize(write=args.write)


if __name__ == "__main__":
    raise SystemExit(main())
