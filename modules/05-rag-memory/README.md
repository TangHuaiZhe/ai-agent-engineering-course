# Module 05｜RAG、检索评测与长期记忆

本模块解决两个经常被混在一起的问题：

1. **RAG / Retrieval**：从外部知识库里找到完成当前任务所需的证据。
2. **Memory**：跨步骤或跨会话保存经过治理的用户/任务事实。

两者都在“给模型提供上下文”，但生命周期、可信度、权限和更新机制完全不同。

## 学习目标

完成后应能够：

1. 设计从文档采集、Chunking、索引、检索、融合到引用的 RAG 流水线。
2. 区分 Sparse / Dense / Hybrid Search，以及 Reranking 在候选集中的作用。
3. 使用 Recall@k、MRR 等指标先评测 Retrieval，再评测最终答案。
4. 设计可追踪的 Citation / Provenance，避免“模型说来源存在”就当作引用成立。
5. 区分 Context、State、Memory 与 Knowledge，并正确处理记忆更正、删除和冲突。

## 课程导航

| 讲次 | 核心问题 | 产出 |
|---|---|---|
| [05.1 RAG 系统边界](01-rag-system.md) | 什么情况下需要 RAG？ | RAG 数据流图 |
| [05.2 Chunking、Metadata 与 Provenance](02-chunking-provenance.md) | 文档如何变成可检索证据？ | Chunk Schema |
| [05.3 Sparse、Dense、Hybrid 与 Rerank](03-hybrid-retrieval.md) | 为什么一种检索方法不够？ | Hybrid Search 设计 |
| [05.4 Retrieval Evals](04-retrieval-evals.md) | 如何知道检索真的变好了？ | Gold Dataset + 指标 |
| [05.5 Memory 与 State](05-memory-and-state.md) | 什么应该被长期记住？ | Memory Policy |
| [Lab 03](../../labs/lab-03-rag-memory.md) | 建立可评测的小型混合检索与版本化记忆 | 代码、测试、评测报告 |

## 可运行实验

~~~bash
python3 examples/rag_hybrid_lab.py
python3 examples/versioned_memory.py
python3 -m unittest tests.test_rag_hybrid_lab -v
python3 -m unittest tests.test_versioned_memory -v
~~~

基础实验只使用 Python 标准库和虚构文档，不调用任何模型 API。这样可以先独立验证检索、融合、引用和记忆更新逻辑。

## 关键原则

- RAG 失败首先可能是**没检索到**，不一定是生成模型“不够聪明”。
- Top-k 越大不一定越好；更多无关上下文可能增加成本和干扰。
- Embedding 能找语义相似，Sparse Search 更擅长精确代码、ID 和术语；应按数据集评测组合效果。
- Chunk 是检索单位，不是原始事实来源；必须保留 document_id、source_uri、section、版本等 Provenance。
- “长期记忆”不是把全部聊天永久塞进 Prompt；记忆需要写入策略、更正、删除、时间与来源。
- 外部检索结果和长期记忆都属于**数据**，不能提升成系统权限。

当前产品实现会持续演进；概念和实验优先使用可复现的自建小数据集，托管 Retrieval API 只作为扩展阅读。

[返回课程首页](../../README.md)