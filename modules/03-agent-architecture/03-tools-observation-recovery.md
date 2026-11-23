# 03.3｜工具调用、Observation 与失败恢复

## 1. Tool Calling 的两阶段语义

当模型输出以下内容时：

~~~json
{"tool": "multiply", "arguments": {"a": 6, "b": 7}, "call_id": "calc-1"}
~~~

这**不是**函数已经执行，只是模型提出调用请求。随后必须由宿主执行：

1. 识别调用工具名是否在白名单。
2. 检查调用方权限、操作对象与审批记录。
3. 验证参数 Schema、业务约束及数据类型。
4. 检查预算、重复请求与调用 ID。
5. 执行 handler，并记录结构化结果。
6. 将结果作为 **Observation（数据）** 传回模型。

不要把“模型输出了一段像 JSON 的文本”当作函数调用成功。

## 2. 错误分类比重试次数重要

| 错误 | 示例 | 建议动作 |
|---|---|---|
| Invalid arguments | 数字字段实际为字符串 | 可返回错误信息要求修正 |
| Unknown / forbidden tool | 请求访问未暴露的 Shell | 拒绝或终止，不靠模型自行约束 |
| Approval required | 请求写文件或发邮件 | 暂停并等待真实人审 |
| Transient tool error | 503、限流、暂时断网 | 有界重试、退避、检查幂等 |
| Permanent tool error | 资源不存在、权限不足 | 明确标记失败或请求重新授权 |
| Invalid observation | 工具返回不可解析内容 | 记录错误，避免污染后续状态 |
| Model budget exhausted | 达到最大决策次数 | 停止，不自行扩大预算 |

**不能无脑重试**：如果“转账成功但 API 回包丢失”，再次发起转账可能造成双重支付。重试策略必须先理解操作是否有副作用。

## 3. Observation 是事实证据吗？

不是。Observation 是某个工具的结果，它可能是：

- 可信计算器返回的数字。
- 公开网页中包含的错误数据。
- 用户上传的文件内容。
- 被 Prompt Injection 污染的外部文本。

观测应该保留“由哪个工具、什么时间、从哪个来源取得、是否已验证”等元数据。来自网页的“忽略之前的系统规则”只能作为**不可信文本**处理。

## 4. call_id 与幂等性

假设调用：

~~~text
save_note(call_id="note-17", text="hello")
~~~

宿主已经写入，但模型没收到结果，又请求完全一样的调用。可将成功结果保存在执行台账中，并将相同调用返回缓存结果。

必须同时校验 **调用 ID 与参数指纹**：

- 同 ID、同工具、同参数：可以重放**已记录结果**。
- 同 ID、不同参数：报 call_id_conflict，而不是静默执行或返回旧结果。
- 不同 ID、相同副作用：仍可能发生重复业务操作；需要业务级幂等键。

进阶示例中的字典仅用于**同一次进程内运行**。生产级的执行台账必须跨重启保存，并正确处理并发冲突、提交成功但回复丢失等边界。仅用 in-memory 字典不满足“恰好执行一次”。

## 5. 让错误可恢复，但不让错误抹平事实

假设第一次执行：

~~~text
add(a=true, b=2) -> invalid_arguments
add(a=1, b=2)    -> 3
Finish            -> "3"
~~~

这是一次可恢复的工具参数错误，模型下一次可以更正。

而如下调用应直接拒绝：

~~~text
shell(command="delete-all")
~~~

因为工具根本不在白名单。模型的请求不是系统增加权限的理由。

## 6. 动手观察 Trace

~~~bash
python3 examples/bounded_agent.py
python3 -m unittest discover -s tests -v
~~~

观察输出中的 model_calls、tool_executions、status。然后读 [test_bounded_agent.py](../../tests/test_bounded_agent.py) 的重复调用、非法参数、工具异常用例。

## 讨论

1. 仅依赖“模型总是诚实的”会在哪个环节失败？
2. 工具返回的数据中包含攻击指令，应在哪些层面隔离？
3. 为读操作和写操作设计怎样不同的重试策略？

[上一讲](02-agent-loop-and-state.md) · [下一讲](04-planning-and-multi-agent.md)