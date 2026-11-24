# Module 04｜工具调用与 MCP

本模块把 Module 03 的 Agent Loop 与外部世界连接起来。重点不仅是让模型会调用工具，更是让**每一次工具调用都具备明确接口、身份、权限和失败语义**。

## 学习目标

1. 区分模型的 Function Calling、宿主的 Tool Execution 和 MCP 的通信协议。
2. 解释 MCP Host、Client、Server 与 Tools / Resources / Prompts。
3. 掌握 stdio 和 Streamable HTTP 的适用场景，以及 Python MCP SDK v1/v2 的差别。
4. 能实现模型不能绕过的授权、审批、资源作用域和幂等性边界。
5. 使用真实的 MCP SDK Client 对 Server 进行协议层测试，而不是只调用 Python 函数。

## 课程导航

| 讲次 | 核心内容 | 实战产物 |
|---|---|---|
| [04.1 Tool Calling 与接口契约](01-tool-contracts.md) | Schema、执行权、错误分类和输出信任 | Tool Contract |
| [04.2 MCP 协议模型](02-mcp-protocol.md) | Host / Client / Server；三类原语；Transport | 系统关系图 |
| [04.3 工具安全与授权](03-auth-approval-security.md) | 身份、OAuth、审批、最小权限和幂等性 | 权限矩阵 |
| [04.4 Python MCP SDK v2](04-sdk-v2-practice.md) | 服务端、独立 Client、协议测试和版本迁移 | 实际 MCP Server/Client |
| [Lab 02：MCP 与授权](../../labs/lab-02-mcp-tools.md) | 工具隔离、审批、跨租户拒绝、重复操作 | 代码 + 测试 + 威胁分析 |

## 运行方式

~~~bash
# MCP v2 依赖单独安装；课程的基础实验不需要它
python3 -m pip install -r requirements-mcp-lab.txt

# 从宿主/独立客户端通过 stdio 启动真正的 MCP Server
python3 -m examples.mcp_course_client

# 先运行无需 SDK 的领域测试；随后运行使用 Client(server) 的协议测试
python3 -m unittest tests.test_mcp_task_store -v
python3 -m unittest tests.test_mcp_course_integration -v
~~~

示例不连接真实账户和生产系统。其审批演示是宿主内存级模拟，**不等同于 OAuth 或真实用户确认**；因此不得直接作为生产身份安全的模板。

## 版本说明（2026-11 核对）

MCP Python SDK v2 已采用 \`from mcp.server import MCPServer\` 与 \`from mcp import Client\`。在 v1 中常见的 \`FastMCP\`、\`ClientSession\` 和旧传输样例不应直接复制到 v2 项目。这里依照官方 v2 文档开发，项目依赖限制为 \`mcp>=2,<3\`。以后升级应先验证 SDK 的实际 API 与本课程测试。

[返回课程首页](../../README.md) · [官方 SDK 文档](https://py.sdk.modelcontextprotocol.io/)