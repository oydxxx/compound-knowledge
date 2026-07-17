# 变更记录

本项目的重要变更记录在此文件中。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [3.1.0] - 2026-07-17

### 新增

- 新增 npm CLI 安装器：可通过 `install`、`status`、`update` 与 `uninstall` 管理 Codex 和 Claude Code 的分发文件；安装前预检全部目标，避免半套安装。
- Codex 默认安装到当前项目 `.agents/skills/`，可选用户级 `~/.codex/skills/`；Claude Code 安装到用户级 `~/.claude/skills/compound-knowledge`。
- 安装器默认不覆盖不同内容；`update` 会先备份旧目录，`uninstall` 会保护已修改的本地内容。

## [3.0.1] - 2026-07-16

### 修复

- 恢复 `zs-boom` 的完整梳理契约：在已有输入时，同一轮必须输出核心要素、参考资料、主题／张力／缺口，再提出 1–3 个带选项的承重问题。
- 恢复原版的固定输出模板、承重问题筛选标准、方向建议和下一步菜单，防止本地化时把工作流压缩成普通摘要。
- 增加合同测试，若上述骨架被删除则构建失败。

## [3.0.0] - 2026-07-16

### 破坏性变更

- 规范技能 `zs-brainstorm` 重命名为 `zs-boom`，Claude 对应入口改为 `/compound-knowledge:zs-boom` 与可选的 `/zs:boom`；旧名称不再分发。
- 此变更只调整名称，不改变梳理工作流、输入处理或 `plans/brainstorm-*.md` 产物语义。

## [2.0.0] - 2026-07-16

### 破坏性变更

- 六个规范技能从 `kw-*` 全面重命名为 `zs-*`；旧 `kw-*` 技能目录不再分发。
- Claude Code 入口改为 `/compound-knowledge:zs-brainstorm` 等规范入口；可选裸兼容命令改为 `/zs:*`。`/kw:*` 不再提供。
- Codex、TRAE SOLO 与 WorkBuddy 的安装目录、展示元数据、归档清单和验收合同统一使用 `zs-*`。

### 验证

- 重命名后的真实 Claude Code 与 Codex 冒烟记录必须重新生成；旧 `kw` 记录仅作为 1.x 历史证据，不能证明 2.0.0 的入口。

## [1.1.1] - 2026-07-16

### 修复

- Claude Code `2.1.211` 的裸旧命令兼容包改为平铺的 `.claude/commands/kw:*.md` 文件；嵌套 `kw/*.md` 不会注册 `/kw:*`。
- 所有新分发 wrapper 与核心技能以 `$ARGUMENTS` 原样传递参数，不再人为添加 `#` 前缀。

## [1.1.0] - 2026-07-16

### 新增

- 六个统一核心技能 `kw-*` 的自然简体中文分发说明，并为 Claude Code、Codex、腾讯 WorkBuddy 和 TRAE SOLO 提供安装、更新、卸载与调用路径。
- 各平台的中文自然语言调用示例；不能注册中文命令别名时继续保留英文规范名。
- 发行、隐私和安全合同检查：验证版本同步、链接、许可证校验值和 `CLAUDE.md` 薄 shim。

### 变更

- 规范技能名迁移并固定为 `kw-*`；Claude Code 的旧入口 `/kw:*` 继续通过条件兼容路径保留，具体可用性仍需真实宿主实测。
- 隐私与安全说明统一为本地优先：不收集遥测、不要求联网；宿主可选联网、模型调用或数据处理不等同于本技能主动联网。
- 发布、发送、登录、删除和其他外部副作用改为始终等待人工授权；外部检索仅是可选宿主能力。
- 跨平台自动契约测试只能验证静态结构和文档。四个平台的安装、发现、更新、卸载和回退必须保存真实运行证据，缺少真实证据不得宣称已通过。

## [1.0.0] - 2026-03-22

### 新增

- 3 个研究角色：`past-work-researcher`、`knowledge-base-researcher`、`stale-knowledge-checker`。
- `/kw:plan` 的并行研究架构：由角色执行检索，而不是只在主流程中内联搜索。
- `/kw:brainstorm` 自动检索知识库与历史计划。
- `/kw:compound` 的陈旧知识检查，在保存前标记矛盾。
- 来源文档链：梳理产物成为计划引用并交叉核对的来源。
- `/kw:plan` 的 Quick、Standard、Deep 三档细节层级。
- `/kw:work` 将执行日志写回计划文件，而非只留在会话中。
- 各交接点提供“推向验证”的提示。
- 六个技能的流水线模式。
- `PRIVACY.md` 和 `SECURITY.md`。

### 变更

- 从 `commands/kw/` 迁移到 `skills/kw-*/SKILL.md` 结构。
- 技能增加 `$ARGUMENTS` 捕获与 `argument-hint` frontmatter。
- 审查角色改为完全限定名称引用。
- “先给结论”规则按工作类型细化。
- `CLAUDE.md` 改为指向 `AGENTS.md` 的薄 shim。
- README 分为根目录介绍页和插件完整说明。

## [0.2.0] - 2026-02-23

### 新增

- `/kw:confidence`：以自然语言校准已知与未知，并给出可执行的补证建议。

## [0.1.0] - 2026-02-19

### 新增

- `/kw:brainstorm`：在规划前梳理想法与已有知识。
- `/kw:plan`：检索历史工作并形成可执行计划。
- `/kw:review`：执行战略对齐与数据准确性审查（P1/P2/P3）。
- `/kw:work`：带任务跟踪地执行计划。
- `/kw:compound`：把经验写入 `docs/knowledge/`。
- 战略对齐审查角色与数据准确性审查角色。
- 安装与使用说明。
