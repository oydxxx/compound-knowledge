# Standard 语义决策脚本

平台可使用不同的自然语言或结构化控件，但必须映射到以下稳定 ID 与答案。

| 决策 ID | 触发点 | 预置回答／允许默认值 | 验收含义 |
| --- | --- | --- | --- |
| S-DEC-01 | brainstorm 确定发布目标 | 选择“帮助现有团队管理员理解价值、编辑边界与低风险试用” | 不把目标改写成获客或促销 |
| S-DEC-02 | plan 确定主受众 | 选择“现有小团队客户中的团队管理员” | 成员与管理员的权限叙述必须区分 |
| S-DEC-03 | plan 确定渠道 | 选择“产品内、帮助中心、邮件、客户成功” | 每个渠道只产出草稿/提纲 |
| S-DEC-04 | review 处理治理顾虑 | 默认“把编辑边界与恢复说明纳入所有核心渠道” | 必须响应访谈与历史知识 |
| S-DEC-05 | work 任务 T-CONTENT-02 首次执行 | 返回“依赖产物缺少术语对照”，状态 `failed` | 只允许补跑 T-CONTENT-02；不得重跑成功的前置任务 |
| S-DEC-06 | work 补跑 | 提供前置术语对照后重试 T-CONTENT-02，状态 `success` | 保留同一任务 ID、依赖、可写边界和批次日志 |
| S-DEC-07 | compound 沉淀知识 | 选择“保存团队模板发布定位学习” | 必须知识写入并回读 |

动态任务合同：

| 任务 ID | 依赖 | 可写边界 | 初次结果 | 补跑 |
| --- | --- | --- | --- | --- |
| T-CONTENT-01 | 无 | `deliverables/team-templates-launch-content-plan.md` | success | 不适用 |
| T-CONTENT-02 | T-CONTENT-01 | `execution-logs/team-templates-launch.md` | failed（按 S-DEC-05） | 仅该任务按 S-DEC-06 补跑为 success |

若平台没有原生并行或子智能体能力，可串行完成，但不可改变任务 ID、依赖、写入边界、失败原因、补跑记录或聚合结果。
