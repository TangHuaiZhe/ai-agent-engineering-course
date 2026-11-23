# Module 03｜Agent 架构与运行循环

> 目标：掌握 Agent 的最小可解释工作原理，并且能使用**确定性代码**对其权限、执行预算和失败恢复实施控制。

本模块从“何时需要 Agent”入手，逐步讲清楚决策循环（Agent Loop）、状态（State）、工具观测（Observation）、执行预算（Budget）、规划（Planning）、多 Agent 与评测的关系。

## 学习成果

完成后应能够：

1. 为一个需求解释为什么选择纯代码、Workflow、RAG 或 Agent。
2. 不依赖任何 Agent 框架，设计一个有状态的决策—执行—观测循环。
3. 明确模型的决策权限与宿主应用的执行权限边界。
4. 正确处理未知工具、非法参数、工具失败、重复调用与运行预算。
5. 用测试和 Trace 验证 Agent 的行为，而不是只看最终答案。

## 讲义导航（建议顺序）

| 课程 | 关键问题 | 产出 |
|---|---|---|
| [03.1 Agent 与 Workflow](01-agent-vs-workflow.md) | 任务是否需要自主决策？ | 需求分类表 |
| [03.2 Agent Loop 与状态机](02-agent-loop-and-state.md) | 运行循环怎样实现？ | 状态与转移图 |
| [03.3 工具、观测与恢复](03-tools-observation-recovery.md) | 工具失败如何影响决策？ | 故障矩阵 |
| [03.4 Planning 与多 Agent](04-planning-and-multi-agent.md) | 何时引入更复杂的编排？ | 架构决策记录 ADR |
| [03.5 安全边界与评测](05-safety-and-evaluation.md) | 如何证明系统可靠？ | 基准集与威胁清单 |
| [实践 Lab 01](../../labs/lab-01-bounded-agent.md) | 亲手实现并扩展 Runner | 代码 + 单元测试 |

## 运行示例

要求 Python 3.11 或更高版本，核心示例不需要 API Key，也不需要第三方依赖：

~~~bash
python3 examples/deterministic_loop.py
python3 examples/bounded_agent.py
python3 -m unittest discover -s tests -v
~~~

- [基础示例](../../examples/deterministic_loop.py)：只演示最小决策循环。
- [进阶示例](../../examples/bounded_agent.py)：分离决策与执行，增加 ToolRegistry、执行预算、审批和重复请求处理。
- [进阶测试](../../tests/test_bounded_agent.py)：覆盖成功、失败、权限及预算路径。

**注意：** 脚本中的 ScriptedDecider 是模拟的模型决策器，并非真正的 LLM；in-memory 的审批与去重仅用于教学，不等同于生产级持久化、分布式幂等性或细粒度授权。

## 学习建议

- 第一天读 03.1、03.2，并画出状态转移图。
- 第二天逐行读 bounded_agent.py，从 Trace 反推每一步。
- 第三天完成 Lab 01 中的失败注入与扩展任务。
- 第四天阅读 03.4、03.5，写一份选择单 Agent 还是 Workflow 的设计决策记录。
- 第五天提交复盘，至少记录一个错误假设及修正证据。

## 完成标准（Definition of Done）

- [ ] 解释模型决策与宿主执行的区别，并给出一个越权实例。
- [ ] 能区分模型调用预算与工具执行预算。
- [ ] 能说明为什么“重试请求”不等于“安全地重做副作用”。
- [ ] 能画出成功、错误、超预算及审批等待的转移路径。
- [ ] 跑通示例与测试，并新增至少一个失败测试。
- [ ] 写出单 Agent / Workflow / Multi-Agent 的架构选型依据。

延伸阅读：[Anthropic — Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)、[OpenAI Agents SDK — Running agents](https://openai.github.io/openai-agents-python/running_agents/)。

[返回课程首页](../../README.md)