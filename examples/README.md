# Examples｜最小可运行代码

## 1. 最简 Agent Loop（不需要模型 API）

~~~bash
python3 examples/deterministic_loop.py
~~~

用于建立“模型决策 → 工具执行 → Observation → 再决策”的最小概念，不包括真实审批或持久化。

## 2. 进阶 Bounded Agent（Module 03 推荐）

~~~bash
python3 examples/bounded_agent.py
python3 -m unittest discover -s tests -v
~~~

这个示例将模型决策器抽象为 Protocol，使用 ScriptedDecider 模拟模型决策，演示：

- ToolRegistry 的工具白名单与 Schema 校验。
- “模型提出请求”与“程序真正执行”之间的权限边界。
- max_model_calls 与 max_tool_executions 两种独立预算。
- 同一运行中重复 call_id 的结果重放和参数指纹冲突处理。
- 对意外异常返回脱敏错误码，不泄露原始异常信息。
- 对有副作用的 save_note 工具要求明确审批标志。

**重要限制：** 这不是生产可用的审批系统，也没有跨进程幂等台账、OAuth、壁钟超时、令牌/金额预算或结构化分布式追踪。生产系统必须将权限与操作资源/调用方/具体参数绑定，持久记录审批与执行状态，并考虑多机并发。

对应教程：[Module 03](../modules/03-agent-architecture/README.md) | [Lab 01](../labs/lab-01-bounded-agent.md)。

## 3. 真实模型 Function Calling（选做）

~~~bash
python3 -m venv .venv
source .venv/bin/activate
pip install openai
export OPENAI_API_KEY='your-secret-key'
export OPENAI_MODEL='a-model-available-to-your-account'
python3 examples/openai_tool_agent.py
~~~

真实模型调用示例使用 OpenAI Responses API 的工具调用形式；不需要赋予文件系统或 Shell 访问权限。建议先读当前官方 [API 文档](https://platform.openai.com/docs/overview) 并检查 SDK 版本。

**不要提交 API Key**，也不要把学习示例的内存授权或模拟处理当成真实产品的安全策略。
