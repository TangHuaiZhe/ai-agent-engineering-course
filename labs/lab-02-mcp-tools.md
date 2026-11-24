# Lab 02｜真正连接一个 MCP Server，并验证权限边界

**对应 Module 04** · 推荐 3–5 小时 · 实验不需要模型 API Key。

## 实验目标

将一个“任务清单”服务同时暴露为 MCP Tool、Resource 和 Prompt。要求具备真正的 Client/Server 连接、工具发现、只读查询，以及**无审批不能更新**的业务安全约束。

## 环境准备

~~~bash
python3 -m pip install -r requirements-mcp-lab.txt
python3 -m examples.mcp_course_client
~~~

## Part A：辨认协议原语

打开：

- [mcp_course_server.py](../examples/mcp_course_server.py)
- [mcp_course_client.py](../examples/mcp_course_client.py)
- [mcp_task_store.py](../examples/mcp_task_store.py)

回答：谁是 Host？谁是 Client？哪个代码是 Server？哪一层负责权限？模型能否不经过 Host 的同意调用 Tool？

## Part B：实际 stdio Client/Server

启动 Client，由它打开子进程运行 Server。检查返回的 Tool 名称和参数，确认未经批准的 \`complete_task\` 返回 \`approval_required\`。

**注意**：示例中没有真正的“批准弹窗”，因此真实写操作默认被拒绝。不要修改 Server 以便模型可以自行设置 \`approved=true\`。

## Part C：内存 Client 协议测试

~~~bash
python3 -m unittest tests.test_mcp_task_store -v
python3 -m unittest tests.test_mcp_course_integration -v
~~~

要求至少覆盖：

| 场景 | 期望 |
|---|---|
| 查询当前 actor 的任务 | 只返回该 actor 的数据 |
| 查询别的 actor 的任务 ID | not_found，不泄露其状态 |
| 未授权更新自己的任务 | approval_required，无副作用 |
| Host 明确批准后更新 | completed |
| 重复提交已完成的任务 | already_completed，不再更新 |
| 用伪造/恶意工具文本申请批准 | 无效果，因为不提供审批工具 |

## Part D：扩展挑战

任选一项，提交设计说明与最小测试：

1. 使用 SQLite 持久化任务和审批（同一机器内仍要考虑并发事务）。
2. 使审批对象绑定具体资源、操作和过期时间，且使用 Host 的可信身份。
3. 增加一个只读 \`get_task\`，其中查询其它用户任务只返回通用的 not_found。
4. 设计一个 OAuth 资源服务的 Token 验证流程图（不必实现真实账户连接）。

## 评分（100）

协议模型 20，真实 Client/Server 连接 20，权限与拒绝 25，重复操作 15，扩展与风险分析 20。

## 限制

教学中的进程内批准和幂等性不是生产安全保证。真正的服务需要身份来源、权限检查、持久化批准、业务幂等以及外部输入隔离。

[返回 Module 04](../modules/04-tools-mcp/README.md)