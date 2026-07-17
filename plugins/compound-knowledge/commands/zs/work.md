---
description: "兼容旧入口 /zs:work，转交规范技能 zs-work。"
argument-hint: "[plan file to execute]"
---

# /zs:work 兼容入口

<compatibility_arguments>$ARGUMENTS</compatibility_arguments>

将 `compatibility_arguments` 中的原始文本不改写、不补默认值地交给规范技能 `zs-work` 的 `SKILL.md` 执行。此文件只负责入口兼容，不复制或解释核心工作流；若 `zs-work` 未发现，报告阻塞并按安装说明修复，不得回退到本文件。
