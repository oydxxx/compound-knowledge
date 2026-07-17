# Compound Knowledge 三轮真实端到端对比报告

状态：**BLOCKED — 尚无真实平台运行、评分或签字证据。**
报告日期：2026-07-16
固定材料数据截止日：2026-07-15

本文件是可导航的真实运行报告草稿，不是运行证据。静态合同、固定场景、目录占位符和本报告都不得替代真实平台运行。所有输入均固定在仓库内；验收过程不得依赖动态网络内容。

## 发布门槛与当前阻塞

只有三轮各自完成 1 份 Claude 原版和 4 份新版平台运行（共 15 份）、每份运行完成六阶段和独立回读、平台冒烟完成并由 A5 去标签盲评签字后，才可更新本报告的结论。

当前为 **BLOCKED**，原因如下：

1. 冻结原版 Claude 入口观察仍待人工实测，见 [原版入口观察](../../tests/acceptance/baseline/original-v1.0.0/claude-entry-observation.md)。
2. Claude Code、Codex、WorkBuddy、TRAE SOLO 均未完成真实安装、发现、调用、更新/缓存/卸载与可信信号冒烟证据；使用 [四平台冒烟清单](../../tests/acceptance/templates/platform-smoke-checklist.md)。
3. 三场景的 15 次隔离运行、90 份阶段证据、15 份回读探针和逐行为证据尚未产生。
4. 尚未移除平台标签、随机排序、盲评七维量表，也没有 A5 签字。

任何一项仍缺失、阶段门槛失败、关键事实/合规错误出现、或分数低于阈值，最终结论继续保持 **BLOCKED**；不得写为通过。

## 固定输入与种子

| 场景 | 固定输入 | seed_digest | 场景特点 |
| --- | --- | --- | --- |
| Quick | [输入](../../tests/acceptance/scenarios/quick/prompt.md)、[会议速记](../../tests/acceptance/scenarios/quick/context/meeting-notes.md)、[决策脚本](../../tests/acceptance/scenarios/quick/decision-script.md)、[完成合同](../../tests/acceptance/scenarios/quick/expected-contract.md) | `97f18371d61c48733a82b9593555099d19782159a7231c4461d2600538e72f53` | 单份速记形成一页改进计划；验证小任务不跳阶段 |
| Standard | [输入](../../tests/acceptance/scenarios/standard/prompt.md)、[固定上下文](../../tests/acceptance/scenarios/standard/context/)、[决策脚本](../../tests/acceptance/scenarios/standard/decision-script.md)、[完成合同](../../tests/acceptance/scenarios/standard/expected-contract.md) | `fe6cad606a506c0570fd5d7230693b8bfe06ca10007f0ed18ea0ea4f5259607a` | 历史知识检索、双角色审查、动态任务失败补跑 |
| Deep | [输入](../../tests/acceptance/scenarios/deep/prompt.md)、[固定上下文](../../tests/acceptance/scenarios/deep/context/)、[决策脚本](../../tests/acceptance/scenarios/deep/decision-script.md)、[完成合同](../../tests/acceptance/scenarios/deep/expected-contract.md) | `67c38b5f962e859d89bebcad321bb976d6fea877d39fde034fa475a604775fbc` | 多来源、跨约束、强制角色降级、任务补跑与外部副作用阻塞 |

`seed_digest` 的计算算法在各场景的完成合同中固定：只取列出的输入、上下文和决策脚本，按相对路径字节序、带路径前缀拼接 UTF-8 原文后计算 SHA-256。每个场景的五份真实运行必须记录相同值；任何变化都需重新固定输入并重新开始该场景的五份运行。

## 真实执行顺序（维护者操作）

对每个场景按以下顺序执行，不能让原版与新版同时注册：

