# 原版 1.0.0 冻结基线

冻结日期：2026-07-16

此目录保存开始中文化与跨平台改造前的只读比较对象。`source/` 是从仓库当时的根级分发文档、`.claude-plugin/` 元数据和完整 `plugins/compound-knowledge/` 机械复制而来；实施计划 `docs/plans/`、测试、运行输出和任何后续适配器均被排除。

`source-manifest.txt` 是按路径排序的完整文件清单；`checksums.sha256` 保存每个文件的 SHA-256。不得从新版目录向此处同步文件；如校验值改变，必须视为基线被污染并重新从未经修改的 1.0.0 来源恢复。

MIT `LICENSE` 是冻结分发副本的一部分，保持原文。

`behavior-inventory.md` 把六个工作流中需保持等价的行为标为稳定 ID。`claude-entry-observation.md` 留出真实 Claude Code 环境的入口与参数传递观察；该人工证据未补齐前，不能把跨平台发布验收标为通过。
