# AI Agent 工程师：从原理到生产实践

> 一门面向软件工程师的中文、项目驱动的 AI Agent Engineering 课程。
>
> 目标：从会调用 LLM API，进阶到能够设计、实现、评测、安全部署生产级 Agent 系统。

![Course](https://img.shields.io/badge/course-12%20weeks-blue) ![Language](https://img.shields.io/badge/language-%E4%B8%AD%E6%96%87-brightgreen) ![Status](https://img.shields.io/badge/status-draft%20v0.1.0-lightgrey)

## 这门课解决什么问题？

Agent 工程不是把大模型套在一个聊天 UI 上。它要求把**不确定性的模型决策**和**确定性的软件执行边界**结合起来，让系统能规划、调用工具、核验结果、恢复失败，同时可观察、可评测、可审计。

**学习成果：**
1. 不依赖框架实现带有工具调用、最大步数、错误处理与停止条件的 Agent Loop。
2. 设计安全的 Tool/MCP 接口，掌握状态、知识检索与上下文管理。
3. 实现复杂工作流：并行、分支、人工审批、持久化与恢复。
4. 建立评测集、回归测试和 Trace；能够量化成功率、延迟和成本。
5. 交付一个有安全边界、运行指标和部署文档的端到端 Agent 项目。

## 课程地图

| 模块 | 主题 | 关键产出 |
|---|---|---|
| [01](modules/01-software-engineering/README.md) | 软件工程基础 | API、任务执行与测试基座 |
| [02](modules/02-llm-foundations/README.md) | LLM 原理与模型 API | Prompt/结构化输出实验 |
| [03](modules/03-agent-architecture/README.md) | Agent 架构与循环 | 自研 Agent Loop |
| [04](modules/04-tools-mcp/README.md) | 工具调用与 MCP | 受限工具集成 |
| [05](modules/05-rag-memory/README.md) | RAG 与记忆 | 可溯源检索 |
| [06](modules/06-orchestration/README.md) | 工作流编排 | 持久化多步流程 |
| [07](modules/07-context-engineering/README.md) | Context Engineering | 上下文预算及压缩策略 |
| [08](modules/08-evaluation/README.md) | Evals 与可观测性 | 基准集、Trace 与回归报告 |
| [09](modules/09-security/README.md) | Agent 安全 | 威胁建模与防注入测试 |
| [10](modules/10-production/README.md) | 生产部署与可靠性 | 可恢复服务及运行手册 |

完整顺序见 [12 周学习路线](ROADMAP.md)；学习内容与验收方式见 [课程大纲](SYLLABUS.md)。

## 从哪里开始？

1. 阅读 [先修知识](docs/prerequisites.md) 与 [学习方式](docs/study-guide.md)。
2. 阅读 [第 03 模块](modules/03-agent-architecture/README.md) 的 Agent Loop 思维模型（即使你还不熟悉 LLM）。
3. 运行不需要 API Key 的第一个示例：

```bash
python3 examples/deterministic_loop.py
python3 -m unittest discover -s tests -v
```

4. 如有模型 API 权限，可运行 [真实模型调用示例](examples/README.md)，它使用只读的确定性工具。
5. 按 [实践任务](labs/README.md) 完成阶段里程碑。

## 综合实战：上市公司研究 Agent

[项目说明](projects/equity-research-agent/README.md) | [系统架构](projects/equity-research-agent/ARCHITECTURE.md) | [验收标准](projects/equity-research-agent/ACCEPTANCE.md)

该项目包含 Research Planner、资料检索、结构化财报抽取、指标计算、引文核验、审核与报告生成。特别强调：**原始事实与模型推断分离，不得伪造数据，不以模型生成内容代替来源核验。**

## 课程原则

- **先原理，后框架**：先自行实现最小 Agent，再引入 SDK 和图编排框架。
- **单 Agent 优先**：只有复杂度与可测得的收益支持时才拆分 Multi-Agent。
- **可复现**：每个实验有输入、输出、测试与验收标准。
- **安全默认**：外部数据不具备指令权限；高风险操作必须审批。
- **证据优先**：课程讲述的是长期有效的设计方法；版本变化以官方文档为准。

## 推荐阅读

详见 [References](references/README.md)。本课程为独立整理的学习计划，不代表 OpenAI、Anthropic、LangChain 或 MCP 项目官方认证。

## 参与完善

欢迎提交 Issue / PR。内容规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。

> 状态：**v0.1.0 课程骨架**。主题、练习、项目与代码示例已初始化，部分深入理论和生产级实现将在后续课程迭代。
