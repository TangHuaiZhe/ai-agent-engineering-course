# Module 02｜LLM 基础与 API 工程

本模块的目标不是训练自己的大模型，而是理解 **LLM 的输入、输出与不确定性**，并掌握将其封装为稳定工程组件的方法。适合已有软件开发基础、尚未系统学习大模型机制的工程师。

## 五项学习目标

1. 理解 Token、Embedding、Transformer Attention、上下文窗口和推理阶段的区别。
2. 知道模型“表达得很肯定”并不代表其所述事实可信。
3. 根据指令优先级设计 Prompt，并将外部数据视为不可信来源。
4. 用 Structured Outputs、Schema 和确定性验证保障接口质量，同时知道 Schema 无法证明语义正确。
5. 建立最小评测集，记录模型版本、成功率、Token、延迟与成本。

## 课程目录

| 讲次 | 内容 | 能力验证 |
|---|---|---|
| [02.1 LLM 如何工作](01-model-basics.md) | Transformer、Token、上下文窗口、推理过程 | 解释模型为什么会产生事实性错误 |
| [02.2 Prompt、指令与可靠性](02-prompt-and-reliability.md) | 指令层级、Few-shot、外部资料隔离 | 给出含恶意网页的输入并设计防护 |
| [02.3 Structured Outputs](03-structured-outputs.md) | JSON、JSON Schema、工具调用、类型校验 | 让程序拒绝格式不正确的输出 |
| [02.4 成本、延迟与评测](04-cost-latency-evals.md) | Token Budget、缓存、评测数据集与指标 | 对两个版本进行公平比较 |
| [Lab 00：结构化抽取](../../labs/lab-00-structured-output.md) | 不依赖模型的验证基座 + 可选 API 对比实验 | 可运行代码和测试报告 |

## 运行实验

~~~bash
python3 examples/structured_output_lab.py
python3 -m unittest discover -s tests -v
~~~

这个示例**故意不请求模型 API**，先把“错误响应如何被程序识别”讲清楚；真实模型对比实验是选做，按使用的 SDK 版本另行实现，不能把模拟验证成绩写成模型成功率。

## 判断是否学会

- [ ] 能解释上下文窗口为何不等于长期记忆。
- [ ] 能区分提示词约束、API 结构化输出约束以及宿主程序的业务规则。
- [ ] 能举例说明格式正确但内容错误的 LLM 输出。
- [ ] 可以读取含错误类型、额外字段和伪造依据的输入，并让 validator 拒绝。
- [ ] 能设计不少于 20 条具有边界条件的评测题，而非凭感觉比较模型。

后续连接：[Module 03 — Agent Loop](../03-agent-architecture/README.md) 与 [Module 04 — Tool & MCP](../04-tools-mcp/README.md)。

[返回课程首页](../../README.md)