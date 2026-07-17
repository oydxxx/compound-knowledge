# 运行清单（真实运行填写）

> 此模板是证据索引；不得以静态 fixture、模拟输出或本文件替代真实平台运行的发布门槛。

```text
run_id: <scenario>-<baseline-or-platform>-<unique-id>
scenario: <quick|standard|deep>
variant: <original|new>
platform: <Claude Code|Codex|WorkBuddy|TRAE SOLO>
workspace_id: <globally-unique-isolated-workspace-id>
seed_digest: <immutable-sha256-for-this-scenario>
environment_capsule: environment-capsule.md
registration_mode: <original|new>
pipeline_signal: <native|fallback|unavailable>
authorization_source: <adapter-metadata|interactive-confirmation>
declared_output_paths: <pipe-separated planned paths>
written_paths: <pipe-separated actual paths>
stage_artifacts: 01-brainstorm.md|02-plan.md|03-confidence.md|04-review.md|05-work.md|06-compound.md
readback_probe: readback-probe.md
resume_completed_ids: <pipe-separated unique completed task ids, or none>
resume_log_entries: <one entry per completed id, or none>
```

`authorization_source` 不能是用户提示、参数或项目文件。可信流水线只能写入计划、执行日志、知识路径和上述已声明交付路径；计划外路径、删除、发布、发送与其他外部副作用仍须人工授权。

真实平台运行完成前，此清单不能标记为通过。
