"""Dependency-free teaching lab for retrieval evaluation.

This module implements:
- a small BM25 retriever,
- a deterministic "semantic-like" synonym-expansion retriever,
- reciprocal-rank fusion (RRF),
- Recall@k / MRR,
- a citation gate.

The semantic-like retriever is NOT an embedding model. It exists only to make
hybrid retrieval behavior reproducible without network calls or API keys.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+|[\u4e00-\u9fff]")


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    text: str
    access_scope: str = "public"
    current: bool = True


CORPUS: tuple[Document, ...] = (
    Document(
        "android-cleartext",
        "Android 网络安全",
        "Android 应用访问明文 HTTP 时可能被 Network Security Configuration 或平台策略阻止。错误信息可能包含 CLEARTEXT communication not permitted。",
    ),
    Document(
        "webview-security",
        "WebView 安全",
        "WebView 应限制不可信导航，谨慎启用 JavaScript bridge，并避免开放本地文件访问给不可信网页。",
    ),
    Document(
        "leave-policy",
        "员工休假政策",
        "员工每年享有年假；请假需要在系统中提交审批。",
    ),
    Document(
        "error-ts999",
        "错误码 TS-999",
        "TS-999 表示同步任务的认证 Token 已过期，需要重新登录后重试。",
    ),
    Document(
        "rag-old-policy",
        "旧版检索政策",
        "旧版政策要求所有检索只使用关键词匹配。",
        current=False,
    ),
    Document(
        "rag-current-policy",
        "当前检索政策",
        "当前政策允许关键词检索与语义检索结合，并要求对结果进行评测。",
    ),
    Document(
        "tenant-b-private",
        "租户 B 私有文档",
        "租户 B 的内部密码轮换流程。",
        access_scope="tenant-b",
    ),
)

# Teaching-only synonym map used by semantic_like_search. This is intentionally
# transparent so students can see exactly why a result matched.
SYNONYMS: dict[str, tuple[str, ...]] = {
    "vacation": ("休假", "年假", "请假"),
    "holiday": ("休假", "年假"),
    "明文": ("cleartext", "http"),
    "cleartext": ("明文", "http"),
    "认证": ("auth", "authentication", "token"),
    "authentication": ("认证", "token"),
    "hybrid": ("关键词", "语义", "混合"),
    "混合": ("hybrid", "关键词", "语义"),
}


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def visible_documents(
    documents: Iterable[Document],
    *,
    scopes: frozenset[str] = frozenset({"public"}),
    current_only: bool = True,
) -> list[Document]:
    return [
        doc
        for doc in documents
        if doc.access_scope in scopes and (doc.current or not current_only)
    ]


def bm25_search(
    query: str,
    documents: Iterable[Document],
    *,
    top_k: int = 5,
    scopes: frozenset[str] = frozenset({"public"}),
    current_only: bool = True,
    k1: float = 1.5,
    b: float = 0.75,
) -> list[tuple[str, float]]:
    docs = visible_documents(documents, scopes=scopes, current_only=current_only)
    if top_k <= 0 or not docs:
        return []
    tokenized = [tokenize(doc.title + " " + doc.text) for doc in docs]
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    avg_len = sum(map(len, tokenized)) / len(tokenized)
    doc_freq: Counter[str] = Counter()
    for tokens in tokenized:
        doc_freq.update(set(tokens))

    scored: list[tuple[str, float]] = []
    n_docs = len(docs)
    for doc, tokens in zip(docs, tokenized):
        tf = Counter(tokens)
        score = 0.0
        for term in query_tokens:
            if term not in tf:
                continue
            df = doc_freq[term]
            idf = math.log(1 + (n_docs - df + 0.5) / (df + 0.5))
            numerator = tf[term] * (k1 + 1)
            denominator = tf[term] + k1 * (1 - b + b * len(tokens) / avg_len)
            score += idf * numerator / denominator
        if score > 0:
            scored.append((doc.doc_id, score))
    return sorted(scored, key=lambda item: (-item[1], item[0]))[:top_k]


def semantic_like_search(
    query: str,
    documents: Iterable[Document],
    *,
    top_k: int = 5,
    scopes: frozenset[str] = frozenset({"public"}),
    current_only: bool = True,
) -> list[tuple[str, float]]:
    """Deterministic teaching stand-in for semantic retrieval.

    It expands explicit synonym aliases and scores token overlap. It must never
    be reported as an embedding benchmark.
    """
    docs = visible_documents(documents, scopes=scopes, current_only=current_only)
    if top_k <= 0:
        return []
    query_lower = query.lower()
    expanded: set[str] = set(tokenize(query))
    semantic_terms: set[str] = set(expanded)
    for key, aliases in SYNONYMS.items():
        if key.lower() in query_lower or key.lower() in expanded:
            semantic_terms.add(key.lower())
            semantic_terms.update(term.lower() for term in aliases)
    if not semantic_terms:
        return []

    scored: list[tuple[str, float]] = []
    for doc in docs:
        haystack = (doc.title + " " + doc.text).lower()
        doc_tokens = set(tokenize(haystack))
        exact_overlap = semantic_terms & doc_tokens
        substring_matches = {term for term in semantic_terms if term and term in haystack}
        matches = exact_overlap | substring_matches
        if matches:
            score = len(matches) / math.sqrt(max(1, len(doc_tokens)))
            scored.append((doc.doc_id, score))
    return sorted(scored, key=lambda item: (-item[1], item[0]))[:top_k]


def reciprocal_rank_fusion(
    *ranked_lists: list[tuple[str, float]],
    top_k: int = 5,
    rrf_k: int = 60,
) -> list[tuple[str, float]]:
    if top_k <= 0 or rrf_k <= 0:
        return []
    scores: Counter[str] = Counter()
    for ranked in ranked_lists:
        for rank, (doc_id, _score) in enumerate(ranked, start=1):
            scores[doc_id] += 1.0 / (rrf_k + rank)
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:top_k]


def hybrid_search(
    query: str,
    documents: Iterable[Document] = CORPUS,
    *,
    top_k: int = 5,
    scopes: frozenset[str] = frozenset({"public"}),
    current_only: bool = True,
) -> list[tuple[str, float]]:
    sparse = bm25_search(
        query, documents, top_k=max(top_k, 5), scopes=scopes, current_only=current_only
    )
    semantic = semantic_like_search(
        query, documents, top_k=max(top_k, 5), scopes=scopes, current_only=current_only
    )
    return reciprocal_rank_fusion(sparse, semantic, top_k=top_k)


def recall_at_k(results: Iterable[str], relevant: frozenset[str], k: int) -> float:
    if not relevant:
        return 1.0
    if k <= 0:
        return 0.0
    top = set(list(results)[:k])
    return len(top & relevant) / len(relevant)


def reciprocal_rank(results: Iterable[str], relevant: frozenset[str]) -> float:
    for rank, doc_id in enumerate(results, start=1):
        if doc_id in relevant:
            return 1.0 / rank
    return 0.0


def mean_reciprocal_rank(cases: Iterable[tuple[list[str], frozenset[str]]]) -> float:
    values = [reciprocal_rank(results, relevant) for results, relevant in cases]
    return sum(values) / len(values) if values else 0.0


def validate_citations(
    citation_ids: Iterable[str],
    retrieved_ids: Iterable[str],
) -> tuple[bool, tuple[str, ...]]:
    retrieved = set(retrieved_ids)
    invalid = tuple(sorted(set(citation_ids) - retrieved))
    return not invalid, invalid


def _ids(ranked: list[tuple[str, float]]) -> list[str]:
    return [doc_id for doc_id, _score in ranked]


if __name__ == "__main__":
    for query in ("TS-999 怎么处理？", "vacation approval", "明文网络为什么被拒绝？"):
        sparse = bm25_search(query, CORPUS, top_k=3)
        semantic = semantic_like_search(query, CORPUS, top_k=3)
        hybrid = reciprocal_rank_fusion(sparse, semantic, top_k=3)
        print(query)
        print("  sparse :", _ids(sparse))
        print("  semantic-like:", _ids(semantic))
        print("  hybrid :", _ids(hybrid))
