# 原版 1.0.0 稳定行为清单

来源：`source/plugins/compound-knowledge/skills/` 中冻结的六份 `SKILL.md`。本清单记录的是后续中文化与宿主适配必须保留的行为，不把 Claude 专有工具名称当作唯一实现机制。

## `kw-brainstorm`

- **B-BRAINSTORM-01（输入）**：接收 topic、brain dump 或 meeting notes，并先提取问题、目标、约束、利益相关者和已知信息。
- **B-BRAINSTORM-02（读取）**：自动检索相关的 `docs/knowledge/` 与 `plans/`，并允许补充引用。
- **B-BRAINSTORM-03（决策）**：对承重问题一次收集一至三个回答，再建议方向与下一步。
- **B-BRAINSTORM-04（写入）**：选择保存或继续 plan 时，必须先写入 `plans/brainstorm-{descriptive-name}.md`。
- **B-BRAINSTORM-05（续接）**：pipeline 模式跳过交互确认，并按默认行为写入产物后续接。

## `kw-plan`

- **B-PLAN-01（分类）**：自动判断工作类型，不把已有可推断的信息反问给用户。
- **B-PLAN-02（角色）**：研究 past work、knowledge base，并按需要加入数据或来源材料检查。
- **B-PLAN-03（读取）**：关联 `docs/knowledge/`、既有计划、项目规则和匹配的 brainstorm 起源文件。
- **B-PLAN-04（写入）**：按工作类型产出计划并写入唯一的 `plans/{type}-{descriptive-name}.md` 路径。
- **B-PLAN-05（续接）**：pipeline 模式跳过提问，按默认值写入并继续。

## `kw-confidence`

- **B-CONFIDENCE-01（评估）**：识别评估对象，诚实说明理解、证据、方法与未知项。
- **B-CONFIDENCE-02（输出）**：使用规定的 prose 结构；不得使用百分比、1–10、字母等级或其他数字化信心评分。
- **B-CONFIDENCE-03（决策）**：允许继续、补充研究、提问或保存评估；保存到活动计划或 `plans/confidence-{date}.md`。
- **B-CONFIDENCE-04（续接）**：恢复 `kw-work` 时从原任务位置继续，不破坏已有执行状态。
- **B-CONFIDENCE-05（pipeline）**：pipeline 模式跳过提问，并按默认写入行为继续。

## `kw-review`

- **B-REVIEW-01（读取）**：加载待审内容及项目规则引用的数据或业务上下文。
- **B-REVIEW-02（角色）**：调用战略一致性与数据准确性两个独立审查职责，再统一汇总。
- **B-REVIEW-03（判断）**：以 P1、P2、P3 和 Clean 栏目展示可定位发现；外部内容还执行编辑检查。
- **B-REVIEW-04（决策）**：呈现后续修订、接受或继续选项，不伪装未解决的问题。
- **B-REVIEW-05（pipeline）**：pipeline 模式跳过提问并继续默认流程。

## `kw-work`

- **B-WORK-01（读取）**：加载显式计划，或选取 `plans/` 中最近修改的计划。
- **B-WORK-02（任务）**：将计划拆成可交付任务，并按依赖分批。
- **B-WORK-03（角色）**：无依赖任务可并行委派；单项或高交互任务可内联执行。
- **B-WORK-04（阻塞）**：访问、依赖、用户决策或质量问题会记录阻塞，不擅自继续。
- **B-WORK-05（写入与续接）**：每批把执行日志写入计划；结束时总结完成与阻塞项，pipeline 模式跳过确认并写入后继续。

## `kw-compound`

- **B-COMPOUND-01（提取）**：从完成的知识工作中识别可复用学习，并先取得用户批准。
- **B-COMPOUND-02（读取）**：在 `docs/knowledge/` 检查重复，并执行陈旧知识检查职责。
- **B-COMPOUND-03（写入）**：必要时创建 `docs/knowledge/`，按 `docs/knowledge/{descriptive-slug}.md` 保存结构化学习。
- **B-COMPOUND-04（确认）**：报告新增学习及路径，并提供后续选择。
- **B-COMPOUND-05（pipeline）**：pipeline 模式跳过提问，按默认行为写入后继续。

## 记录约定

新版验收对每个适用行为 ID 记录机制（`native` 或 `fallback`）、结果状态（`success`、`partial`、`blocked` 或 `failed`）、来源、产物、错误与必要的补跑。行为 ID 是结果合同，不能因使用普通中文提问或串行角色回退而缺失。
