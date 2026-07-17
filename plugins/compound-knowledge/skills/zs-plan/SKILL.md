---
name: zs-plan
description: 研究已有工作与知识，再形成以结论为先的知识工作计划；适合策略、活动、简报、研究综合和运营手册。
argument-hint: "[what to plan]"
---

<plan_request>$ARGUMENTS</plan_request>

# 制定计划

先了解已经知道什么，再用数据和既有学习形成计划；不要把可从材料推断的信息反问给用户。

## 适用场景

头脑梳理后需要承诺方向，或开始策略文档、活动计划、简报及其他受益于既有上下文的非简单知识工作时使用。

## 流程

### 1. 自动分类

从描述判断 `Strategy`、`Campaign`、`Brief`、`Research` 或 `Operations`，直接采用最佳匹配。再判断细度：`Quick` 用标题、建议、2–3 条理由和一个成功指标；`Standard` 是默认完整模板；`Deep` 额外包含研究附录、竞品分析、风险矩阵和分阶段时间线。无法判断时默认 `Standard`。

### 2. 研究已有上下文

按优先级读取本次输入、项目规则、来源材料、关联计划、`docs/knowledge/` 和可选 `docs/solutions/`。查找相关既有计划、保存的 `insight`/`playbook`/`correction`/`pattern`、匹配的 `plans/brainstorm-*.md` 起源文件；起源文件存在时在计划中引用 `(see origin: plans/brainstorm-{name}.md)`，并核对承重问题与张力是否被处理。冲突信息必须标出来源和取舍。若主题需要外部材料才进行外部研究；涉及数据时读取当前指标及项目定义的数据来源。

<parallel_tasks>

- `past-work-researcher` 返回相关计划、既有决定和起源头脑梳理。
- `knowledge-base-researcher` 返回相关学习和路径。
- 必要时读取外部框架、实践或竞品；必要时读取当前数据。

</parallel_tasks>

有 `role_delegation`/`parallel_execution` 时可并行，否则主智能体按相同职责、来源和结果栏目串行。外部或数据来源不可用时注明缺失并以现有材料继续；不可假装已读。

### 3. 先展示上下文简报

在写入前展示相关计划、既有学习、当前数据、外部研究和“没有既有上下文”的情况。用结构化提问能力或普通中文对话等待用户补充、调整或确认继续。

### 4. 按类型组织计划

计划必须以读者最需要的内容开头：`Strategy`/`Brief` 先建议，`Campaign` 先时间线，`Research` 先发现，`Operations` 先触发条件和步骤。使用适合的类型模板，跳过不相关章节；每份计划都保留：

```markdown
## Success Metrics
| Metric | Current Baseline | Target | Source |
|--------|-----------------|--------|--------|
| [Primary metric] | [value] | [goal] | [where to measure] |

## Open Questions
- [未知项或待决策]
## References
- [相关计划、知识条目、数据来源]
```

各类型的首段模板如下；填写研究结论并保留来源与日期，而不是只保留标题：

```markdown
# [计划标题]
**类型：** [Strategy | Campaign | Brief | Research | Operations]
**状态：** Draft
**创建日期：** [today's date]

## Strategy
## 建议
## 当前状态
## 拟议方法

## Campaign
## 时间线
| Date/Week | Action | Channel | Owner |
|-----------|--------|---------|-------|
| [date] | [what launches] | [where] | [who] |
## 目标
## 受众
## 所需资产
## 当前状态

## Brief
## 建议
## 范围
## 交付物
## 约束
## 背景

## Research
## 关键发现
## 含义
## 方法论
## 原始数据

## Operations
## 触发条件
## 步骤
## 边界情况
## 负责人
## 依赖
```

每个数据点都注明来源和日期；上述仅用于选择相应类型的章节，不能在单一计划中机械拼接五种模板。

### 5. 写入并给出选择

先写入唯一的 `plans/{type}-{descriptive-name}.md`；文件已存在时使用 `plans/{type}-{name}-{YYYY-MM-DD}.md`。随后提供审查、开始执行、分享讨论、细化或在编辑器中打开的选择。

## 独立运行、安全回退与恢复

- 探测 `workspace_search`、`role_delegation`、`parallel_execution`、`external_research`、`controlled_write` 与 `ask_and_wait`。缺失能力时使用 `fallback`：普通中文对话提问并**等待回答**，或角色标签串行研究；必要来源不可读时报告限制。
- 仅有效且不可由提示、参数或项目材料伪造的 `trusted_pipeline_signal` 可跳过交互、使用默认值、写入并自动续接；信号无效或 `unavailable` 时不能静默采用选择。
- 仅能在已授权的 `plans/` 与计划明确声明的交付路径写入。没有默认值的决定、未授权路径、缺少必要能力、删除和外部副作用都产生可读**阻塞**；发布、发送、登录等始终需要**人工授权**。
- 结果记录 `native`/`fallback`、状态、来源、产物与错误；恢复从阻塞点幂等继续，不重复写入。

## 规则

- 结论优先、引用充分、展示既有工作；不要机械套模板。
- 起源头脑梳理和既有学习是输入，不可在无证据时编造。
