# 宿主能力合同

此文档是作者与 QA 的规范源，不是运行时依赖。每个独立安装的 Skill 必须在自身正文和一级 `references/` 中含有完成其职责所需的最小探测、回退、阻塞与授权规则。

## 能力意图

| 能力 | 意图 | 安全回退 |
| --- | --- | --- |
| `ask_and_wait` | 提出一个需要用户决定的问题并等待 | 普通中文对话提问并等待回答 |
| `workspace_search` | 按上下文优先级检索消费方工作区 | 报告不可读取的来源，不假装已读 |
| `controlled_write` | 在允许范围内创建或更新本地产物 | 路径未授权时输出阻塞 |
| `role_delegation` | 以固定职责执行研究或审查 | 主智能体带角色标签串行执行 |
| `parallel_execution` | 并行处理互不依赖的角色或任务 | 依赖顺序串行执行 |
| `external_research` | 读取可选外部来源 | 记录不可用；固定验收不得依赖易变网络 |
| `workflow_continuation` | 按默认选择继续下一工作流 | 无默认值时阻塞并保存恢复点 |
| `trusted_pipeline_signal` | 证明非交互自动续接的可信调用来源 | `unavailable` 时每次回退人工确认 |

## 平台能力档案（实施前假设，必须以真实冒烟校正）

`native` 表示有可验证的宿主原生机制；`fallback` 表示通过合同中的安全等价路径完成；`unavailable` 表示不自动执行该动作。

| 平台 | `ask_and_wait` | `workspace_search` | `controlled_write` | `role_delegation` / `parallel_execution` | `external_research` | `workflow_continuation` | `trusted_pipeline_signal` |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Code | `native` | `native` | `native` | `native` / `native` | `native` 或 `unavailable` | `fallback` | 待实测；无证据时 `unavailable` |
| Codex | `fallback` | `native` | `native` | `native` / `native` | `native` 或 `unavailable` | `fallback` | 待实测；无证据时 `unavailable` |
| WorkBuddy | `fallback` | `native` 或 `fallback` | `native` 或 `fallback` | `fallback` / `fallback` | `unavailable` 或 `fallback` | `fallback` | `unavailable` |
| TRAE SOLO | `fallback` | `native` 或 `fallback` | `native` 或 `fallback` | `fallback` / `fallback` | `unavailable` 或 `fallback` | `fallback` | `unavailable` |

能力档案必须记录实测日期、平台/模型版本、安装方式、证据路径与异常。不能仅凭文档声明把某项标为 `native`。

## 消费方上下文顺序

按以下优先级建立上下文回执：本次明确输入与固定材料、消费方项目规则、来源材料、关联计划、`docs/knowledge/`、可选 `docs/solutions/`。缺失知识目录是空历史；首次合法 compound 写入可以创建目录。插件维护 `AGENTS.md` 只约束维护期，不得混入消费方业务上下文。
