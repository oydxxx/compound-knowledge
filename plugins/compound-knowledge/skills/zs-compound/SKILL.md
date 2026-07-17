---
name: zs-compound
description: 从已完成的知识工作中提取经批准的可复用学习，保存到 docs/knowledge/ 供未来工作检索。
---

# 沉淀学习

闭环不是保存一切，而是筛出未来确实有用的学习。

## 适用场景

计划、活动、分析或策略完成后；数据纠正、流程修复、策略洞察之后；或任何有意义的工作会话结束时使用。

## 流程

### 1. 识别学习

按本次输入、项目规则、来源材料、关联计划、`docs/knowledge/`、可选 `docs/solutions/` 的顺序扫描当前会话，标出冲突来源和取舍；最多提取 1–3 项：`insight`（新发现）、`playbook`（可重复流程）、`correction`（被纠正的假设/定义/来源）或 `pattern`（反复出现的系统现象）。没有值得单独保存的内容时如实说明工作已在计划/交付物中记录。

```markdown
**学习：** [一句话]
**类型：** [insight | playbook | correction | pattern]
**为何重要：** [它如何改变未来工作]
```

### 2. 先获批准

展示草稿，允许用户原样批准、编辑、跳过单项或补充遗漏。**未获批准不得保存任何内容。**没有 `ask_and_wait` 时使用普通中文对话并**等待回答**。

### 3. 查重与陈旧知识

对获批学习搜索 `docs/knowledge/` 和 `docs/solutions/`；相似条目存在时展示它并询问更新还是另存。执行 `stale-knowledge-checker` 职责，识别可能矛盾或过时的条目，并展示更新、移除或并存的建议。该职责无论 `native` 还是 `fallback` 都只返回文本，**不得写入或删除文件**。

<critical_requirement>
所有研究/陈旧检查职责只返回文本；只有主持的沉淀技能可在获批后写入或更新知识文件。
</critical_requirement>

### 4. 本地保存

仅由本技能在批准后写入；必要时创建 `docs/knowledge/`。新文件为 `docs/knowledge/{descriptive-slug}.md`，格式保持：

```markdown
---
type: [insight | playbook | correction | pattern]
tags: [relevant keywords for future search]
confidence: [high | medium | low]
created: [today's date]
source: [brief description of what triggered this]
---

# [学习标题]
## Context
[发现时的工作]
## Implication
[未来工作应如何改变]
```

### 5. 确认与下一步

报告新增/更新的学习和路径，以及未来哪些标签会触发检索；提供开始新计划、分享讨论或结束的选择。

## 独立运行、安全回退与恢复

- 探测 `workspace_search`、`role_delegation`、`controlled_write`。找不到目录代表空历史；首次合法写入可创建目录。角色或并行不可用时用角色标签串行执行并记录来源、结果与失败。
- 只有有效、不可伪造的 `trusted_pipeline_signal` 才可跳过提问、按默认批准与写入后续接；否则 `fallback` 到普通中文对话并等待回答。
- 未批准、未授权路径、缺少必要来源、删除旧条目和外部副作用都必须**阻塞**并记录恢复点。删除、发布、发送、登录以及其他外部副作用始终需要**人工授权**。
- 每项结果记录 `native`/`fallback`、状态、来源、产物和错误；恢复保持幂等，不重复保存或覆盖已完成内容。

## 规则

- 质量优先于数量；条目必须具体，标签服务未来检索。
- 先查重，再创建；必要的旧条目更新只在获得相应授权后执行。
