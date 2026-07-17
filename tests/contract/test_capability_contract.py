"""Verify the host-neutral capabilities and authorization boundaries."""

from __future__ import annotations

from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_ROOT = REPOSITORY_ROOT / "plugins/compound-knowledge/docs/contracts"


class CapabilityContractTests(unittest.TestCase):
    def test_host_matrix_covers_every_platform_and_capability(self) -> None:
        content = (CONTRACTS_ROOT / "host-capabilities.md").read_text(
            encoding="utf-8"
        )
        for platform in ("Claude Code", "Codex", "WorkBuddy", "TRAE SOLO"):
            self.assertIn(platform, content)
        for capability in (
            "ask_and_wait",
            "workspace_search",
            "controlled_write",
            "role_delegation",
            "parallel_execution",
            "external_research",
            "workflow_continuation",
            "trusted_pipeline_signal",
        ):
            self.assertIn(f"`{capability}`", content)
        for status in ("`native`", "`fallback`", "`unavailable`"):
            self.assertIn(status, content)

    def test_behavior_contract_keeps_interaction_and_pipeline_safe(self) -> None:
        content = (CONTRACTS_ROOT / "workflow-behavior.md").read_text(
            encoding="utf-8"
        )
        for requirement in (
            "普通中文对话",
            "等待回答",
            "不得静默",
            "trusted_pipeline_signal",
            "计划明确声明的交付路径",
            "外部副作用",
            "人工授权",
            "幂等",
        ):
            self.assertIn(requirement, content)

    def test_role_contract_separates_read_only_roles_from_work_tasks(self) -> None:
        content = (CONTRACTS_ROOT / "role-execution.md").read_text(
            encoding="utf-8"
        )
        for role in (
            "knowledge-base-researcher",
            "past-work-researcher",
            "stale-knowledge-checker",
            "strategic-alignment-reviewer",
            "data-accuracy-reviewer",
        ):
            self.assertIn(f"`{role}`", content)
        self.assertIn("只读", content)
        self.assertIn("zs-work", content)
        self.assertIn("计划明确声明的交付路径", content)


if __name__ == "__main__":
    unittest.main()
