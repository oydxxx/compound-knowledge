# Codex 冒烟尝试：2026-07-16

状态：**部分通过 — 已完成真实只读发现与调用；生命周期和完整六阶段运行仍待测。**

## 已完成的隔离安装布局检查

- 隔离工作区：`/private/tmp/compound-knowledge-codex.Vuo3cJ`
- 安装布局：`.agents/skills/` 下有六个目录：`kw-brainstorm`、`kw-plan`、`kw-confidence`、`kw-review`、`kw-work`、`kw-compound`。
- 每份 `SKILL.md` 的 `name` 与父目录一致，且均包含 `agents/openai.yaml` 中文展示元数据。

## 真实 Codex 会话证据

- CLI：修复后为 `codex-cli 0.144.5`，使用 ChatGPT 登录。
- 会话方式：`codex exec --ephemeral --skip-git-repo-check --sandbox read-only -C /private/tmp/compound-knowledge-codex.Vuo3cJ`。
- 调用：`$kw-plan` 加中文计划请求。
- 观察结果：Codex 发现并加载 `kw-plan`，读取消费方 `AGENTS.md`，将请求分类为 Operations/Quick，以中文给出上下文简报和需要确认的范围；输出明确表示不会创建或修改文件。
- 实际最终消息与运行日志保留在隔离工作区的 `codex-last-message.md`、`codex-session.log`。本仓库仅记录其摘要，不把临时会话目录当作长期发布证据。

第二次独立只读会话使用不显式点名技能的中文请求。Codex 自动加载 `kw-brainstorm`，检索到并遵守同一份消费方 `AGENTS.md`，确认没有既有计划或知识库，再以中文提出两个承重范围选择。该结果证明中文自然语言调用可触发正确的核心工作流；其最终消息与日志分别在 `codex-natural-last-message.md`、`codex-natural-session.log`。

这证明 Codex 的本地发现、显式调用、中文交互回退和消费方规则读取可用；它**不**证明更新、缓存刷新、卸载、可信流水线信号、角色委派、完整六阶段或知识回读。

## 环境阻塞

初始 `codex --version` 无法启动，因为全局安装引用的原生二进制不存在：

```text
.../vendor/aarch64-apple-darwin/codex/codex ENOENT
```

经维护者授权原样重装后，CLI 已恢复，以上真实会话已完成。桌面 Codex 应用在此自动化环境中仍不允许被直接控制；后续仍须在上述隔离目录验证中文自然语言调用、同名更新、缓存刷新与卸载，并保存真实文本或截图证据。
