# 环境胶囊

> 每一次真实运行必须单独填写。不得以静态 fixture 或文档推断平台可用性；真实平台运行才是发布门槛。

```text
run_id: <same-as-manifest>
workspace_id: <same-as-manifest>
host_environment_id: <unique host/configuration capsule id>
platform: <actual platform>
model_version: <actual version>
install_source: <actual package/archive/source path>
registration_mode: <original|new>
registration_inventory: <six registered canonical entries; no mixed original/new registration>
core_digest: <sha256 or immutable source digest>
cache_clearance: <actual cache-clear action/evidence>
fresh_session_evidence: <actual new-session transcript/screenshot path>
trusted_pipeline_evidence: <native metadata path, or unavailable/fallback confirmation record>
```

同场景五次运行的 `workspace_id` 与 `host_environment_id` 必须不同，`seed_digest` 必须相同。不得用静态填写替代真实平台运行。
