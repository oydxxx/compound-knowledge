"""Contract checks for the Chinese distribution and maintenance surface."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins/compound-knowledge"
VERSION = "3.1.0"
LICENSE_DIGEST = "5e6b8e5eb65e330d1222707bec87584d57ec48f61daa92a590d98f88ac3c04e3"


class DistributionDocumentationTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")

    def test_versions_are_synchronized_in_all_distribution_manifests(self) -> None:
        marketplace = json.loads(self.read(".claude-plugin/marketplace.json"))
        plugin = json.loads(
            self.read("plugins/compound-knowledge/.claude-plugin/plugin.json")
        )
        changelog = self.read("plugins/compound-knowledge/CHANGELOG.md")

        self.assertEqual(marketplace["metadata"]["version"], VERSION)
        self.assertEqual(marketplace["plugins"][0]["version"], VERSION)
        self.assertEqual(plugin["version"], VERSION)
        self.assertIn(f"## [{VERSION}]", changelog)
        self.assertRegex(marketplace["metadata"]["description"], r"[\u4e00-\u9fff]")
        self.assertRegex(marketplace["plugins"][0]["description"], r"[\u4e00-\u9fff]")
        self.assertRegex(plugin["description"], r"[\u4e00-\u9fff]")

    def test_readmes_cover_four_platform_lifecycles_and_chinese_invocation(self) -> None:
        root_readme = self.read("README.md")
        plugin_readme = self.read("plugins/compound-knowledge/README.md")

        for content in (root_readme, plugin_readme):
            for platform in ("Claude Code", "Codex", "WorkBuddy", "TRAE SOLO"):
                self.assertIn(platform, content)
            for required in ("安装", "更新", "卸载", "中文自然语言"):
                self.assertIn(required, content)
            self.assertRegex(content, r"请[帮为]我.*(?:规划|梳理|复盘|制定)")

        self.assertIn("plugins/compound-knowledge/adapters/", root_readme)
        self.assertIn("adapters/", plugin_readme)
        self.assert_markdown_links_resolve(root_readme, REPOSITORY_ROOT / "README.md")
        self.assert_markdown_links_resolve(plugin_readme, PLUGIN_ROOT / "README.md")

    def test_privacy_and_security_documents_state_the_same_precise_boundaries(self) -> None:
        for relative in (
            "PRIVACY.md",
            "SECURITY.md",
            "plugins/compound-knowledge/PRIVACY.md",
            "plugins/compound-knowledge/SECURITY.md",
        ):
            content = self.read(relative)
            with self.subTest(document=relative):
                for required in (
                    "不收集遥测",
                    "不要求联网",
                    "本地优先",
                    "宿主平台",
                    "模型调用",
                    "不等同于本技能主动联网",
                    "人工授权",
                ):
                    self.assertIn(required, content)

    def test_changelog_records_names_legacy_entry_and_evidence_caveat(self) -> None:
        changelog = self.read("plugins/compound-knowledge/CHANGELOG.md")
        for required in (
            "zs-*",
            "/zs:*",
            "Claude Code",
            "Codex",
            "WorkBuddy",
            "TRAE SOLO",
            "真实",
            "静态",
            "证据",
        ):
            self.assertIn(required, changelog)

    def test_license_is_byte_for_byte_identical_to_the_frozen_baseline(self) -> None:
        license_path = PLUGIN_ROOT / "LICENSE"
        baseline = (
            REPOSITORY_ROOT
            / "tests/acceptance/baseline/original-v1.0.0/checksums.sha256"
        ).read_text(encoding="utf-8")
        recorded = {
            path: digest
            for digest, path in (
                line.split("  ", 1) for line in baseline.splitlines()
            )
        }
        self.assertEqual(recorded["plugins/compound-knowledge/LICENSE"], LICENSE_DIGEST)
        self.assertEqual(hashlib.sha256(license_path.read_bytes()).hexdigest(), LICENSE_DIGEST)

    def test_claude_file_remains_a_thin_agents_shim(self) -> None:
        shim = self.read("plugins/compound-knowledge/CLAUDE.md").strip()
        self.assertLessEqual(len(shim), 100)
        self.assertIn("AGENTS.md", shim)
        self.assertNotIn("Plugin Structure", shim)

    def assert_markdown_links_resolve(self, content: str, source: Path) -> None:
        for target in re.findall(r"(?<!!)\[[^]]+\]\(([^)]+)\)", content):
            target = target.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            self.assertTrue((source.parent / target).exists(), f"broken link: {target}")


if __name__ == "__main__":
    unittest.main()
