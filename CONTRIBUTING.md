# 参与贡献

感谢你愿意让「想清楚再做」在更多真实场景中变得可靠。

## 最适合的贡献

- 提交一个真实但已匿名的使用场景，并说明它帮你做出了什么下一步；
- 报告 Codex、Claude Code 或其他平台的安装与运行问题；
- 改进中文表达、安装说明或隐私边界；
- 为新增或修改的行为补充相应测试。

## 提交前检查

1. 先搜索已有 Issue，避免重复。
2. 描述你输入了什么、期望看到什么、实际发生了什么；不要粘贴密钥、私人会议记录或其他敏感信息。
3. 运行以下检查，确认结果通过：

```bash
npm run test:installer
npm pack --dry-run
python -B -m unittest discover -s tests/contract -v
python -B -m unittest discover -s tests/acceptance -v
```

## 提交原则

- 保持技能名称、平台入口和安装行为一致；
- 将功能改动与无关格式改动分开；
- 不提交生成目录、账号凭据或用户内容。

当你不确定某个想法是否值得实现时，先开 Issue 讨论即可。
