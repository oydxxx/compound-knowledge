"""Executable failure-mode rules shared by the contract and acceptance gates.

These are deliberately small, platform-neutral policy fixtures.  They prove
that the documented fallbacks have testable outcomes; they do not pretend to
exercise a real host platform.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
import unittest


FIXED_ROLES = (
    "knowledge-base-researcher",
    "past-work-researcher",
    "stale-knowledge-checker",
    "strategic-alignment-reviewer",
    "data-accuracy-reviewer",
)
SAFE_ROOTS = ("plans/", "docs/knowledge/", "execution-logs/")


@dataclass(frozen=True)
class Outcome:
    status: str
    mechanism: str
    detail: str


def resolve_interaction(*, structured_question: bool, has_default: bool) -> Outcome:
    if structured_question:
        return Outcome("waiting", "native", "structured question")
    if has_default:
        return Outcome("waiting", "fallback", "ordinary Chinese question")
    return Outcome("blocked", "fallback", "ordinary Chinese question; no default")


def resolve_fixed_roles(native_available: bool, failed_native_roles: tuple[str, ...]) -> dict[str, Outcome]:
    """A partial native failure reruns only failed duties, all with stable IDs."""
    results = {}
    for role in FIXED_ROLES:
        if native_available and role not in failed_native_roles:
            results[role] = Outcome("success", "native", "native result")
        else:
            results[role] = Outcome("success", "fallback", "serial role result")
    return results


def knowledge_history_paths(existing: tuple[str, ...]) -> tuple[tuple[str, ...], bool]:
    """Missing knowledge directories are an empty history, not a fatal error."""
    readable = tuple(path for path in existing if path.startswith(("docs/knowledge/", "docs/solutions/")))
    return readable, not any(path.startswith("docs/knowledge/") for path in existing)


def is_safe_relative_path(path: str) -> bool:
    parsed = PurePosixPath(path)
    return not parsed.is_absolute() and ".." not in parsed.parts


def authorize_pipeline_write(*, signal_source: str, path: str, declared_paths: tuple[str, ...], external_effect: bool) -> Outcome:
    trusted = signal_source == "adapter-metadata"
    allowed_path = is_safe_relative_path(path) and (
        path in tuple(item for item in declared_paths if is_safe_relative_path(item))
        or path.startswith(SAFE_ROOTS)
    )
    if external_effect or not trusted or not allowed_path:
        return Outcome("blocked", "interactive-confirmation", "manual authorization required")
    return Outcome("success", "trusted-pipeline", "planned write")


def resume_tasks(completed_ids: tuple[str, ...], requested_ids: tuple[str, ...]) -> tuple[str, ...]:
    """Return only unfinished work while rejecting a corrupted duplicate checkpoint."""
    if len(completed_ids) != len(set(completed_ids)):
        raise ValueError("duplicate completed task id")
    completed = set(completed_ids)
    return tuple(task_id for task_id in requested_ids if task_id not in completed)


def resolve_dynamic_task(*, task_id: str, dependency_ids: tuple[str, ...], completed_ids: tuple[str, ...],
                         permitted_path: str, attempted_path: str, failed: bool) -> Outcome:
    """Dynamic work preserves its ID, dependency and write-boundary evidence."""
    if task_id in completed_ids:
        return Outcome("success", "resume", "already complete; do not rerun")
    if any(dependency not in completed_ids for dependency in dependency_ids):
        return Outcome("blocked", "task-contract", "dependency incomplete")
    if attempted_path != permitted_path:
        return Outcome("blocked", "task-contract", "write boundary exceeded")
    if failed:
        return Outcome("failed", "task-contract", "record failure for targeted retry")
    return Outcome("success", "task-contract", "batch result recorded")


class FailureModeTests(unittest.TestCase):
    def test_no_interactive_tool_waits_in_chinese_or_blocks_without_default(self) -> None:
        self.assertEqual(resolve_interaction(structured_question=False, has_default=True).mechanism, "fallback")
        self.assertEqual(resolve_interaction(structured_question=False, has_default=False).status, "blocked")

    def test_no_or_partial_role_agents_keep_all_fixed_role_contracts(self) -> None:
        no_agents = resolve_fixed_roles(False, ())
        partial = resolve_fixed_roles(True, ("data-accuracy-reviewer",))
        self.assertEqual(tuple(no_agents), FIXED_ROLES)
        self.assertTrue(all(result.mechanism == "fallback" for result in no_agents.values()))
        self.assertEqual(partial["data-accuracy-reviewer"].mechanism, "fallback")
        self.assertEqual(partial["strategic-alignment-reviewer"].mechanism, "native")

    def test_missing_knowledge_directories_are_empty_history(self) -> None:
        readable, create_on_first_compound = knowledge_history_paths(("plans/active.md",))
        self.assertEqual(readable, ())
        self.assertTrue(create_on_first_compound)

    def test_untrusted_pipeline_and_planned_path_boundaries_block(self) -> None:
        self.assertEqual(authorize_pipeline_write(
            signal_source="user-prompt", path="deliverables/brief.md",
            declared_paths=("deliverables/brief.md",), external_effect=False,
        ).status, "blocked")
        self.assertEqual(authorize_pipeline_write(
            signal_source="adapter-metadata", path="secrets/token.txt",
            declared_paths=("deliverables/brief.md",), external_effect=False,
        ).status, "blocked")
        self.assertEqual(authorize_pipeline_write(
            signal_source="adapter-metadata", path="deliverables/brief.md",
            declared_paths=("deliverables/brief.md",), external_effect=True,
        ).status, "blocked")
        self.assertEqual(authorize_pipeline_write(
            signal_source="adapter-metadata", path="deliverables/brief.md",
            declared_paths=("deliverables/brief.md",), external_effect=False,
        ).status, "success")

    def test_dynamic_task_resume_is_idempotent(self) -> None:
        self.assertEqual(resume_tasks(("task-1",), ("task-1", "task-2")), ("task-2",))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            resume_tasks(("task-1", "task-1"), ("task-1", "task-2"))

    def test_dynamic_task_failure_keeps_the_targeted_retry_boundary(self) -> None:
        failure = resolve_dynamic_task(
            task_id="task-2", dependency_ids=("task-1",), completed_ids=("task-1",),
            permitted_path="deliverables/brief.md", attempted_path="deliverables/brief.md", failed=True,
        )
        self.assertEqual(failure.status, "failed")
        self.assertEqual(resolve_dynamic_task(
            task_id="task-2", dependency_ids=("task-1",), completed_ids=("task-1",),
            permitted_path="deliverables/brief.md", attempted_path="outside.md", failed=False,
        ).status, "blocked")

    def test_contract_policy_is_not_path_traversable(self) -> None:
        self.assertTrue(is_safe_relative_path("plans/nested/brief.md"))
        self.assertFalse(is_safe_relative_path("plans/../../secrets/token.txt"))
        self.assertFalse(is_safe_relative_path("/plans/brief.md"))
        self.assertEqual(authorize_pipeline_write(
            signal_source="adapter-metadata", path="../outside.md",
            declared_paths=("deliverables/brief.md",), external_effect=False,
        ).status, "blocked")
        self.assertEqual(authorize_pipeline_write(
            signal_source="adapter-metadata", path="plans/../../secrets/token.txt",
            declared_paths=(), external_effect=False,
        ).status, "blocked")
        self.assertEqual(authorize_pipeline_write(
            signal_source="adapter-metadata", path="docs/knowledge/../secrets.md",
            declared_paths=(), external_effect=False,
        ).status, "blocked")
        self.assertEqual(authorize_pipeline_write(
            signal_source="adapter-metadata", path="plans/nested/brief.md",
            declared_paths=(), external_effect=False,
        ).status, "success")


if __name__ == "__main__":
    unittest.main()
