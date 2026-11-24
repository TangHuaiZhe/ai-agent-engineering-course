# 04.2｜MCP：连接工具和上下文的协议，不是 Agent 的大脑

## MCP 的结构

~~~mermaid
flowchart LR
  U[用户] --> H[Host：AI 应用]
  H --> M[LLM]
  H --> C[MCP Client]
  C <-->|MCP Protocol| S[MCP Server]
  S --> T[Tools]
  S --> R[Resources]
  S --> P[Prompts]
  S --> B[文件 / API / 数据库]
~~~

- **Host**：承载 Agent 的应用，负责人与模型的交互以及访问策略。
- **Client**：Host 内部与某个 MCP Server 建立通信的协议客户端。
- **Server**：将某类能力和内容暴露为可发现的接口。
- **LLM**：根据任务产生建议与调用意图，**不是 MCP 通信端本身**。

## 三个核心原语

| 原语 | 常见控制者 | 用途 |
|---|---|---|
| Tools | 模型提出调用，Host 执行授权 | 查询数据或请求写入 |
| Resources | Host/应用选择 | 将文件或其它数据提供给模型 |
| Prompts | 用户或应用选择 | 可复用提示模板 |

一个 MCP Server 可以同时暴露三种原语。三者可以有不同的获取方式与权限边界，不能都当成“工具函数”。

## Transport 不是权限

- **stdio**：Host 启动本地子进程，适合桌面工具和本机集成；stdout 是协议通道，不应混入调试日志。
- **Streamable HTTP**：适合远程服务，需要部署 TLS、身份认证、访问控制与网络边界。
- **旧 SSE**：旧式传输，2025 年后被 Streamable HTTP 取代，不建议新系统优先使用。

传输协议决定信息如何传递，而**不是**谁有权进行哪些操作。localhost、stdio、HTTP 与 OAuth 授权仍是不同层面的设计问题。

## MCP 与 Skills

MCP 主要解决能力和上下文的标准化连接与发现；Skill 通常描述任务的操作方法、规则、模板和可复用流程。Skill 并不自动获得外部系统权限；权限仍由宿主和各服务控制。

## 版本坑

官方 Python SDK v2 将高层服务端从 \`FastMCP\` 改为 \`MCPServer\`，并加入第一类 \`Client\`。在阅读代码时要核对文档对应的版本，避免把 v1/v2 不同对象混用。

参考：[MCP Specification](https://modelcontextprotocol.io/specification)、[MCP Python SDK v2 — First steps](https://py.sdk.modelcontextprotocol.io/get-started/first-steps/)。

[上一讲](01-tool-contracts.md) · [下一讲](03-auth-approval-security.md)