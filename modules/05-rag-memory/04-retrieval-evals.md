# 05.4｜Retrieval Evals：先证明“找到了”，再评答案写得好不好

## 1. 为什么要拆开评测？

问题：**“移动端明文 HTTP 为什么被拒绝？”**

如果 Agent 回答错了，可能因为：
1. Retrieval 没找到 Android Network Security 文档；
2. 找到了错误版本的资料；
3. 资料正确但被 Rerank 丢掉；
4. 证据已经在 Context 里，生成模型仍解释错误。

只有 Retrieval Gold Set 才能区分 1–3。

## 2. Gold Case

每条 Query 至少记录：

~~~json
{
  "query_id": "q-001",
  "query": "员工休假政策",
  "relevant_doc_ids": ["policy-leave"],
  "forbidden_doc_ids": ["tenant-b-private"],
  "notes": "同义表达，不要求出现年假二字"
}
~~~

不要只写 expected answer；对于检索评测，需要明确**哪些证据算 relevant**。

## 3. 常用指标

### Recall@k

Top-k 是否覆盖了应检索的相关文档：

~~~text
Recall@k = retrieved_relevant / all_relevant
~~~

多证据问题尤其重要。

### Precision@k

~~~text
Precision@k = retrieved_relevant / k
~~~

如果 Top-20 里只有一个有用 Chunk，虽然 Recall 可能够高，但 Context 噪声很大。

### MRR

对于通常只需要一个最关键证据的问题：

~~~text
RR = 1 / first_relevant_rank
MRR = mean(RR)
~~~

排名第 1 比排名第 10 更有价值。

## 4. Citation Validation

答案中的 Citation 应指向：
- 本次实际检索过的 chunk；
- 当前用户有权限的 source；
- 与 claim 对应的文本；
- 正确版本。

至少可以自动验证“Citation ID 是否属于 Retrieval Result”；更深入的“Claim 是否被 Chunk 支持”通常还需要结构化抽取、规则或人工/模型 Judge。

## 5. 比较检索策略

同一 Gold Dataset 下比较：

| Variant | Recall@5 | MRR | 平均候选数 | 延迟 |
|---|---:|---:|---:|---:|
| Sparse | ... | ... | 5 | ... |
| Dense | ... | ... | 5 | ... |
| Hybrid | ... | ... | 5 | ... |
| Hybrid + Rerank | ... | ... | 5 | ... |

**不要用不同 Query Set 比较两个方案。**

## Lab

Lab 03 内置一组小型 Gold Cases。要求你增加至少 10 条边界问题，包括 ID 精确匹配、同义表达、无答案、过期文档与权限过滤。

[上一讲](03-hybrid-retrieval.md) · [下一讲](05-memory-and-state.md)