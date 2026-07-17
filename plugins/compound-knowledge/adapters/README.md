# 平台适配

六个 `skills/zs-*/SKILL.md` 是唯一权威正文。适配层只提供发现、显示或兼容入口，不能复制核心流程。每个平台安装后都应新开**全新会话**，确认英文规范名 `zs-*` 和中文说明可见，再用中文自然语言调用。

| 平台 | 安装说明 | 规范技能位置 |
| --- | --- | --- |
| Claude Code | [claude-code/README.md](claude-code/README.md) | 插件技能；必要时兼容命令 |
| Codex | [codex/README.md](codex/README.md) | `.agents/skills/` |
| WorkBuddy | [workbuddy/README.md](workbuddy/README.md) | 逐个导入归档 |
| TRAE SOLO | [trae-solo/README.md](trae-solo/README.md) | `.agents/skills/` |

## 通用生命周期与安全边界

- **安装：**只复制或导入标准技能目录；不要把插件维护用的 `AGENTS.md` 当作消费方上下文。
- **消费方规则：**读取用户项目的 `AGENTS.md`、`CLAUDE.md`、TRAE Rules 或 WorkBuddy 等价规则，并按技能正文的上下文优先级归一化。
- **缓存与全新会话：**更新前关闭旧会话；按宿主说明清理技能注册/缓存，再在全新会话检查六项发现结果。缓存残留或同名旧技能时不得宣称更新完成。
- **更新与卸载：**先列出已注册条目；更新时替换同一规范名，确认没有重复；卸载时移除该平台的注册或导入项，并在全新会话确认不可发现。
- **能力与回退：**`trusted_pipeline_signal` 只能来自不可由普通参数、项目文件或自然语言伪造的宿主调用元数据。档案为 `unavailable` 或信号不能证明时，使用 `fallback`：普通中文提问并等待人工确认。外部副作用始终需要人工授权。

这些说明是可执行检查清单，不是平台实测记录；真实状态必须写入冒烟证据。
