"""Detect obvious English-only product prose in the six user-facing skills."""

from __future__ import annotations

from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPOSITORY_ROOT / "plugins/compound-knowledge/skills"
SKILL_NAMES = (
    "zs-boom", "zs-plan", "zs-confidence", "zs-review", "zs-work", "zs-compound",
)


class ChineseSurfaceTests(unittest.TestCase):
    def test_user_visible_headings_are_chinese(self) -> None:
        forbidden_headings = (
            "# Brainstorm", "# Plan", "# Confidence Check", "# Review", "# Work", "# Compound",
            "## When to Use", "## Process", "## Important Rules", "## Pipeline Mode",
        )
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                text = (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn("name: zs:", text)
                self.assertTrue(any("\u4e00" <= char <= "\u9fff" for char in text))
                for heading in forbidden_headings:
                    self.assertNotIn(heading, text)

    def test_claude_only_commands_are_not_the_core_interface(self) -> None:
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                text = (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertNotIn("/zs:", text)
                self.assertNotIn("CLAUDE.md", text)


if __name__ == "__main__":
    unittest.main()
