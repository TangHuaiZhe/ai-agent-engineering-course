# AI Agent 工程师：从原理到生产实践

> 面向软件工程师的中文、项目驱动 AI Agent Engineering 课程。
>
> 核心目标：把模型的不确定性决策变成可靠、可控、可评测、可审计的软件系统。

![Course](https://img.shields.io/badge/course-12%20weeks-blue) ![Language](https://img.shields.io/badge/language-%E4%B8%AD%E6%96%87-brightgreen) ![Status](https://img.shields.io/badge/status-v0.4.0%20in%20progress-lightgrey)

## 适合谁？

有基本编程经验，想从 LLM API 走向 Agent 系统工程的学习者。你不需要先训练大模型，但应理解基本 HTTP、函数、异常、测试和 Git。课程实践以 Python 为主，核心架构思想不依赖某种语言或框架。

## 十大核心模块

| 模块 | 主题 | 本课程的交付标准 |
|---|---|---|
| [01](modules/01-software-engineering/README.md) | Software Engineering | API、类型、异步与测试基座 |
| **[02](modules/02-llm-foundations/README.md)** | **LLM Foundations** | **4 节讲义 + Structured Outputs Lab 00** |
| **[03](modules/03-agent-architecture/README.md)** | **Agent Architecture** | **5 节正式讲义 + 有边界的 Agent Runner + 测试** |
| **[04](modules/04-tools-mcp/README.md)** | **Tools & MCP** | **4 节讲义 + 真正的 MCP Server/Client + Lab 02** |
| **[05](modules/05-rag-memory/README.md)** | **RAG & Memory** | **5 节讲义 + Hybrid Retrieval / Memory Lab 03** |
| [06](modules/06-orchestration/README.md) | Orchestration | 路由、并行、Checkpoint、HITL |
| [07](modules/07-context-engineering/README.md) | Context Engineering | 上下文预算与可信边界 |
| [08](modules/08-evaluation/README.md) | Evaluation & Observability | Evals、Trace、回归测试 |
| [09](modules/09-security/README.md) | Agent Security | 注入防护、权限隔离与审计 |
| [10](modules/10-production/README.md) | Production Engineering | 部署、限流、故障恢复与 SLO |

Module 02–05 已有分节讲义与可运行实验；Module 06–10 目前以知识地图和实践提纲为主，后续逐步完善。


## 在线课程网站（GitHub Pages）

[打开 AI Agent 工程师课程网站](https://tanghuaizhe.github.io/ai-agent-engineering-course/) · [GitHub Pages 部署说明](docs/deployment.md)

网站由 MkDocs Material 生成，支持中文导航、全文搜索、Mermaid 架构图、移动端适配与深浅色主题。仓库 Markdown 是唯一内容来源。**首次启用需在仓库 Settings → Pages 中将 Source 设为 GitHub Actions**；确认部署成功后链接才可正常访问。

## 从这里开始（当前推荐）

1. 阅读 [先修知识](docs/prerequisites.md) 和 [12 周学习路线](ROADMAP.md)。
2. 先读 [Module 02：LLM 基础](modules/02-llm-foundations/README.md)，再进入 [Module 03：Agent 架构](modules/03-agent-architecture/README.md)，再学习 [Module 04：MCP](modules/04-tools-mcp/README.md) 与 [Module 05：RAG & Memory](modules/05-rag-memory/README.md)。
3. 运行两个不用模型 API Key 的示例：

~~~bash
python3 examples/deterministic_loop.py
python3 examples/bounded_agent.py
python3 -m unittest discover -s tests -v
~~~

4. 依次完成 [Lab 00：结构化输出](labs/lab-00-structured-output.md)、[Lab 01：Agent Loop](labs/lab-01-bounded-agent.md) 和 [Lab 02：MCP 与授权](labs/lab-02-mcp-tools.md) 和 [Lab 03：RAG 与 Memory](labs/lab-03-rag-memory.md)。
5. 有真实 API 权限时，再尝试 [可选的真实模型工具调用示例](examples/README.md)。

## 课程理念

- **先原理后框架**：不把 LangGraph、Agents SDK、MCP 和 Skills 混作一谈。
- **先确定性后自主性**：能用固定 Workflow 做到的，不必强行使用 Agent。
- **先单 Agent 后 Multi-Agent**：复杂度应由真实评测收益证明。
- **先可观测后优化**：没有可复现的测试集，就没有可靠的质量提升结论。
- **安全由软件强制**：模型的 ToolCall 不是权限声明。
- **案例贴近工程**：贯穿上市公司研究 Agent，用来源、计算、权限和评测连接知识。

## 综合项目

[上市公司研究 Agent](projects/equity-research-agent/README.md)：研究规划、资料采集、数字抽取、确定性财务计算、引用核验与报告生成。所有数字必须保留来源、时间、单位和口径，禁止伪造数据。

## 进一步阅读与贡献

- [课程大纲](SYLLABUS.md) · [12 周路线](ROADMAP.md) · [所有实验](labs/README.md)
- [官方参考资料](references/README.md) · [贡献方式](CONTRIBUTING.md) · [维护约定](AGENTS.md)

> 课程由独立学习者维护，不代表任何模型厂商官方认证。当前版本 v0.4.0：Module 02–05 已包含正式讲义与实验，Module 06–10 仍在迭代。
