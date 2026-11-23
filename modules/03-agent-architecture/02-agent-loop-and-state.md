# 03.2｜Agent Loop 与状态：不是一个无限调用 LLM 的 while

## 1. 最小模型

把 Agent 视为一个有状态的策略执行系统：

~~~text
User Goal
   |
   v
[构建上下文] → [模型做出决策] → ┬→ Finish → [核验 / 输出]
                           |
                           └→ ToolCall → [宿主校验]
                                            |
                                            v
                                         [工具执行]
                                            |
                                            v
                              [Observation 写回状态]
                                            |
                                 (进入下一轮决策)
~~~

可以用一个抽象函数表示：

~~~text
decision_t = policy(goal, state_t)
state_(t+1) = reduce(state_t, execute(decision_t))
~~~

这里的 policy 可以是 LLM，也可以是模拟器或规则引擎。最关键的是：**policy 选择意图，executor 决定能否执行。**

## 2. State 应该包含什么？

区分两类数据：

**业务状态（Business State）**

- 用户目标、任务 ID、公司代码与报告截止日。
- 已经验证的来源、已完成的任务和待处理的依赖。
- 工具结果、需要人审的待办事项。

**执行状态（Execution State）**

- 已做多少次模型决策和工具执行。
- 已消耗多少 Token / 费用 / 墙钟时间。
- 当前运行阶段、错误、Trace、重试次数。
- 已经执行过的操作 ID 与幂等记录。

这些数据不能全部放进一个不断增长的 Prompt。某些字段必须**由宿主保存为结构化状态**，并独立于上下文窗口持久化。

## 3. Agent 是个有限状态机

常见状态包括：

| 状态 | 进入条件 | 可以转移到 |
|---|---|---|
| READY | 用户提交任务 | DECIDING |
| DECIDING | 已构建有效上下文 | FINISHED、CHECKING、FAILED |
| CHECKING | 模型请求调用工具 | EXECUTING、WAITING_APPROVAL、FAILED |
| EXECUTING | 权限和预算通过 | OBSERVING、FAILED |
| OBSERVING | 收到工具结果或受控错误 | DECIDING |
| WAITING_APPROVAL | 需要授权且尚未批准 | EXECUTING 或 CANCELLED |
| FINISHED | 模型完成且输出通过必要检查 | 终止 |
| FAILED / CANCELLED | 无法继续或明确终止 | 终止 |

说明：本模块的示例为简化实现，遇到缺失审批时直接返回 approval_required，而非真正暂停和持久化。生产级系统应提供真实的等待及恢复流程。

## 4. 两套预算不要混淆

**模型决策次数（model_calls）** ≠ **工具执行次数（tool_executions）**。

在一个“一轮决策最多生成一个工具调用”的示例中：

- 第 1 次决策：调用 multiply → 执行工具 1 次。
- 第 2 次决策：返回 Finish → 无工具执行。
- 总计：model_calls = 2，tool_executions = 1。

还有一些 API 允许模型在单次响应中请求多个工具调用。此时模型轮次与工具调用数更不能混为一谈。SDK 对“turn”的定义也可能不同，阅读具体版本文档时应核对。

为了避免 Off-by-one 错误，明确：

- 每次调用 policy 都消耗一个 model_call。
- 每次尝试工具 handler（即使失败）都消耗一个 tool_execution。
- 返回 Finish 不消耗工具预算。
- 超出预算时不得“再试一次”，也不能悄悄改大预算。

## 5. 运行伪代码

~~~python
for _ in range(max_model_calls):
    decision = model.decide(goal, state)

    if decision.type == "finish":
        return verify_then_finish(decision)

    if decision.type != "tool_call":
        return invalid_decision()

    check_tool_exists(decision.name)            # 白名单
    require_approval_if_needed(decision)        # 权限
    check_budget_before_execution()
    result = execute_validated_tool(decision)   # 执行，可能出错
    state.observations.append(result)            # 写回观测

return model_budget_exhausted()
~~~

## 6. 四个不可丢失的不变量（Invariants）

1. **无授权不执行**：模型生成 ToolCall ≠ 用户已经授权。
2. **无 Schema 不执行**：参数通过模型生成不意味着类型正确。
3. **无预算不执行**：模型的“只再试一次”不能绕过硬限制。
4. **真实执行才写成功**：工具结果必须来自已执行的 handler，不能由模型凭空宣称。

推荐阅读代码：[bounded_agent.py](../../examples/bounded_agent.py)。

## 思考题

- 模型第一次请求工具、第二次给出最终答案：max_model_calls=1 时应该怎样？
- 工具执行 1 次后响应丢失，模型重新提交相同 call_id，怎么办？
- 用户让 Agent “继续到做完为止”，为什么不能移除预算？

下一讲会把这些边界落实到错误分类、观测和去重。

[上一讲](01-agent-vs-workflow.md) · [下一讲](03-tools-observation-recovery.md)