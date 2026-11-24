# Changelog

## v0.3.0 — 2026-11-24

- 将 Module 02 扩展为四节 LLM 基础讲义，并加入 Lab 00 结构化输出验证器和边界测试。
- 将 Module 04 扩展为四节 MCP 讲义，并加入 Lab 02：独立 MCP Server/Client、权限与幂等性实验。
- 使用当前 MCP Python SDK v2 的 MCPServer/Client API，区分 v1/v2 版本差异。
- 完善 GitHub Pages 导航、代码示例与单元测试；CI 增加可选 MCP SDK 集成测试 Job。


## v0.2.1 — 2026-11-24

- 添加 MkDocs Material 中文课程网站，包含导航、全文搜索、Mermaid 图、深浅色主题。
- 使用脚本从仓库 Markdown 构建站点，避免复制维护内容。
- 增加 GitHub Actions Pages 自动部署、部署说明与站点生成测试。

## v0.2.0 — 2026-11-23

- Module 03 从提纲升级为 5 节完整讲义，覆盖架构选型、决策循环与状态、工具/失败恢复、规划与 Multi-Agent、安全与评测。
- 新增 Lab 01：有边界的 Agent Loop，包含学习目标、实验步骤、失败注入、扩展挑战与评分标准。
- 新增无外部依赖的 bounded_agent.py：模型决策抽象、工具注册、输入校验、审批门槛、执行预算、幂等重放（单进程）及简化 Trace。
- 新增 15 项回归测试，覆盖正常及失败路径。
- 更新课程首页、路线图、示例导航和实验目录。

## v0.1.0 — 2026-11-23

- 初始化 10 个学习模块、12 周路线与课程大纲。
- 添加综合项目：上市公司研究 Agent。
- 添加最小 Agent Loop、可选 LLM API 示例、单元测试和 CI。
- 增加参考资料、贡献规范与维护约定。
