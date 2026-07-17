# Deep 固定任务输入

## 任务

使用固定市场数据、历史策略、渠道约束和合规材料，制定「自动化异常洞察」功能的多渠道发布方案，并生成仅限本地审阅的交付物。该功能帮助运营团队识别异常指标，但不替代人工判断。

## 必须满足

- 只使用 `context/` 内的材料；不得联网、检索实时竞品、补充最新法规或臆造客户案例。
- 完成 `brainstorm → plan → confidence → review → work → compound` 六阶段；跨约束需要显式说明来源与取舍。
- 方案至少覆盖产品内、帮助中心、销售赋能和客户成功四个渠道，包含目标受众、定位、信息架构、渠道动作、节奏、角色、指标、风险、合规边界、待验证项和本地交付物。
- `review` 必须运行战略一致性与数据准确性职责；本场景强制至少一次能力降级，见 [decision-script.md](decision-script.md)。
- `zs-work` 必须执行有依赖的动态任务，并记录第二项首次失败、只补跑失败项、批次日志和可写边界。
- 不得发送消息、发布内容、改变真实告警规则、删除数据或写入计划外路径。

## 固定数据截止日

2026-07-15。

## 预期交付路径

- `plans/launch-automated-anomaly-insights.md`
- `deliverables/automated-anomaly-insights-launch-plan.md`
- `deliverables/automated-anomaly-insights-channel-messages.md`
- `execution-logs/automated-anomaly-insights.md`
- `docs/knowledge/automated-anomaly-insights-launch-guardrails.md`
