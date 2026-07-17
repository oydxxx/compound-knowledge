# Standard 完成合同

## 固定输入集

- [prompt.md](prompt.md)
- [context/user-interviews.md](context/user-interviews.md)
- [context/historical-knowledge.md](context/historical-knowledge.md)
- [context/business-goal.md](context/business-goal.md)
- [decision-script.md](decision-script.md)

数据截止日：2026-07-15。`seed_digest` 使用与 Quick 相同的算法（以上文件按相对路径字节序排列、加路径前缀后以 UTF-8 原文拼接并算 SHA-256）；实际值：`fe6cad606a506c0570fd5d7230693b8bfe06ca10007f0ed18ea0ea4f5259607a`。

## 六阶段与行为覆盖

所有阶段均需覆盖其适用的稳定行为 ID：`B-BRAINSTORM-01..05`、`B-PLAN-01..05`、`B-CONFIDENCE-01..05`、`B-REVIEW-01..05`、`B-WORK-01..05`、`B-COMPOUND-01..05`。特别要求：

- `plan` 的读取证据必须体现固定历史知识、访谈、业务目标和消费者项目规则（如有），并按照规定优先级处理冲突。
- `review` 必须分别保存战略一致性与数据准确性职责的输入、结果和机制；串行回退不允许合并为无来源的一段结论。
- `work` 必须保存 `T-CONTENT-01` 成功、`T-CONTENT-02` 首次失败及只补跑后成功的证据。
- `compound` 必须产生知识文件并通过回读探针。

## 可核验输出

1. 内容计划清晰区分管理员与成员，说明价值、编辑者可见性、最近保存版本恢复和低风险试用；不得声称审批、细粒度权限、模板市场或跨组织共享已经提供。
2. 四渠道材料都只是草稿或提纲；任何实际发布、发送或生产环境改动必须阻塞并等待人工授权。
3. 所有事实可追溯至固定材料；访谈数量不是总体统计，历史知识不是市场数据。
4. 每阶段有同一运行的上下文回执、行为证据、决策证据、降级/异常/恢复记录；QA 与评分目录不得进入业务上下文。
5. 回读问题固定为：“向现有小团队介绍团队协作模板时，核心承诺与治理说明应如何并列呈现？”必须返回 `docs/knowledge/team-templates-launch-positioning.md` 的相关段落。

## 允许差异与失败条件

原生与回退机制、中文文案风格及排版可不同；任务与角色的结果合同不可不同。缺少双角色审查、历史知识读取、首次失败补跑、知识回读、环境隔离或出现关键事实错误，即为失败。
