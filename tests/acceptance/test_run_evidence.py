"""Static checks for the acceptance-evidence format.

These tests validate a deliberately synthetic fixture.  They do not represent
platform execution evidence; live, isolated platform runs remain the release
gate.
"""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ACCEPTANCE_ROOT = REPOSITORY_ROOT / "tests" / "acceptance"
TEMPLATES = ACCEPTANCE_ROOT / "templates"
STAGES = ("brainstorm", "plan", "confidence", "review", "work", "compound")
PLATFORMS = ("Claude Code", "Codex", "WorkBuddy", "TRAE SOLO")


def parse_record(path: Path) -> dict[str, str]:
    """Read the simple, reviewable ``key: value`` evidence record format."""
    record: dict[str, str] = {}
    if not path.is_file():
        return record
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line or line.lstrip().startswith(("#", ">", "```")):
            continue
        key, value = line.split(":", 1)
        if key.replace("_", "").isalnum():
            record[key.strip()] = value.strip()
    return record


def split_values(value: str) -> tuple[str, ...]:
    return tuple(item for item in value.split("|") if item and item != "none")


def validate_run(run_root: Path) -> list[str]:
    """Return schema violations without claiming that a run is platform-valid."""
    problems: list[str] = []
    manifest = parse_record(run_root / "run-manifest.md")
    required_manifest = {
        "run_id", "scenario", "variant", "platform", "workspace_id", "seed_digest",
        "environment_capsule", "registration_mode", "pipeline_signal",
        "authorization_source", "declared_output_paths", "written_paths",
        "stage_artifacts", "readback_probe", "resume_completed_ids", "resume_log_entries",
    }
    problems.extend(f"manifest missing {key}" for key in required_manifest - manifest.keys())
    if problems:
        return problems
    if manifest["scenario"] not in {"quick", "standard", "deep"}:
        problems.append("invalid scenario")
    if manifest["variant"] not in {"original", "new"}:
        problems.append("invalid variant")
    if manifest["registration_mode"] not in {"original", "new"}:
        problems.append("invalid registration mode")
    if manifest["authorization_source"] in {"prompt", "parameter", "project-file"}:
        problems.append("untrusted authorization source")
    if manifest["pipeline_signal"] == "native" and manifest["authorization_source"] != "adapter-metadata":
        problems.append("native pipeline lacks adapter metadata")
    if manifest["pipeline_signal"] != "native" and manifest["authorization_source"] != "interactive-confirmation":
        problems.append("non-native pipeline must use interactive confirmation")

    declared = set(split_values(manifest["declared_output_paths"]))
    for path in split_values(manifest["written_paths"]):
        if path not in declared and not path.startswith(("plans/", "docs/knowledge/", "execution-logs/")):
            problems.append(f"unplanned write: {path}")

    capsule = parse_record(run_root / manifest["environment_capsule"])
    for key in ("run_id", "workspace_id", "host_environment_id", "platform", "install_source",
                "registration_mode", "registration_inventory", "core_digest", "cache_clearance",
                "fresh_session_evidence", "trusted_pipeline_evidence"):
        if not capsule.get(key):
            problems.append(f"capsule missing {key}")
    if capsule.get("workspace_id") != manifest["workspace_id"]:
        problems.append("capsule workspace mismatch")
    inventory = capsule.get("registration_inventory", "").lower()
    if "original" in inventory and "new" in inventory:
        problems.append("original and new are simultaneously registered")
    if capsule.get("registration_mode") != manifest["registration_mode"]:
        problems.append("capsule registration mode mismatch")

    artifacts = split_values(manifest["stage_artifacts"])
    if len(artifacts) != len(STAGES):
        problems.append("missing a six-stage artifact")
    for index, (stage, artifact) in enumerate(zip(STAGES, artifacts), start=1):
        stage_record = parse_record(run_root / artifact)
        for key in ("run_id", "stage", "workspace_id", "input_artifact", "output_artifact",
                    "decision_evidence", "behavior_evidence", "context_receipt", "status"):
            if not stage_record.get(key):
                problems.append(f"{stage} missing {key}")
        if stage_record.get("run_id") != manifest["run_id"]:
            problems.append(f"{stage} run mismatch")
        if stage_record.get("stage") != stage:
            problems.append(f"{stage} stage mismatch")
        if stage_record.get("workspace_id") != manifest["workspace_id"]:
            problems.append(f"{stage} workspace mismatch")

        behavior = parse_record(run_root / stage_record.get("behavior_evidence", "missing"))
        for key in ("behavior_ids", "mechanism", "status", "source_evidence", "artifact_evidence",
                    "fixed_role_results", "dynamic_task_results"):
            if not behavior.get(key):
                problems.append(f"{stage} behavior missing {key}")
        if behavior.get("mechanism") not in {"native", "fallback"}:
            problems.append(f"{stage} behavior mechanism invalid")

        receipt = parse_record(run_root / stage_record.get("context_receipt", "missing"))
        for key in ("run_id", "stage", "workspace_id", "read_paths", "content_summary",
                    "priority_order", "conflict_resolution", "prior_stage_artifact"):
            if not receipt.get(key):
                problems.append(f"{stage} receipt missing {key}")
        if "tests/acceptance" in receipt.get("read_paths", "") or "docs/acceptance" in receipt.get("read_paths", ""):
            problems.append(f"{stage} receipt reads QA material")
        prior = receipt.get("prior_stage_artifact")
        if index == 1 and prior != "none":
            problems.append("first stage must not name a predecessor")
        if index > 1 and (not prior or artifacts[index - 2] not in prior):
            problems.append(f"{stage} does not cite the prior same-run artifact")

    readback = parse_record(run_root / manifest["readback_probe"])
    for key in ("run_id", "workspace_id", "seed_digest", "knowledge_path", "retrieval_query",
                "retrieved_path", "related_excerpt", "probe_evidence", "status"):
        if not readback.get(key):
            problems.append(f"readback missing {key}")
    if readback.get("knowledge_path") != readback.get("retrieved_path"):
        problems.append("readback does not retrieve compound knowledge")

    completed = split_values(manifest["resume_completed_ids"])
    log_entries = split_values(manifest["resume_log_entries"])
    if len(completed) != len(set(completed)) or len(log_entries) != len(set(log_entries)):
        problems.append("resume duplicates completed work")
    if completed and set(completed) != set(log_entries):
        problems.append("resume log does not match completed work")
    return problems


