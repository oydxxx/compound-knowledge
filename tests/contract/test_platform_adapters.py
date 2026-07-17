"""Contract checks for thin, lifecycle-safe platform adapters."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins/compound-knowledge"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
SKILLS = (
    "zs-boom",
    "zs-plan",
    "zs-confidence",
    "zs-review",
    "zs-work",
    "zs-compound",
)
COMMANDS = tuple(name.removeprefix("zs-") for name in SKILLS)


class PlatformAdapterTests(unittest.TestCase):
    def read(self, relative: str) -> str:
        return (PLUGIN_ROOT / relative).read_text(encoding="utf-8")

    def test_claude_legacy_wrappers_forward_to_the_canonical_skills(self) -> None:
        for canonical_name, command in zip(SKILLS, COMMANDS):
            with self.subTest(command=command):
                for relative in (
                    f"commands/zs/{command}.md",
                    f"adapters/claude-code/commands/zs:{command}.md",
                ):
                    content = self.read(relative)
                    self.assertIn(f"/zs:{command}", content)
                    self.assertIn(canonical_name, content)
                    self.assertIn("$ARGUMENTS", content)
                    self.assertNotIn("#$ARGUMENTS", content)
                    self.assertIn("SKILL.md", content)
                    self.assertLess(len(content), 1800, relative)
                    self.assertNotIn("# 流程", content, relative)

    def test_codex_metadata_preserves_canonical_names_and_uses_chinese_ui(self) -> None:
        for skill in SKILLS:
            with self.subTest(skill=skill):
                content = (SKILLS_ROOT / skill / "agents/openai.yaml").read_text(
                    encoding="utf-8"
                )
                self.assertRegex(content, r"(?m)^interface:$")
                self.assertRegex(content, r"(?m)^  display_name: .*[\u4e00-\u9fff]")
                self.assertRegex(content, r"(?m)^  short_description: .*[\u4e00-\u9fff]")
                self.assertIn(f"${skill}", content)
                self.assertIn("allow_implicit_invocation", content)

    def test_platform_documentation_covers_install_lifecycle_and_safety(self) -> None:
        documents = (
            "adapters/README.md",
            "adapters/claude-code/README.md",
            "adapters/codex/README.md",
            "adapters/workbuddy/README.md",
            "adapters/trae-solo/README.md",
        )
        for relative in documents:
            with self.subTest(document=relative):
                content = self.read(relative)
                for required in (
                    "安装",
                    "全新会话",
                    "缓存",
                    "更新",
                    "卸载",
                    "trusted_pipeline_signal",
                    "fallback",
                    "消费方",
                ):
                    self.assertIn(required, content)

        claude = self.read("adapters/claude-code/README.md")
        for required in ("已验证", "冲突", "重复", ".claude/commands/zs:"):
            self.assertIn(required, claude)
        self.assertIn("不提供裸", claude)

        codex = self.read("adapters/codex/README.md")
        self.assertIn(".agents/skills", codex)
        self.assertIn("openai.yaml", codex)
        trae = self.read("adapters/trae-solo/README.md")
        self.assertIn(".agents/skills", trae)
        workbuddy = self.read("adapters/workbuddy/README.md")
        for required in ("确定性", "manifest", "LICENSE", "SHA-256", "归档"):
            self.assertIn(required, workbuddy)

    def test_workbuddy_manifest_has_one_canonical_skill_hash(self) -> None:
        manifest = self.read("adapters/workbuddy/manifest.sha256")
        actual = {}
        for skill in SKILLS:
            source = SKILLS_ROOT / skill / "SKILL.md"
            actual[f"skills/{skill}/SKILL.md"] = hashlib.sha256(
                source.read_bytes()
            ).hexdigest()
        recorded = {}
        for line in manifest.strip().splitlines():
            digest, path = line.split("  ", maxsplit=1)
            recorded[path] = digest
        for skill in SKILLS:
            self.assertRegex(
                manifest,
                rf"(?m)^[0-9a-f]{{64}}  skills/{re.escape(skill)}/SKILL\.md$",
            )
        self.assertEqual(len(manifest.strip().splitlines()), len(SKILLS))
        self.assertEqual(recorded, actual)

    def test_smoke_checklist_requires_real_evidence_not_static_claims(self) -> None:
        content = (
            REPOSITORY_ROOT / "tests/acceptance/templates/platform-smoke-checklist.md"
        ).read_text(encoding="utf-8")
        for platform in ("Claude Code", "Codex", "WorkBuddy", "TRAE SOLO"):
            self.assertIn(platform, content)
        for required in (
            "截图或文本证据",
            "全新会话",
            "trusted_pipeline_signal",
            "伪造参数",
            "伪造项目文件",
            "人工确认",
            "不得以静态合同替代",
        ):
            self.assertIn(required, content)


if __name__ == "__main__":
    unittest.main()
