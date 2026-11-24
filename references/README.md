# 参考资料（优先一手资料）

以下链接用于理解基本原理与核对版本特性。产品 API 与协议实现可能更新，请以访问时的最新官方文档为准。

## Agent 架构

- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- OpenAI — [Agents SDK](https://openai.github.io/openai-agents-python/)
- LangGraph — [Overview](https://docs.langchain.com/oss/python/langgraph/overview)

## 工具与协议

- Model Context Protocol — [Specification](https://modelcontextprotocol.io/specification)
- OpenAI — [API Docs](https://platform.openai.com/docs/overview)

## 评测与安全

- OpenAI — [Evaluation best practices](https://platform.openai.com/docs/guides/evaluation-best-practices)
- OWASP — [Top 10 for LLM Applications](https://genai.owasp.org/)
- OpenTelemetry — [Documentation](https://opentelemetry.io/docs/)

## 研究方法建议

- 先读概念原文，再读 SDK 文档，最后看开源示例。
- 做版本相关实验时注明依赖与模型标识；拒绝照搬可能已经过期的代码。
- 明确区分一手规范、实践博客、个人推测和实测结果。

## MCP Python SDK v2（2026-11 核对）

- [v2 安装与版本要求](https://py.sdk.modelcontextprotocol.io/get-started/installation/)
- [Host / Client / Server 与三大原语](https://py.sdk.modelcontextprotocol.io/get-started/first-steps/)
- [MCP Client transports](https://py.sdk.modelcontextprotocol.io/client/transports/)
- [v1 → v2 重要变动](https://py.sdk.modelcontextprotocol.io/whats-new/)
- [Python SDK 官方测试方式](https://py.sdk.modelcontextprotocol.io/get-started/testing/)

## Retrieval / RAG（2026-11 核对）

- OpenAI — [Retrieval guide](https://developers.openai.com/api/docs/guides/retrieval)
- OpenAI — [File Search](https://developers.openai.com/api/docs/guides/tools-file-search)
- OpenAI — [Embeddings](https://developers.openai.com/api/docs/guides/embeddings)
- Anthropic — [Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval)

课程中的 Chunk Size、Top-k、Hybrid Weight 和 Reranking 方案都应当作待评测超参数，而不是通用最佳值。

## 上下文工程（2026-11-24 核对）

- OpenAI — [Prompt caching（提示词缓存）](https://developers.openai.com/api/docs/guides/prompt-caching)
- OpenAI — [Compaction（上下文压缩）](https://developers.openai.com/api/docs/guides/compaction)
- OpenAI — [Evaluation best practices（评测实践）](https://platform.openai.com/docs/guides/evaluation-best-practices)

具体缓存条件和压缩接口随服务与模型而变；课程实验不调用这些 API，也不把教学近似计数当作真实 Token。

## 评测与轨迹（2026-11-24 核对）

- OpenAI — [Evaluation best practices（评测最佳实践）](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
- OpenTelemetry — [Traces（调用轨迹）](https://opentelemetry.io/docs/concepts/signals/traces/)
- OpenAI Agents SDK — [Tracing（轨迹记录）](https://openai.github.io/openai-agents-python/tracing/)

Lab 06 自行实现教学用轨迹结构，不使用 OpenTelemetry 协议或 Agents SDK；官方资料用于对照概念与生产实现边界。
