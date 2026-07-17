# Quick 完成合同

## 固定输入集

- [prompt.md](prompt.md)
- [context/meeting-notes.md](context/meeting-notes.md)
- [decision-script.md](decision-script.md)

数据截止日：2026-07-15。`seed_digest` 在正式运行前按上述三个文件的相对路径字节序排序，逐个以 UTF-8 原文拼接（每份文件前加 `--- <relative-path>\n`）后计算 SHA-256；实际值：`97f18371d61c48733a82b9593555099d19782159a7231c4461d2600538e72f53`。五个环境必须记录同一值。

## 六阶段与行为覆盖

| 阶段 | 最少行为 ID | 必有结果 |
| --- | --- | --- |
| brainstorm | B-BRAINSTORM-01 至 B-BRAINSTORM-05 | 从速记提炼问题、读取空或现有本地历史、记录 Q-DEC-01、写入起源文件并续接 |
| plan | B-PLAN-01 至 B-PLAN-05 | 形成两周一页计划，记录范围和本地写入路径 |
| confidence | B-CONFIDENCE-01 至 B-CONFIDENCE-05 | 用非数字 prose 说明证据与未知项 |
| review | B-REVIEW-01 至 B-REVIEW-05 | 保存战略与数据准确性职责结果；若回退则分别记录 |
| work | B-WORK-01 至 B-WORK-05 | 任务拆分、依赖/阻塞、写入边界与执行日志 |
| compound | B-COMPOUND-01 至 B-COMPOUND-05 | 去重/陈旧检查、知识写入与确认 |

## 可核验输出

1. 一页计划含目标、范围/非目标、优先级、负责人角色、两周节奏、指标、风险和下一步。
2. 不把 45% 以外的完成率、原因数量或人力容量写成事实；未知项显式标注。
3. 三个预期交付路径之外的写入、删除、发布或发送必须要求人工授权并留下阻塞或确认记录。
4. 每阶段保存上下文回执，不读取 `tests/acceptance/`、`docs/acceptance/` 或评分材料；阶段 2 至 6 引用同一运行上一个阶段产物。
5. 回读问题固定为：“团队下次改善新用户导入体验时，应优先验证什么并提供哪些引导？”必须返回 `docs/knowledge/new-user-activation-friction.md` 的相关段落。

## 允许差异与失败条件

- 允许平台以原生能力或串行回退完成角色/任务，但行为 ID、决策、输入条件、结果栏目、任务依赖和可写边界必须等价。
- 中文措辞、版式与模型生成的非事实性建议可以不同。
- 缺任一阶段、关键决策、角色/任务结果、知识回读、环境隔离或事实关键错误，即为该运行二元失败，不能用评分抵消。
