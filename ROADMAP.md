# 12 周学习路线

推荐节奏：每周 5–8 小时；概念阅读约 30%，实现与实验约 50%，复盘评测约 20%。

| 周次 | 核心目标 | 实验或具体任务 | 可验收的输出 |
|---|---|---|---|
| 01 | Python/TS、HTTP、async、JSON Schema、异常和测试 | 最小工具执行器 | 单测、输入 Schema |
| 02 | Transformer/Token、LLM API、结构化输出 | [Lab 00 结构化抽取](labs/lab-00-structured-output.md) | 输出验证与评测记录 |
| **03** | **Agent Loop、状态、权限、预算** | **[Module 03 + Lab 01](labs/lab-01-bounded-agent.md)** | **Runner、失败测试、状态机** |
| 04 | Function Calling、MCP、身份与审批 | [Lab 02 MCP 与授权](labs/lab-02-mcp-tools.md) | Server/Client 与越权拒绝测试 |
| 05 | Embedding、Chunking、Hybrid Search、Reranking | [Lab 03 Hybrid RAG + Memory](labs/lab-03-rag-memory.md) | Recall@k / MRR、引用 Gate、记忆更正 |
| 06 | 短期/长期记忆，状态与知识分层 | [Module 05 Memory 实验](modules/05-rag-memory/05-memory-and-state.md) | Supersede / Delete / Source Policy |
| 07 | 路由、并行、条件分支、评估优化 | 工作流编排 | 状态转移测试 |
| 08 | Checkpoint、人审、重试与恢复 | 中断/恢复实验 | 幂等性验证 |
| 09 | Context Engineering、预算与压缩 | 长任务上下文实验 | Token 与质量报告 |
| 10 | Evals、Trace、回归与指标 | 20–50 条测试样例 | 基准集、失败分类 |
| 11 | Prompt Injection、权限、沙箱 | 红队测试 | 威胁模型、攻击用例 |
| 12 | 部署、监控、成本、版本与灾备 | 综合项目 MVP | Demo、运行手册、评测报告 |

## 四个阶段性成果

- **M1（第 3 周）**：实现并理解无框架、预算可控的 Agent Loop。
- **M2（第 6 周）**：安全连接工具与知识，所有关键检索结果可溯源。
- **M3（第 9 周）**：设计持久化、人工审批、断点恢复与上下文治理。
- **M4（第 12 周）**：将综合项目部署到测试环境并经过功能、质量、安全与运维验收。

## 每周复盘模板

~~~markdown
# Week N 复盘
- 目标 / 学习记录：
- 实现链接及提交 SHA：
- 核心概念与反例：
- 故障注入：输入、期望、实际、定位证据：
- 指标：任务成功率、工具执行次数、延迟、成本（如适用）：
- 下次改动假设：
~~~

**说明：** 12 周是教学组织方式，不是完成复杂项目的进度保证。真正掌握能力以可运行产出与评测结果为准。
