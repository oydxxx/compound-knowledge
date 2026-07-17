# 知识回读探针

> 此探针不是第七个产品工作流。它必须在六阶段完成后于同一隔离工作区执行，且不得以静态模板替代真实平台运行。

```text
run_id: <same-as-manifest>
workspace_id: <same-as-manifest>
seed_digest: <same-as-manifest>
knowledge_path: <new compound knowledge file path>
retrieval_query: <fixed scenario query>
retrieved_path: <same knowledge_path>
related_excerpt: <actual returned relevant excerpt>
probe_evidence: <actual transcript/screenshot path>
status: <success|partial|blocked|failed>
```

真实平台运行和原始回读记录才满足发布门槛；静态检查不得替代。
