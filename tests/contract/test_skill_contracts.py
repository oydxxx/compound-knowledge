"""Contract checks for the six portable Compound Knowledge skills."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPOSITORY_ROOT / "plugins/compound-knowledge/skills"
SKILLS = {
    "zs-boom": ("[topic, brain dump, or meeting notes]", "brain_dump"),
    "zs-plan": ("[what to plan]", "plan_request"),
    "zs-confidence": (None, None),
    "zs-review": ("[file path or content to review]", "review_target"),
    "zs-work": ("[plan file to execute]", "work_target"),
    "zs-compound": (None, None),
}


class SkillContractTests(unittest.TestCase):
    def skill_text(self, name: str) -> str:
        return (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")

    def test_standard_names_and_frontmatter_are_portable(self) -> None:
        for name, (argument_hint, _) in SKILLS.items():
            with self.subTest(skill=name):
                path = SKILLS_ROOT / name / "SKILL.md"
                text = self.skill_text(name)
                self.assertEqual(path.parent.name, name)
                self.assertRegex(text, rf"(?m)^name: {re.escape(name)}$")
                self.assertRegex(text, r"(?m)^description: .*[\u4e00-\u9fff]")
                if argument_hint is None:
                    self.assertNotIn("argument-hint:", text)
                else:
                    self.assertIn(f"argument-hint: \"{argument_hint}\"", text)

    def test_argument_wrappers_and_stable_protocols_survive(self) -> None:
        for name, (_, wrapper) in SKILLS.items():
            with self.subTest(skill=name):
                text = self.skill_text(name)
                if wrapper:
                    self.assertIn(f"<{wrapper}>$ARGUMENTS</{wrapper}>", text)
                    self.assertNotIn(f"<{wrapper}> #$ARGUMENTS </{wrapper}>", text)
        for name in ("zs-boom", "zs-plan", "zs-confidence", "zs-work"):
            self.assertIn("plans/", self.skill_text(name))
        confidence = self.skill_text("zs-confidence")
        for forbidden in ("百分比", "1–10", "字母等级"):
            self.assertIn(forbidden, confidence)
        self.assertIn("docs/knowledge/", self.skill_text("zs-compound"))

    def test_each_skill_is_independently_safe_without_central_contracts(self) -> None:
        for name in SKILLS:
            with self.subTest(skill=name):
                text = self.skill_text(name)
                for required in ("普通中文对话", "等待回答", "阻塞", "人工授权"):
                    self.assertIn(required, text)
                self.assertIn("trusted_pipeline_signal", text)
                self.assertIn("fallback", text)
                self.assertNotRegex(text, r"AskUserQuestion|Launch Task agent|disable-model-invocation")

    def test_baseline_xml_wrappers_are_preserved(self) -> None:
        expected = {
            "zs-boom": ("parallel_tasks", "critical_requirement"),
            "zs-plan": ("parallel_tasks",),
            "zs-review": ("parallel_tasks",),
            "zs-work": ("critical_requirement",),
            "zs-compound": ("critical_requirement",),
        }
        for name, wrappers in expected.items():
            with self.subTest(skill=name):
                text = self.skill_text(name)
                for wrapper in wrappers:
                    self.assertIn(f"<{wrapper}>", text)
                    self.assertIn(f"</{wrapper}>", text)

    def test_workflow_specific_artifacts_and_defaults_remain(self) -> None:
        expected = {
            "zs-boom": "plans/brainstorm-{descriptive-name}.md",
            "zs-plan": "plans/{type}-{descriptive-name}.md",
            "zs-confidence": "plans/confidence-{date}.md",
            "zs-review": "P1",
            "zs-work": "## Execution Log",
            "zs-compound": "docs/knowledge/{descriptive-slug}.md",
        }
        for name, token in expected.items():
            with self.subTest(skill=name):
                self.assertIn(token, self.skill_text(name))

    def test_boom_preserves_the_full_brainstorming_contract(self) -> None:
        """Prevent a short localization from silently deleting workflow stages."""
        boom = self.skill_text("zs-boom")
        required = (
            "## 我听到的内容",
            "## 主题、张力与缺口",
            "### 主题",
            "### 张力",
            "### 缺口",
            "承重问题",
            "一次只提出 1–3 个问题",
            "已有候选时不要退化成开放式追问",
            "这是衔接步骤，不是需求访谈",
            "基于目前信息，核心问题是",
            "头脑梳理已完成，接下来做什么？",
            "进入 `zs-plan`",
            "继续深挖",
            "征求反馈",
            "保存后继续",
            "继续补充",
            "在提出任何问题之前，必须完整输出以下三个小节",
            "若 `<brain_dump>` 非空",
            "同一轮回复",
            "不得因“先确认”而停止在第 1 步",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, boom)


if __name__ == "__main__":
    unittest.main()