def validate_scenario_isolation(run_roots: tuple[Path, ...]) -> list[str]:
    """Check the five-run equality/isolation contract for one fixed scenario."""
    manifests = [parse_record(root / "run-manifest.md") for root in run_roots]
    problems: list[str] = []
    if len(manifests) != 5:
        problems.append("scenario requires one original and four new runs")
        return problems
    if len({item.get("workspace_id") for item in manifests}) != 5:
        problems.append("workspace_id reused")
    if len({parse_record(root / item["environment_capsule"]).get("host_environment_id") for root, item in zip(run_roots, manifests)}) != 5:
        problems.append("host environment capsule reused")
    if len({item.get("seed_digest") for item in manifests}) != 1:
        problems.append("scenario seed_digest differs")
    if sum(item.get("variant") == "original" for item in manifests) != 1:
        problems.append("scenario needs exactly one original baseline")
    if {item.get("platform") for item in manifests if item.get("variant") == "new"} != set(PLATFORMS):
        problems.append("scenario needs all four new platforms")
    return problems


def write_valid_run(root: Path, *, scenario: str, variant: str, platform: str, number: int,
                    seed_digest: str = "seed-shared") -> Path:
    """Create a synthetic fixture solely for schema tests, never release evidence."""
    run_id = f"{scenario}-{variant}-{number}"
    run_root = root / run_id
    evidence = run_root / "evidence"
    evidence.mkdir(parents=True)
    artifacts = tuple(f"evidence/{index:02d}-{stage}.md" for index, stage in enumerate(STAGES, 1))
    (run_root / "run-manifest.md").write_text(
        "\n".join((
            f"run_id: {run_id}", f"scenario: {scenario}", f"variant: {variant}",
            f"platform: {platform}", f"workspace_id: workspace-{number}",
            f"seed_digest: {seed_digest}", "environment_capsule: environment-capsule.md",
            f"registration_mode: {variant}", "pipeline_signal: unavailable",
            "authorization_source: interactive-confirmation",
            "declared_output_paths: deliverables/brief.md",
            "written_paths: deliverables/brief.md",
            f"stage_artifacts: {'|'.join(artifacts)}", "readback_probe: readback-probe.md",
            "resume_completed_ids: task-1|task-2", "resume_log_entries: task-1|task-2",
        )), encoding="utf-8")
    (run_root / "environment-capsule.md").write_text(
        "\n".join((
            f"run_id: {run_id}", f"workspace_id: workspace-{number}",
            f"host_environment_id: host-{number}", f"platform: {platform}", "model_version: fixture",
            "install_source: fixture-only", f"registration_mode: {variant}",
            f"registration_inventory: {variant}-six-canonical-skills", "core_digest: fixture",
            "cache_clearance: fixture", "fresh_session_evidence: fixture", "trusted_pipeline_evidence: unavailable",
        )), encoding="utf-8")
    for index, (stage, artifact) in enumerate(zip(STAGES, artifacts), 1):
        behavior_path = f"evidence/{index:02d}-{stage}-behavior.md"
        receipt_path = f"evidence/{index:02d}-{stage}-context.md"
        (run_root / artifact).write_text(
            "\n".join((
                f"run_id: {run_id}", f"stage: {stage}", f"workspace_id: workspace-{number}",
                "input_artifact: consumer/input.md", f"output_artifact: {artifact}",
                "decision_evidence: fixture", f"behavior_evidence: {behavior_path}",
                f"context_receipt: {receipt_path}", "status: success",
            )), encoding="utf-8")
        (run_root / behavior_path).write_text(
            "\n".join((
                f"run_id: {run_id}", f"stage: {stage}", f"workspace_id: workspace-{number}",
                "behavior_ids: B-FIXTURE-01", "mechanism: fallback", "status: success",
                "source_evidence: fixture", f"artifact_evidence: {artifact}", "error: none",
                "fixed_role_results: not-applicable-with-reason",
                "dynamic_task_results: not-applicable-with-reason",
            )), encoding="utf-8")
        predecessor = "none" if index == 1 else artifacts[index - 2]
        (run_root / receipt_path).write_text(
            "\n".join((
                f"run_id: {run_id}", f"stage: {stage}", f"workspace_id: workspace-{number}",
                "read_paths: consumer/AGENTS.md|consumer/docs/knowledge/", "content_summary: fixture",
                "priority_order: explicit-input|project-rules|source-materials|related-plans|docs/knowledge|docs/solutions",
                "conflict_resolution: none", f"prior_stage_artifact: {predecessor}",
            )), encoding="utf-8")
    (run_root / "readback-probe.md").write_text(
        "\n".join((
            f"run_id: {run_id}", f"workspace_id: workspace-{number}", f"seed_digest: {seed_digest}",
            "knowledge_path: docs/knowledge/fixture.md", "retrieval_query: fixture",
            "retrieved_path: docs/knowledge/fixture.md", "related_excerpt: fixture", "probe_evidence: fixture",
            "status: success",
        )), encoding="utf-8")
    return run_root


