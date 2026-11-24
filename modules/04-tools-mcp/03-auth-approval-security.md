# 04.3｜MCP 安全：身份、审批、最小权限、幂等性

## 重要原则：模型不能充当身份提供者

用户在客户端已登录，不意味着模型可以随意声明另一个 \`user_id\`。身份应来源于 Host 的认证会话、受信任的身份断言或服务端验证的凭证，而不是从 LLM 生成的工具参数中信任一个 \`actor\` 字段。

典型错误设计：

~~~text
complete_task(user_id, task_id, approved=true)
~~~

这允许模型“指定用户”和“自称已获审批”，极容易越权。

推荐拆分：

~~~text
Host authenticated session (actor)
              |
              v
Server-resolved identity + task resource scope
              |
              v
Approval record (from actual user action)
              |
              v
Tool handler executes permitted operation
~~~

## 四层防线

1. **工具白名单**：只能执行被注册且当前用户允许使用的工具。
2. **资源级权限**：即使工具可用，也要检查对具体文件、记录、租户是否有权限。
3. **明确审批**：删除、发送、交易、批量更新等副作用操作，必须获得真实用户明确批准；批准记录应绑定调用者、资源和具体操作。
4. **重复调用保护**：为有副作用的操作设计业务幂等键、持久化台账与事务边界；不能只缓存模型响应。

## 对比三个概念

- **OAuth / Authentication**：证明谁在调用，以及凭证可代表的权限范围。
- **Authorization**：当前调用者是否可以执行此动作并访问该资源。
- **Human Approval**：当前具体动作是否得到了用户的额外确认。

OAuth 并不自动意味着每次危险操作都获批。反过来，弹窗确认也不能代替认证。

## Prompt Injection 与工具响应

MCP Server 返回的文档、资源和 Tool Output 可能被污染。Host 应把它们当作低信任数据：不能让外部文本覆盖系统策略；对有副作用的工具，即使模型被诱导提出调用，宿主也应在执行前拦截。

## 教学实验的边界

\`examples/mcp_task_store.py\` 在服务器实例中固定 actor，并将批准保存在进程内存，以演示权限逻辑。**这只证明一条业务规则可以拒绝操作**，不是 OAuth、会话隔离、签名批准或持久化事务的实现。

生产应用还需要：认证/授权中间件、审计记录、过期与撤销、并发一致性、真实确认 UI、跨重启幂等以及速率限制。

参考：[MCP SDK Authorization](https://py.sdk.modelcontextprotocol.io/run/authorization/)（请使用 SDK 当前导航核对路径）、[OWASP GenAI Security](https://genai.owasp.org/)。

[上一讲](02-mcp-protocol.md) · [下一讲](04-sdk-v2-practice.md)