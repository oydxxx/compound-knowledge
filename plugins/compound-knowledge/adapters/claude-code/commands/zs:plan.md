---
description: "可安装的 /zs:plan 兼容入口；转交 zs-plan。"
argument-hint: "[what to plan]"
---

# /zs:plan 兼容入口

<compatibility_arguments>$ARGUMENTS</compatibility_arguments>

原样转交 `compatibility_arguments` 给已发现的规范技能 `zs-plan` 的 `SKILL.md`。此薄 wrapper 不含核心流程；未发现规范技能时阻塞并提示重新安装，绝不调用自身。
