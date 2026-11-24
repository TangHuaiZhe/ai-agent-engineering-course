# 05.2｜Chunking、Metadata 与 Provenance：不要切完文本就丢掉文档身份

## 1. Chunk 为什么重要？

检索系统通常不是直接给整篇文档打分，而是对 Chunk 建索引。Chunk 太大：
- 检索粒度粗，命中一个段落可能带入大量噪声；
- Token 成本增加。

Chunk 太小：
- 公司名、时间、章节标题可能被切掉；
- 单独看一句“增长 12%”时，不知道是谁、哪一年、什么指标。

不存在对所有数据都最佳的固定 Chunk Size。应根据文档结构和检索 Gold Set 实验。

## 2. 优先使用语义边界

典型切分优先级：

1. 文档 / 页面 / Heading。
2. 段落、列表、表格等自然单元。
3. 长度达到上限后再按句子或 Token 切分。
4. 必要时添加有限 Overlap。

技术手册适合保留标题；财报应保留报告期、公司名与表格上下文；代码检索应避免把函数签名和函数体切开。

## 3. Chunk Schema

至少保留：

~~~json
{
  "chunk_id": "doc-17#section-4#chunk-2",
  "document_id": "doc-17",
  "text": "...",
  "title": "Revenue Recognition",
  "source_uri": "https://...",
  "published_at": "2026-03-15",
  "version": "sha256:...",
  "access_scope": "public",
  "ordinal": 2
}
~~~

检索结果应该能从 chunk 回到**原始文档和版本**。

## 4. Provenance 比 Citation 字符串重要

模型输出：

> “收入增长 12% [来源 3]”

只有在系统能够证明“来源 3”对应真实检索结果，并且该 Chunk 真的包含这个事实时，这个 Citation 才有价值。

建议将：
- Retrieval Result IDs
- Source URI / File ID
- Chunk ID
- 文档版本
- 抽取位置 / page / section

作为结构化数据保留，而不是让模型自由生成 URL。

## 5. Contextual Chunking

有些 Chunk 本身缺乏完整身份。可在索引前为 Chunk 加入短上下文，如“这是 Example Corp 2025 年年报的现金流章节”。这种 Contextual Retrieval 思想可以改善检索，但生成的上下文同样需要版本化，且不能覆盖原始文本。

Anthropic 的公开实验显示，其 Contextual Embeddings + Contextual BM25 在其测试集上降低了 Top-20 Retrieval Failure；这是一项特定实验结果，不代表所有数据集都应照搬相同参数。正确做法仍然是建立自己的 Eval。

## Lab 准备

[Lab 03](../../labs/lab-03-rag-memory.md) 的虚构知识库为每个文档保留 doc_id、title 和文本；后续扩展时请加入发布日期和权限 Scope。

[上一讲](01-rag-system.md) · [下一讲](03-hybrid-retrieval.md)