1. 从固定场景复制一份独立消费方工作区；记录唯一 `workspace_id`、宿主环境、模型版本、安装来源、注册清单、核心摘要、缓存清理与全新会话证据。
2. **先**在只注册 [冻结原版 1.0.0](../../tests/acceptance/baseline/original-v1.0.0/README.md) 的隔离 Claude Code 环境运行。记录真实入口、原始参数和六阶段证据。完成后卸载或清除注册状态。
3. 为 Claude Code、Codex、WorkBuddy、TRAE SOLO **分别新建**四个工作区和环境胶囊；每个只注册新版，确认该场景 `seed_digest` 与原版相同后运行六阶段。
4. 每次运行都从 [运行清单模板](../../tests/acceptance/templates/run-manifest.md) 建立实际 `run-manifest.md`，并填入 [环境胶囊](../../tests/acceptance/templates/environment-capsule.md)、6 份 [阶段证据](../../tests/acceptance/templates/stage-evidence.md)、行为证据、上下文回执、异常/降级/恢复记录与 [回读探针](../../tests/acceptance/templates/readback-probe.md)。仅链接真实截图、转录或文件；不要把 QA 目录读入业务上下文。
5. 运行后将同场景五份产物去掉平台标签并随机排序，由 A5 依据 [评分量表](../../tests/acceptance/rubric.md) 评审；恢复标签后填写下列矩阵、差异与结论。披露评审者数量、模型差异和平台版本限制。

## 证据路径约定

每个目前的链接都只指向“无证据”占位 README。真实运行完成后，保留目录并在该目录创建下列实际文件，再把本报告的“实际证据”单元格改为这些真实文件链接：

- `run-manifest.md`、`environment-capsule.md`、`readback-probe.md`；
- `evidence/01-brainstorm.md` 至 `evidence/06-compound.md`；
- 每阶段对应的行为证据与上下文回执；
- 原始截图/文本转录、决策证据、失败与补跑记录；
- 去标签评分包、随机排序记录和 A5 签字。

不得预先创建上述材料、填写合成结果，或将空模板当成证据。

## Round 1 — Quick

固定合同：[Quick 完成合同](../../tests/acceptance/scenarios/quick/expected-contract.md)。重点：六阶段完整性、一页计划、计划内写入、知识回读。

