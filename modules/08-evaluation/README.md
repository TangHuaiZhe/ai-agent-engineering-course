# 评测与可观测性（Evaluation & Observability）

## 学习目标

- 定义端到端任务成功率与中间过程指标。
- 理解 Trace、评测集、回归与人工审核。
- 减少 LLM-as-Judge 带来的偏差。

## 核心概念

Gold Dataset；Success Rate；Tool Accuracy；Task Completion；Groundedness；Latency；Token Cost；Trace / Span；Rubric；回归、A/B 与统计置信。

## 思考题

1. 这部分的哪些失败可通过确定性代码预防？
2. 如果工具或模型没有按预期工作，系统应如何观测和恢复？
3. 什么情况下不该采用更复杂的 Agent 设计？

## 实验任务

构建至少 30 条任务案例，包含正常、模糊、缺失信息、工具失败与恶意输入。对两个 Agent 版本跑同一套评测，展示差异。

## 验收标准

报告同时包含成功与失败样例、版本、数据集、评估方法和限制；不能只报告单一总分。

## 学习记录

- [ ] 用自己的话解释关键概念
- [ ] 完成实验并记录输入输出
- [ ] 覆盖成功路径与失败路径
- [ ] 复盘一次设计取舍

> 延伸阅读见 [References](../../references/README.md)；当前内容为教学提纲，后续可添加深入讲义与实验代码。
