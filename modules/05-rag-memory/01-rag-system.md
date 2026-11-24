# 05.1｜RAG 是检索增强生成，不是“装一个向量数据库”

## 1. RAG 的最小数据流

~~~mermaid
flowchart LR
  D[原始文档] --> P[解析 / 清洗]
  P --> C[Chunking]
  C --> I[索引<br/>Sparse / Dense / Metadata]
  Q[用户 Query] --> R[Retrieval]
  I --> R
  R --> K[候选 Chunks]
  K --> RR[Rerank / Filter]
  RR --> E[Evidence Context]
  E --> G[Generation]
  G --> V[引用 / 事实核验]
~~~

RAG 的核心不是“把文档转成向量”，而是：

> **给一个问题，从受控知识源中选择足够且正确的证据，让模型在证据约束下完成任务。**

## 2. 哪些场景不一定需要 RAG？

- 知识规模很小，整个可信资料集可以合理地放入上下文。
- 任务是确定性数据库查询，应该直接使用 SQL / API。
- 用户问的是实时市场价格，应调用实时数据源，而不是检索旧文档 Embedding。
- 问题要求执行动作，RAG 只能提供知识，不能替代 Tool Authorization。

不要把“模型不知道某个事实”统一归因为“需要向量数据库”。

## 3. 三种不同的失败

**Retrieval Failure**
: 正确证据根本没有进入候选 Top-k。

**Context Failure**
: 证据检索到了，但被截断、排序过低、与大量噪声混在一起，或缺少上下文。

**Generation Failure**
: 正确证据已经提供，但模型仍错误解释、计算或引用。

排查顺序很重要。只评最终答案，无法知道改 Prompt、换模型还是改检索更有效。

## 4. Hosted Retrieval 与自建 Retrieval

托管方案可以负责文件解析、Chunk、Embedding、索引和检索；自建方案可以更精确控制索引、版本、权限、排序与成本。工程决策应考虑：

- 数据权限和驻留要求。
- 文档规模与更新频率。
- 是否需要自定义 Sparse / Dense / Reranker。
- 可观测性、回溯与删除能力。
- 团队维护成本。

当前 OpenAI Retrieval / File Search 提供 vector store、语义与关键词检索、文件属性过滤和排序配置；课程不绑定某个厂商，具体参数以使用时官方文档为准。

## 练习

对“公司年度报告分析”“Android API 文档问答”“当前股价查询”“删除云端文件”四个任务，分别判断：
- 是否需要 Retrieval？
- 数据来自文档、数据库还是实时工具？
- 最终答案需要怎样的证据？
- 哪一步必须由确定性权限系统控制？

参考：[OpenAI Retrieval](https://developers.openai.com/api/docs/guides/retrieval) · [Anthropic Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval)

[下一讲](02-chunking-provenance.md)