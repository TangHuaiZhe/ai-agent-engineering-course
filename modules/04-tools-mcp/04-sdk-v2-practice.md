# 04.4｜用 MCP Python SDK v2 实现并测试 Server/Client

本讲按照官方 **MCP Python SDK v2** 的 API 风格编写。不要把旧版的 \`FastMCP\` 导入路径直接复制到新版项目。

## 1. 安装

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-mcp-lab.txt
~~~

实验环境只使用假数据，不调用任何财务、通讯录或生产账户。

## 2. Server 是什么？

[示例 Server](../../examples/mcp_course_server.py) 使用：

~~~python
from mcp.server import MCPServer

mcp = MCPServer("Course Task Service")

@mcp.tool()
def list_tasks() -> list[dict[str, str]]:
    ...
~~~

它另外包含 \`@mcp.resource\` 与 \`@mcp.prompt\`，以便区分 Tools、Resources 和 Prompts。

实际源码将 Server 的工具请求转给一个普通 Python [TaskStore](../../examples/mcp_task_store.py)。这层业务逻辑独立于 MCP，因此可以在**未安装 SDK 时**对其进行快速单元测试。

## 3. 独立 Client 经 stdio 连接

~~~bash
python3 -m examples.mcp_course_client
~~~

[Client](../../examples/mcp_course_client.py) 使用：

~~~python
from mcp import Client, StdioServerParameters
~~~

它启动独立的 Python 子进程，连接 Server，并调用 \`list_tools\`、\`list_tasks\`、\`complete_task\`。未经过宿主审批，更新任务会返回 \`approval_required\`。这里故意没有提供模型可以自行“审批”的工具。

## 4. 使用内存 Client 进行集成测试

SDK v2 支持直接连接 Server 对象：

~~~python
from mcp import Client

async with Client(server) as client:
    available = await client.list_tools()
    result = await client.call_tool("list_tasks", {})
~~~

[测试代码](../../tests/test_mcp_course_integration.py) 在没有额外进程和端口的情况下测试协议层访问、更新拒绝与审批后更新。它不是在“直接调用 Python 函数”，而是通过 MCP SDK 的 Client 调用。

## 5. 测试命令

~~~bash
python3 -m unittest tests.test_mcp_task_store -v
python3 -m unittest tests.test_mcp_course_integration -v
~~~

前一组不依赖第三方库；后一组需要 \`mcp>=2,<3\`。CI 将为 MCP 单独安装依赖并运行协议测试。

## 6. 为什么不能直接用于生产？

- 进程内审批记录不能证明真实用户身份。
- \`TaskStore\` 没有数据库与跨进程事务。
- 演示固定 actor，不包含多用户会话管理或 OAuth。
- 错误码和审计信息都需要纳入公司实际的规范与合规要求。
- 不应把可被模型控制的参数当作授权证明。

[上一讲](03-auth-approval-security.md) · [进入 Lab 02](../../labs/lab-02-mcp-tools.md)