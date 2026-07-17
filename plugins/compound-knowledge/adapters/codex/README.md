# Codex 适配

## 安装与发现

将每个标准技能目录复制到消费方仓库的 `.agents/skills/`，例如 `.agents/skills/zs-plan/SKILL.md`。Codex 只从 `.agents/skills` 扫描仓库技能；不要使用非标准发现路径。每个目录的 `agents/openai.yaml` 是可选 UI 元数据：`interface.display_name` 与 `short_description` 提供中文显示，`default_prompt` 保留 `$zs-*` 规范名，`policy.allow_implicit_invocation` 允许按中文请求匹配。它不改变 `SKILL.md` frontmatter 的规范名。

完成后开启**全新会话**，确认六个 `zs-*` 英文规范名和中文描述可见，用 `$zs-plan` 及中文自然语言各调用一次，并记录截图或文本证据。

## 更新、卸载和缓存

- **更新：**比较六个目录的清单后整体替换同名目录，避免在 `.agents/skills/` 留下第二份 `zs-*`；按当前 Codex 版本的界面或重启方式刷新缓存，并在全新会话复查发现结果。
- **卸载：**删除对应 `.agents/skills/zs-*` 目录，刷新缓存并在全新会话确认不再发现。
- **回退：**若 UI 元数据不显示，仍以 `SKILL.md` 的英文规范名和中文自然语言调用；不要另建正文副本。

## 上下文与授权

读取消费方项目的 `AGENTS.md` 及其明确输入、材料、计划和知识目录；插件维护 `AGENTS.md` 不属于消费方上下文。`trusted_pipeline_signal` 尚未有可证明来源时是 `unavailable`，必须使用 `fallback`：普通中文对话等待人工确认。不得把用户参数或项目文件当作可信信号，外部副作用始终需要人工授权。
