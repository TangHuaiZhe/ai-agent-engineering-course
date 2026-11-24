# 05.3｜Sparse、Dense、Hybrid Search 与 Reranking

## 1. Sparse Search：精确词很强

BM25 等 Sparse / Lexical Search 根据词项出现情况打分。它特别适合：

- 错误码：\`ERR_AUTH_481\`
- API 类名：\`WebViewClient\`
- 产品 SKU / 股票代码 / 文件 ID
- 人名、术语和版本号

缺点是用户换一种表达方式时，可能完全没有词面重合。

## 2. Dense Search：语义相似

Embedding 将 Query 与 Chunk 表示为向量，通过 Cosine / Dot Product 等相似度找语义相关文本。它能找出“员工休假政策”和“年假规则”这类词面不同但概念接近的内容。

但 Dense Retrieval 也可能：
- 漏掉非常具体的字符串；
- 把主题相似但事实无关的文档排得很高；
- 受 Embedding Model、语言和领域影响。

## 3. Hybrid Search：两个候选集融合

常见做法：

~~~text
sparse_results = BM25(query, top_n)
dense_results  = EmbeddingSearch(query, top_n)
candidates = ReciprocalRankFusion(sparse_results, dense_results)
final = rerank(query, candidates)[:k]
~~~

RRF（Reciprocal Rank Fusion）只使用排名，不要求两个系统分数在同一尺度：

~~~text
RRF_score(d) = Σ 1 / (k_rrf + rank_i(d))
~~~

课程实验使用简化 BM25 + 教学用“语义别名检索”模拟 Dense 的互补行为，避免 API 依赖。它**不是 Embedding 的实现或性能替代物**。

## 4. Reranking

第一阶段 Retrieval 更关注“不要漏”，可以取较大候选集；Reranker 再对 Query–Chunk 相关性精排，将较少结果交给生成模型。

Reranking 会增加延迟和费用，因此应比较：
- Top-N 候选数；
- Rerank 后 Top-K；
- Recall@K；
- 最终答案成功率；
- 端到端延迟和成本。

## 5. Metadata Filter 应该在正确阶段使用

例如用户只允许访问 \`tenant=A\`，权限过滤不应依靠 Reranker 把其它 Tenant 排到后面，而要在检索前/检索时**彻底排除无权结果**。

日期、语言、文档类型常适合 Metadata Filter；而“是否与问题相关”属于 Ranking 问题。

## 实验

运行：

~~~bash
python3 examples/rag_hybrid_lab.py
~~~

观察 exact-code 查询与 paraphrase 查询在 sparse、semantic、hybrid 三种模式下的排名差异。

参考：OpenAI Retrieval 当前支持语义搜索、查询改写、属性过滤以及 Hybrid Ranking 配置；具体 API 和 ranker 名称是版本相关细节。

[上一讲](02-chunking-provenance.md) · [下一讲](04-retrieval-evals.md)