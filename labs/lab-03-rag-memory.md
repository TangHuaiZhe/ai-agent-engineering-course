# Lab 03｜构建可评测的 Hybrid Retrieval 与版本化 Memory

**对应 Module 05** · 推荐 4–6 小时 · 无需模型 API Key。

## 实验目标

建立一个小型 RAG Retrieval 基座，并证明：

1. Sparse Search 在精确术语上有优势。
2. “语义检索”能够补充同义表达（课程用确定性教学模拟器）。
3. RRF Hybrid 能融合不同排名。
4. Retrieval 必须用 Gold Cases 评测。
5. Citation 只能引用实际检索到的结果。
6. 长期 Memory 的更正必须 supersede 旧事实，删除后不能继续返回。

## Part A：运行 Hybrid Retrieval

~~~bash
python3 examples/rag_hybrid_lab.py
python3 -m unittest tests.test_rag_hybrid_lab -v
~~~

知识库是虚构的课程文档。代码实现：
- 一个简化 BM25；
- 一个基于显式同义词展开的“semantic-like”教学 Retriever；
- Reciprocal Rank Fusion；
- Recall@k 与 MRR；
- Citation ID 验证。

**semantic-like Retriever 不是 Embedding。** 它只是用确定性方式制造“词面不同但语义接近”的候选，帮助理解 Hybrid 机制。进阶部分再替换成真实 Embedding API。

## Part B：扩展 Gold Dataset

增加至少 10 条 Query：

- 2 条精确错误码 / SKU / API 名。
- 2 条同义表达。
- 2 条需要多个证据。
- 2 条无答案问题。
- 1 条过期文档。
- 1 条不允许当前用户访问的文档。

比较 sparse / semantic / hybrid 的 Recall@3、MRR。不能只展示 Hybrid 赢的案例。

## Part C：真实 Embedding（选做）

任选一个可授权使用的 Embedding Provider，将 \`semantic_like_search()\` 替换成真实向量搜索。记录：

- Model ID / 日期；
- Chunking 方法；
- Similarity；
- Top-k；
- Token/费用；
- 与确定性 baseline 的同一 Gold Set 指标。

如果使用 OpenAI 托管 Retrieval，可以比较其 semantic / hybrid 配置与本地 Sparse baseline。不要把官方默认 Chunk 参数当作你的业务最优参数。

## Part D：Citation Gate

系统返回 answer 前，先检查引用的 \`doc_id\` 是否属于本次 Retrieval Results。增加：
- 合法 citation；
- 模型捏造 citation；
- 引用存在于知识库但本次没有检索到。

后两者必须拒绝。

## Part E：Memory

~~~bash
python3 examples/versioned_memory.py
python3 -m unittest tests.test_versioned_memory -v
~~~

完成：
- 只允许 trusted source 写入；
- 同 key 新值 supersede 旧版本；
- current() 只返回 active；
- delete 后 current() 返回 None；
- history 保留状态用于教学审计。

## 验收

| 项目 | 分值 |
|---|---:|
| 能解释 Sparse / Dense / Hybrid / Rerank 差别 | 20 |
| Gold Dataset 与 Retrieval 指标 | 25 |
| Citation Gate | 20 |
| Memory Update / Delete / Source Policy | 20 |
| 扩展实验与失败案例复盘 | 15 |

## 生产差距

本 Lab 没有数据库、向量索引、真实 ACL、并发写入、加密删除或真实 Embedding。生产系统必须将 Tenant / ACL 过滤前置，并为索引重建、版本迁移和删除设计完整生命周期。

[返回 Module 05](../modules/05-rag-memory/README.md)