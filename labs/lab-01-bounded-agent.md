# Lab 01｜实现有边界的 Agent Loop

**对应课程：** Module 03 · **预估学习时间：** 2–4 小时（依经验而异） · **依赖：** Python 3.11+

## 实验目标

在没有模型 API Key 的环境中，亲手验证 Agent 的五个基本约束：

1. 模型决策不是工具执行。
2. 工具名和参数必须由宿主校验。
3. 写入操作需审批，不能被外部文本间接授权。
4. 重复工具调用不会在同一次运行中造成重复副作用。
5. 模型调用和工具执行都有硬预算。

## 先运行示例

在仓库根目录：

~~~bash
python3 examples/deterministic_loop.py
python3 examples/bounded_agent.py
python3 -m unittest discover -s tests -v
~~~

第二个脚本使用 ScriptedDecider 代替真实模型。这样实验有确定性，不受 API 成本、网络、模型版本和随机采样影响。

## Part A — 画出状态转移

阅读 [03.2](../modules/03-agent-architecture/02-agent-loop-and-state.md)，为以下 5 种情况画出路径：

- 正常执行工具并返回 Finish；
- 无效工具名；
- 写操作等待审批；
- 已达工具预算；
- Tool Handler 抛出异常。

提交一个 Mermaid 状态图或 Markdown 表格。每个终止状态必须命名明确。

## Part B — 跟踪执行

阅读 [bounded_agent.py](../examples/bounded_agent.py)，回答：

- 什么时候增加 model_calls？
- 什么时候增加 tool_executions？
- 模型输出错误参数后，是否允许模型下一轮修正？
- 如果当前执行没有批准 save_note，哪些步骤保证它绝不会写入？
- Trace 为什么不直接记录所有参数和工具返回内容？

将这些结果写在你的学习日志中。

## Part C — 故障注入（必须完成）

阅读 [test_bounded_agent.py](../tests/test_bounded_agent.py)。测试至少应覆盖：

| 测试 | 预期 |
|---|---|
| 未知工具 shell | policy_denied |
| 参数 a=true（Python 中 bool 是 int 的子类） | invalid_arguments |
| 模型决策预算达到上限 | model_budget_exhausted |
| 工具执行预算为 0 | tool_budget_exhausted |
| 未授权 save_note | approval_required，写入列表为空 |
| 已授权 save_note，重复同一 call_id | 只写入一次 |
| 同一 call_id 换了参数 | call_id_conflict |
| 工具内部抛出包含敏感信息的异常 | model-visible Observation 中只有安全错误码 |

## Part D — 自己实现一个增强

**基础挑战（建议完成）**：添加一个只读工具 divide(a,b)，整数分母为 0 时返回受控错误，而不是异常外泄；添加三个测试（正常、除零、非数值）。

**进阶挑战（任选一项）**：

- 在工具调用前加入数据范围授权，如 read_document(doc_id) 只能读取批准的 ID。
- 注入 FakeClock 并引入 max_elapsed_seconds，确保长任务超时可测试。
- 为一次运行计算 trace summary，统计每类失败和执行次数。
- 把进程内执行台账替换成持久化 SQLite，并验证重启与并发行为。

注意：仅靠 SQLite 记日志也不能自动解决“外部服务完成副作用但本地事务尚未提交”的分布式原子性问题。生产系统需业务端的幂等键及正确的恢复协议。

## 报告模板

~~~markdown
# Lab 01 复盘
- 系统不变量：
- 有效工具清单：
- 授权边界：
- 测试命令与运行输出：
- 发生的一个错误及定位证据：
- 对“如何避免重复操作”的结论：
- 当前方案不能覆盖的场景：
~~~

## 评分标准（100 分）

| 项目 | 分值 | 验收 |
|---|---:|---|
| 能解释模型决策与工具执行的分离 | 20 | 关键步骤不混淆 |
| 运行与阅读 Trace | 20 | 能解释模型/工具两个计数 |
| 权限与校验用例 | 20 | 测试通过，无越权 |
| 预算与去重用例 | 20 | 测试通过，无额外副作用 |
| 扩展功能与复盘 | 20 | 有失败测试与局限性分析 |

**下一步：** Module 04 的 MCP 工具接口设计；本实验保留 Runner 基础供后续复用。