class EvidenceTemplateTests(unittest.TestCase):
    def test_required_evidence_templates_exist(self) -> None:
        required = {
            "run-manifest.md",
            "stage-evidence.md",
            "behavior-evidence.md",
            "context-receipt.md",
            "environment-capsule.md",
            "readback-probe.md",
        }
        self.assertEqual({path.name for path in TEMPLATES.glob("*.md")}, required | {"platform-smoke-checklist.md"})

    def test_templates_state_the_live_release_gate(self) -> None:
        for path in TEMPLATES.glob("*.md"):
            if path.name == "platform-smoke-checklist.md":
                continue
            content = path.read_text(encoding="utf-8")
            self.assertIn("真实平台运行", content, path.name)
            self.assertIn("不得以静态", content, path.name)

    def test_rubric_preserves_na_and_non_numeric_confidence_rules(self) -> None:
        content = (ACCEPTANCE_ROOT / "rubric.md").read_text(encoding="utf-8")
        for required in ("中文自然度", "跨平台一致性", "N/A", "zs-confidence", "不得", "数字"):
            self.assertIn(required, content)

    def test_valid_synthetic_fixture_has_no_schema_violation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run = write_valid_run(Path(directory), scenario="quick", variant="new", platform="Codex", number=1)
            self.assertEqual(validate_run(run), [])

    def test_schema_rejects_missing_stage_and_qa_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run = write_valid_run(Path(directory), scenario="quick", variant="new", platform="Codex", number=1)
            manifest = run / "run-manifest.md"
            manifest.write_text(manifest.read_text(encoding="utf-8").replace(
                "06-compound.md", "missing-compound.md"), encoding="utf-8")
            receipt = run / "evidence/02-plan-context.md"
            receipt.write_text(receipt.read_text(encoding="utf-8").replace(
                "consumer/AGENTS.md", "tests/acceptance/runs/qa"), encoding="utf-8")
            problems = validate_run(run)
            self.assertIn("plan receipt reads QA material", problems)
            self.assertTrue(any("compound" in problem for problem in problems), problems)

    def test_schema_rejects_forged_authorization_unplanned_write_and_non_idempotent_resume(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            run = write_valid_run(Path(directory), scenario="quick", variant="new", platform="Codex", number=1)
            manifest = run / "run-manifest.md"
            content = manifest.read_text(encoding="utf-8")
            content = content.replace("authorization_source: interactive-confirmation", "authorization_source: prompt")
            content = content.replace("written_paths: deliverables/brief.md", "written_paths: secrets/token.txt")
            content = content.replace("resume_completed_ids: task-1|task-2", "resume_completed_ids: task-1|task-1")
            manifest.write_text(content, encoding="utf-8")
            problems = validate_run(run)
            self.assertIn("untrusted authorization source", problems)
            self.assertIn("unplanned write: secrets/token.txt", problems)
            self.assertIn("resume duplicates completed work", problems)

    def test_scenario_requires_isolation_and_shared_seed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runs = (write_valid_run(root, scenario="quick", variant="original", platform="Claude Code", number=1),) + tuple(
                write_valid_run(root, scenario="quick", variant="new", platform=platform, number=index)
                for index, platform in enumerate(PLATFORMS, 2)
            )
            self.assertEqual(validate_scenario_isolation(runs), [])
            manifest = runs[-1] / "run-manifest.md"
            manifest.write_text(manifest.read_text(encoding="utf-8").replace("seed-shared", "wrong-seed"), encoding="utf-8")
            self.assertIn("scenario seed_digest differs", validate_scenario_isolation(runs))


if __name__ == "__main__":
    unittest.main()
