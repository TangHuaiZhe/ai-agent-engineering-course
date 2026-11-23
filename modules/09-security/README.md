# Agent 安全工程（Agent Security）

## 学习目标

- 理解 Prompt Injection 与传统输入验证的区别。
- 设计最小权限、数据边界与审批机制。
- 区分不可信内容、可信策略、工具执行身份。

## 核心概念

Prompt Injection；Indirect Injection；Tool Poisoning；Secret Exfiltration；Least Privilege；Tool Allowlists；沙箱；身份代理；审计；安全预算；攻击面建模。

## 思考题

1. 这部分的哪些失败可通过确定性代码预防？
2. 如果工具或模型没有按预期工作，系统应如何观测和恢复？
3. 什么情况下不该采用更复杂的 Agent 设计？

## 实验任务

为文件/网页检索型 Agent 制作威胁模型。编写恶意文档片段诱导泄露秘密或执行危险动作，证明受限 Agent 会拒绝越权调用。

## 验收标准

至少覆盖数据窃取、越权操作、恶意工具返回与审批绕过；不能把“模型说不会做”当作安全隔离。

## 学习记录

- [ ] 用自己的话解释关键概念
- [ ] 完成实验并记录输入输出
- [ ] 覆盖成功路径与失败路径
- [ ] 复盘一次设计取舍

> 延伸阅读见 [References](../../references/README.md)；当前内容为教学提纲，后续可添加深入讲义与实验代码。
