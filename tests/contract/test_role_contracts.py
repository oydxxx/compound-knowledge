"""Guard portable fixed-role contracts and their Claude projections."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPOSITORY_ROOT / "plugins/compound-knowledge"
SYNC_SCRIPT = REPOSITORY_ROOT / "tests/contract/sync_role_projections.py"

ROLE_SPECS = (
    (
        "knowledge-base-researcher",
        "skills/zs-plan/references/knowledge-base-researcher.md",
        "agents/research/knowledge-base-researcher.md",
        ("docs/knowledge/", "`tags`", "confidence:", "90 天", "correction"),
    ),
    (
        "past-work-researcher",
        "skills/zs-plan/references/past-work-researcher.md",
        "agents/research/past-work-researcher.md",
        ("`plans/`", "`docs/solutions/`", "3-5", "未解决"),
    ),
    (
        "stale-knowledge-checker",
        "skills/zs-compound/references/stale-knowledge-checker.md",
        "agents/research/stale-knowledge-checker.md",
        ("矛盾", "取代", "互补", "correction", "不得删除"),
    ),
    (
        "strategic-alignment-reviewer",
        "skills/zs-review/references/strategic-alignment-reviewer.md",
        "agents/review/strategic-alignment-reviewer.md",
        ("目标", "假设", "成功指标", "范围", "机会成本", "P1"),
    ),
    (
        "data-accuracy-reviewer",
        "skills/zs-review/references/data-accuracy-reviewer.md",
        "agents/review/data-accuracy-reviewer.md",
        ("来源", "比较基线", "48 小时", "7 天", "不得补充数据", "P1"),
    ),
)


class RoleContractTests(unittest.TestCase):
    def test_each_fixed_role_has_one_authoritative_contract(self) -> None:
        discovered = set()
        for role, contract_relative, _, required_terms in ROLE_SPECS:
            contract = PLUGIN_ROOT / contract_relative
            self.assertTrue(contract.is_file(), role)
            content = contract.read_text(encoding="utf-8")
            self.assertIn(f"name: {role}", content)
            self.assertIn("权威角色合同", content)
            self.assertIn("## 输入", content)
            self.assertIn("## 返回栏目", content)
            self.assertIn("只读", content)
            self.assertIn("不得创建、覆盖或发布", content)
            for term in required_terms:
                self.assertIn(term, content, f"{role}: {term}")
            discovered.add(contract.resolve())
        self.assertEqual(len(discovered), 5)

    def test_fixed_role_contracts_keep_the_execution_envelope(self) -> None:
        for role, contract_relative, _, _ in ROLE_SPECS:
            content = (PLUGIN_ROOT / contract_relative).read_text(encoding="utf-8")
            for term in (
                "稳定 ID",
                "输入与依赖",
                "只读来源",
                "`native`",
                "`fallback`",
                "状态",
                "来源证据",
                "错误",
                "补跑",
                "聚合结果",
            ):
                self.assertIn(term, content, f"{role}: {term}")

    def test_contract_references_are_only_one_level_deep(self) -> None:
        for role, contract_relative, wrapper_relative, _ in ROLE_SPECS:
            contract = (PLUGIN_ROOT / contract_relative).read_text(encoding="utf-8")
            wrapper = (PLUGIN_ROOT / wrapper_relative).read_text(encoding="utf-8")
            self.assertNotIn("](", contract, f"{role} contract must not chain references")
            self.assertNotIn("references/", contract)
            self.assertIn(f"source: {contract_relative}", wrapper)
            self.assertNotIn("](", wrapper, f"{role} wrapper must not add a second reference hop")

    def test_claude_projections_are_generated_and_synchronized(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SYNC_SCRIPT), "--check"],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_dynamic_tasks_keep_a_separate_write_boundary(self) -> None:
        content = (PLUGIN_ROOT / "docs/contracts/role-execution.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`zs-work`", content)
        self.assertIn("计划明确声明的交付路径", content)
        self.assertIn("不能借用角色权限合同扩大授权", content)


if __name__ == "__main__":
    unittest.main()
