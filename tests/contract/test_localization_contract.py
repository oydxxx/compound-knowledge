"""Guard the identifiers that must survive Chinese localization."""

from __future__ import annotations

from pathlib import Path
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    REPOSITORY_ROOT
    / "plugins/compound-knowledge/docs/contracts/localization.md"
)


class LocalizationContractTests(unittest.TestCase):
    def test_contract_locks_stable_protocol_identifiers(self) -> None:
        content = CONTRACT.read_text(encoding="utf-8")
        for identifier in (
            "`type`",
            "`tags`",
            "`confidence`",
            "`created`",
            "`source`",
            "`insight`",
            "`playbook`",
            "`correction`",
            "`pattern`",
            "`P1`",
            "`P2`",
            "`P3`",
            "`$ARGUMENTS`",
            "`plans/`",
            "`docs/knowledge/`",
        ):
            self.assertIn(identifier, content)

    def test_contract_requires_chinese_for_user_visible_material(self) -> None:
        content = CONTRACT.read_text(encoding="utf-8")
        self.assertIn("自然简体中文", content)
        self.assertIn("不得翻译", content)
        self.assertIn("MIT License", content)


if __name__ == "__main__":
    unittest.main()