| 比较对象 | 当前状态 | 占位目录／实际证据待填 | 六阶段、行为、回读 | 差异与评分证据 |
| --- | --- | --- | --- | --- |
| Claude 原版 | BLOCKED | [占位目录](../../tests/acceptance/runs/quick/claude-original/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |
| Claude Code 新版 | BLOCKED | [3.0.0 `zs-boom` 冒烟记录](../../tests/acceptance/runs/quick/claude-code/boom-smoke-2026-07-16.md)；尚无完整六阶段运行证据 | 已完成 `/zs:boom` 入口发现与原始参数转交；其余门槛待测 | 待去标签评分 |
| Codex 新版 | BLOCKED | [3.0.0 `zs-boom` 冒烟记录](../../tests/acceptance/runs/quick/codex/boom-smoke-2026-07-16.md)；尚无完整六阶段运行证据 | 已完成 `$zs-boom` 只读发现与调用；其余门槛待测 | 待去标签评分 |
| WorkBuddy 新版 | BLOCKED | [占位目录](../../tests/acceptance/runs/quick/workbuddy/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |
| TRAE SOLO 新版 | BLOCKED | [占位目录](../../tests/acceptance/runs/quick/trae-solo/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |

逐阶段差异（真实运行后填写）：

| 阶段 | 原版证据 | 四平台新版证据 | 翻译差异／宿主机制差异／允许差异／真实回归 |
| --- | --- | --- | --- |
| brainstorm | 待填 | 待填 | 待填 |
| plan | 待填 | 待填 | 待填 |
| confidence | 待填 | 待填 | 待填 |
| review | 待填 | 待填 | 待填 |
| work | 待填 | 待填 | 待填 |
| compound 与回读 | 待填 | 待填 | 待填 |

Quick 结论：**BLOCKED — 未产生原版与四平台的真实可比证据。**

## Round 2 — Standard

固定合同：[Standard 完成合同](../../tests/acceptance/scenarios/standard/expected-contract.md)。重点：固定历史知识、双角色审查、`T-CONTENT-02` 首次失败后只补跑该任务、知识回读。

| 比较对象 | 当前状态 | 占位目录／实际证据待填 | 六阶段、行为、回读 | 差异与评分证据 |
| --- | --- | --- | --- |
| Claude 原版 | BLOCKED | [占位目录](../../tests/acceptance/runs/standard/claude-original/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |
| Claude Code 新版 | BLOCKED | [占位目录](../../tests/acceptance/runs/standard/claude-code/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |
| Codex 新版 | BLOCKED | [占位目录](../../tests/acceptance/runs/standard/codex/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |
| WorkBuddy 新版 | BLOCKED | [占位目录](../../tests/acceptance/runs/standard/workbuddy/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |
| TRAE SOLO 新版 | BLOCKED | [占位目录](../../tests/acceptance/runs/standard/trae-solo/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |

逐阶段差异（真实运行后填写）：

| 阶段 | 原版证据 | 四平台新版证据 | 翻译差异／宿主机制差异／允许差异／真实回归 |
| --- | --- | --- | --- |
| brainstorm | 待填 | 待填 | 待填 |
| plan（历史知识） | 待填 | 待填 | 待填 |
| confidence | 待填 | 待填 | 待填 |
| review（双角色） | 待填 | 待填 | 待填 |
| work（失败补跑） | 待填 | 待填 | 待填 |
| compound 与回读 | 待填 | 待填 | 待填 |

Standard 结论：**BLOCKED — 未产生原版与四平台的真实可比证据。**

## Round 3 — Deep

固定合同：[Deep 完成合同](../../tests/acceptance/scenarios/deep/expected-contract.md)。重点：多来源与跨约束、强制 `fallback` 角色证据、`T-LAUNCH-02` 失败补跑、外部副作用阻塞与知识回读。

| 比较对象 | 当前状态 | 占位目录／实际证据待填 | 六阶段、行为、回读 | 差异与评分证据 |
| --- | --- | --- | --- |
| Claude 原版 | BLOCKED | [占位目录](../../tests/acceptance/runs/deep/claude-original/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |
| Claude Code 新版 | BLOCKED | [占位目录](../../tests/acceptance/runs/deep/claude-code/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |
| Codex 新版 | BLOCKED | [占位目录](../../tests/acceptance/runs/deep/codex/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |
| WorkBuddy 新版 | BLOCKED | [占位目录](../../tests/acceptance/runs/deep/workbuddy/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |
| TRAE SOLO 新版 | BLOCKED | [占位目录](../../tests/acceptance/runs/deep/trae-solo/README.md)；实际证据：待运行后链接 | 待真实运行 | 待去标签评分 |

逐阶段差异（真实运行后填写）：

| 阶段 | 原版证据 | 四平台新版证据 | 翻译差异／宿主机制差异／允许差异／真实回归 |
| --- | --- | --- | --- |
| brainstorm（多来源） | 待填 | 待填 | 待填 |
| plan（跨约束） | 待填 | 待填 | 待填 |
| confidence | 待填 | 待填 | 待填 |
| review（强制 fallback） | 待填 | 待填 | 待填 |
| work（补跑与副作用阻塞） | 待填 | 待填 | 待填 |
| compound 与回读 | 待填 | 待填 | 待填 |

Deep 结论：**BLOCKED — 未产生原版与四平台的真实可比证据。**

## 去标签评分与 A5 签字

评分使用 [三轮对比评分量表](../../tests/acceptance/rubric.md)。每个格必须链接到真实产物或差异说明；`zs-confidence` 的非数字化自检不得作为 QA 数字评分。英文原版的“中文自然度”“跨平台一致性”必须写 `N/A`，不得填 0 或虚构评价。

| 场景 | 语义保真 | 内容完整 | 逻辑结构 | 可执行性 | 事实准确 | 中文自然度（新版） | 跨平台一致性（新版） | 盲评证据与签字 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Quick | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | 待 A5 去标签评分与签字 |
| Standard | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | 待 A5 去标签评分与签字 |
| Deep | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | 待 A5 去标签评分与签字 |

评审披露（真实评审后填写）：评审者数量：待填；随机排序记录：待填；各平台/模型版本：待填；限制与偏差：待填。

## 最终发布结论

**BLOCKED。** 当前只能确认固定场景、决策脚本、种子摘要、证据目录和报告导航已准备好，不能据此推断任何平台行为、中文质量、知识闭环或发布资格。完成上述 15 次真实隔离运行、四平台冒烟、盲评与 A5 签字后，依据实际证据重新判定；在此之前，本报告不得标记为通过。
