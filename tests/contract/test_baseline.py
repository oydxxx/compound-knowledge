"""Protect the frozen 1.0.0 comparison fixture from accidental drift."""

from __future__ import annotations

import hashlib
from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BASELINE_ROOT = (
    REPOSITORY_ROOT / "tests/acceptance/baseline/original-v1.0.0"
)
SOURCE_ROOT = BASELINE_ROOT / "source"


class BaselineContractTests(unittest.TestCase):
    def test_snapshot_contains_required_original_components(self) -> None:
        required_paths = {
            ".claude-plugin/marketplace.json",
            "README.md",
            "PRIVACY.md",
            "SECURITY.md",
            "plugins/compound-knowledge/.claude-plugin/plugin.json",
            "plugins/compound-knowledge/LICENSE",
        }
        required_paths.update(
            f"plugins/compound-knowledge/skills/{name}/SKILL.md"
            for name in (
                "kw-brainstorm",
                "kw-plan",
                "kw-confidence",
                "kw-review",
                "kw-work",
                "kw-compound",
            )
        )
        required_paths.update(
            f"plugins/compound-knowledge/agents/{group}/{name}.md"
            for group, name in (
                ("research", "knowledge-base-researcher"),
                ("research", "past-work-researcher"),
                ("research", "stale-knowledge-checker"),
                ("review", "strategic-alignment-reviewer"),
                ("review", "data-accuracy-reviewer"),
            )
        )

        self.assertTrue(SOURCE_ROOT.is_dir(), "missing frozen source fixture")
        snapshot_paths = {
            path.relative_to(SOURCE_ROOT).as_posix()
            for path in SOURCE_ROOT.rglob("*")
            if path.is_file()
        }
        self.assertTrue(required_paths <= snapshot_paths)
        self.assertFalse(any(path.startswith("docs/plans/") for path in snapshot_paths))
        self.assertFalse(any(path.startswith("tests/") for path in snapshot_paths))

    def test_manifest_and_checksums_match_every_snapshot_file(self) -> None:
        manifest_path = BASELINE_ROOT / "source-manifest.txt"
        checksums_path = BASELINE_ROOT / "checksums.sha256"
        manifest_paths = manifest_path.read_text(encoding="utf-8").splitlines()
        snapshot_paths = sorted(
            path.relative_to(SOURCE_ROOT).as_posix()
            for path in SOURCE_ROOT.rglob("*")
            if path.is_file()
        )
        self.assertEqual(snapshot_paths, manifest_paths)

        recorded = {}
        for line in checksums_path.read_text(encoding="utf-8").splitlines():
            digest, path = line.split("  ", 1)
            recorded[path] = digest
        self.assertEqual(set(snapshot_paths), set(recorded))
        for relative_path in snapshot_paths:
            actual = hashlib.sha256(
                (SOURCE_ROOT / relative_path).read_bytes()
            ).hexdigest()
            self.assertEqual(recorded[relative_path], actual, relative_path)

    def test_behavior_inventory_and_entry_observation_are_present(self) -> None:
        inventory = (BASELINE_ROOT / "behavior-inventory.md").read_text(
            encoding="utf-8"
        )
        for skill in (
            "kw-brainstorm",
            "kw-plan",
            "kw-confidence",
            "kw-review",
            "kw-work",
            "kw-compound",
        ):
            self.assertIn(f"`{skill}`", inventory)
        observation = (BASELINE_ROOT / "claude-entry-observation.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("人工实测", observation)


if __name__ == "__main__":
    unittest.main()
