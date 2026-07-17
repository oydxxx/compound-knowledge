# 上下文回执

> 此回执只列消费方工作区的实际读取；不得将 `tests/acceptance/`、评分材料或其他 QA 目录注入业务上下文，也不得以静态模板替代真实平台运行。

```text
run_id: <same-as-manifest>
stage: <workflow stage>
workspace_id: <same-as-manifest>
read_paths: <pipe-separated actual consumer-workspace paths>
content_summary: <summary or digest of each input>
priority_order: explicit-input|project-rules|source-materials|related-plans|docs/knowledge|docs/solutions
conflict_resolution: <source and decision, or none>
prior_stage_artifact: <none for brainstorm; same-run prior stage output otherwise>
```

真实平台运行的原始读取证据是发布门槛；静态检查不得替代。
