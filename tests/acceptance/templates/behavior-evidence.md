# 行为证据

> 每个适用原版行为 ID 都要有结果合同；不得用静态清单替代真实平台运行。

```text
run_id: <same-as-manifest>
stage: <workflow stage>
workspace_id: <same-as-manifest>
behavior_ids: <pipe-separated B-... ids>
mechanism: <native|fallback>
status: <success|partial|blocked|failed>
source_evidence: <actual source/transcript path>
artifact_evidence: <actual output path>
error: <none or error record>
fixed_role_results: <five stable role ids and outcomes, or not-applicable-with-reason>
dynamic_task_results: <zs-work task ids/dependencies/write boundary/outcomes, or not-applicable-with-reason>
```

固定角色与动态任务不可互相借用权限。真实平台运行和原始产物才满足发布门槛；不得以静态数据宣称通过。
