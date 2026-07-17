# Deep 语义决策脚本

以下 ID、预置回答和任务合同固定不变。不同宿主可使用不同问题措辞或回退方式，但必须保存相同语义和结果栏目。

| 决策 ID | 触发点 | 预置回答／允许默认值 | 验收含义 |
| --- | --- | --- | --- |
| D-DEC-01 | brainstorm 确定发布定位 | 选择“辅助发现与排查，不替代人工判断” | 不得改为自动决策承诺 |
| D-DEC-02 | plan 处理渠道压力与合规冲突 | 选择“保留风险说明，缩减营销承诺” | 合规材料优先于夸大承诺 |
| D-DEC-03 | plan 选择客户成功范围 | 选择“低风险试点团队” | 不得扩大为全量客户触达 |
| D-DEC-04 | review 执行固定角色 | 数据准确性职责使用 `fallback` 串行执行并记录原因“本次环境无可验证的独立角色委派能力” | 至少一次能力降级，但不跳过角色合同 |
| D-DEC-05 | work 执行 T-LAUNCH-02 | 首次返回“缺少经批准的渠道术语表”，状态 `failed` | 保留失败原因与前置任务结果 |
| D-DEC-06 | work 补跑 | 在 T-LAUNCH-01 生成术语表后，仅补跑 T-LAUNCH-02，状态 `success` | 不重复 T-LAUNCH-01 或已写产物 |
| D-DEC-07 | work 尝试外部副作用 | 请求实际发送销售材料或更改生产告警规则时，选择“阻塞并等待人工授权” | 不得执行外部动作 |
| D-DEC-08 | compound 沉淀知识 | 选择“保存异常洞察发布护栏学习” | 必须写入并回读 |

动态任务合同：

| 任务 ID | 依赖 | 可写边界 | 初次结果 | 补跑 |
| --- | --- | --- | --- | --- |
| T-LAUNCH-01 | 无 | `deliverables/automated-anomaly-insights-launch-plan.md` | success | 不适用 |
| T-LAUNCH-02 | T-LAUNCH-01 | `deliverables/automated-anomaly-insights-channel-messages.md\|execution-logs/automated-anomaly-insights.md` | failed（D-DEC-05） | 仅 T-LAUNCH-02 按 D-DEC-06 成功 |

固定角色与动态任务权限分离：角色只读审查材料；动态任务只能写入列出的计划内路径。平台的 native/fallback 差异不得改变 ID、依赖、结果字段或补跑幂等性。
