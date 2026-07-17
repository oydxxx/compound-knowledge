# 原版 Claude Code 入口与参数传递观察

## 当前状态

**验证状态：部分人工实测，仍未完成。** 2026-07-16 在 Claude Code CLI `2.1.211`、OAuth 登录、每次 `--plugin-dir` 临时加载冻结插件的独立会话中记录了以下事实。它们只证明入口发现与最小调用，不代替六工作流、参数转交、更新/卸载或跨平台发布验收。

## 静态冻结事实（非运行证据）

- 插件清单名为 `compound-knowledge`，版本为 `1.0.0`。
- 六个技能的原 frontmatter 名为：`kw:brainstorm`、`kw:plan`、`kw:confidence`、`kw:review`、`kw:work`、`kw:compound`。
- 三个带参数技能使用 `#$ARGUMENTS`：brainstorm、plan、review。
- `kw-work` 也接受目标计划路径；其原技能正文把运行日志写回计划文件。

## 已观察到的入口行为

| 技能 | 实际发现入口 | 裸 `/kw:*` 是否可用 | 带参调用与收到的参数 | 证据路径 | 结果 |
| --- | --- | --- | --- | --- | --- |
| brainstorm（冻结原版） | `/kw:brainstorm` | 是 | 调用 `/kw:brainstorm 产品发布会议速记：目标是在下周前确定三项发布准备工作。` 被执行 | CLI session `80d1ba01-e353-4d18-b693-06ae5d2f9587`；临时工作区 `/private/tmp/compound-knowledge-claude-baseline.h3Z3SX/` | 部分通过；命令输出称写入了用户级 `~/.claude/plans/tender-pondering-neumann.md`，未在隔离工作区写入 |
| brainstorm（冻结原版） | `/compound-knowledge:kw:brainstorm` | 不适用 | 同一插件临时加载时立即返回 `Unknown command` | CLI session `71795e03-25dd-4ec8-998a-0ed2de41c720` | 不通过；该命名空间形式不是当前 CLI 的实际入口 |
| brainstorm（新版规范技能） | `/kw-brainstorm` | 不适用 | 规范技能被加载并用中文开始处理会议速记；测试附带的结构探测文字被识别为提示注入并拒绝执行 | CLI session `486de309-c63f-4a26-a265-38d90528b81a`；临时工作区 `/private/tmp/compound-knowledge-claude-new.*` | 部分通过；证明规范入口可发现与核心安全边界生效，但尚未验证兼容 wrapper 的原样参数转交 |
| brainstorm（新版插件内 wrapper） | `/kw:brainstorm` | 否 | 无参数调用立即返回 `Unknown command`，CLI 建议使用 `/kw-brainstorm` | CLI session `33cae10b-1b9c-4488-b0c3-f73e0aa2a2c3` | 不通过；插件内 wrapper 不能保留裸旧入口 |
| brainstorm（新版独立兼容命令，旧嵌套布局） | `/kw:brainstorm` | 否 | 将 adapter 的 `commands/kw/` 安装到隔离项目 `.claude/commands/kw/` 后，人工交互返回 `Unknown command` | 隔离项目 `/private/tmp/compound-knowledge-claude-standalone.JHeiNU/` | 不通过；`kw/brainstorm.md` 不会注册冒号入口 |
| brainstorm（新版独立兼容命令，平铺布局） | `/kw:brainstorm` | 是 | 从 `.claude/commands/kw:brainstorm.md` 发现命令；模型调用规范技能 `kw-brainstorm`，参数为原始会议速记且没有额外 `#` 前缀 | CLI session `e4354a3f-cfe7-4110-bdf5-4d04307046a8`；隔离项目 `/private/tmp/compound-knowledge-claude-flat.bjgJa5/` | 入口与参数转交通过；完整工作流、冲突、更新、缓存与卸载仍待测 |

### 本次发现的阻塞与后续动作

- 冻结原版的裸 `/kw:brainstorm` 会把产物写到用户级 `~/.claude/plans/`；它不满足 U8 所要求的隔离工作区证据。该文件未经本测试清理，删除需维护者明确授权。
- 新版 `/kw:brainstorm` 的真实兼容 wrapper、六个入口的参数转交、冲突、更新、缓存刷新与卸载仍待在独立消费方项目中逐项实测。
- 当前 Claude CLI 中插件内 wrapper 不提供裸旧入口；项目级 `.claude/commands/kw/` 也不支持将目录名转换为冒号。平铺 `.claude/commands/kw:*.md` 已验证可注册裸 `/kw:*`，并将 `brainstorm` 转交给规范技能。
- 2026-07-16 提高至 `$0.25` 的旧嵌套布局无参数重试在两分钟内没有产生模型输出或结果文件，已终止临时会话；该超时不构成通过证据。
- **人工交互复测（Claude Code 2.1.211）：旧布局失败、平铺布局通过。** 未限制工具的会话中，`.claude/commands/kw/brainstorm.md` 对 `/kw:brainstorm` 返回 `Unknown command`；改为 `.claude/commands/kw:brainstorm.md` 后，CLI 的命令清单含 `kw:brainstorm`，并调用规范技能 `kw-brainstorm`，参数没有额外前缀。R18 的入口发现与参数转交阻塞解除，其余发布验收仍保持未完成。
- 插件静态验证对冻结版和新版均通过，但均报告同一非阻塞警告：插件根 `CLAUDE.md` 不会作为项目上下文加载；这是插件维护 shim，不得作为消费方上下文证据。

## 待补充的人工实测记录

请在只安装冻结 `source/` 的隔离 Claude Code 环境中填写。每个观察须附日期、Claude Code 版本、安装方式、会话标识或截图/日志路径，并保留原始参数文本。

| 技能 | 实际发现入口 | 裸 `/kw:*` 是否可用 | 带参调用与收到的参数 | 证据路径 | 结果 |
| --- | --- | --- | --- | --- | --- |
| brainstorm | 见上；兼容 wrapper 待测 | 待测 | 待测 | 待测 | 待测 |
| plan | 待测 | 待测 | 待测 | 待测 | 待测 |
| confidence | 待测 | 待测 | 待测 | 待测 | 待测 |
| review | 待测 | 待测 | 待测 | 待测 | 待测 |
| work | 待测 | 待测 | 待测 | 待测 | 待测 |
| compound | 待测 | 待测 | 待测 | 待测 | 待测 |

缺少此实测证据时，R18 与任何依赖 Claude 兼容入口的发布验收保持阻塞。
