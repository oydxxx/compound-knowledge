# 阶段证据（每阶段一份）

> 仅记录真实运行的原始路径与结果；不得以静态模板或合成 evidence 代替真实平台运行。

```text
run_id: <same-as-manifest>
stage: <brainstorm|plan|confidence|review|work|compound>
workspace_id: <same-as-manifest>
input_artifact: <actual input path>
output_artifact: <actual output path>
decision_evidence: <decision-script id and transcript/screenshot path>
behavior_evidence: <behavior evidence path>
context_receipt: <context receipt path>
status: <success|partial|blocked|failed>
degradation: <native|fallback|none plus reason>
exception: <none or actual exception record>
resume_record: <none or recovery record>
```

阶段 2 至 6 的 context receipt 必须引用同一运行上一个阶段的实际产物。真实平台运行是发布门槛，静态检查不得替代。
