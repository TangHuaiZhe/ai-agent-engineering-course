import unittest

from examples.rag_hybrid_lab import (
    CORPUS,
    bm25_search,
    hybrid_search,
    mean_reciprocal_rank,
    recall_at_k,
    reciprocal_rank,
    reciprocal_rank_fusion,
    semantic_like_search,
    validate_citations,
)


def ids(results):
    return [doc_id for doc_id, _score in results]


class TestRAGHybridLab(unittest.TestCase):
    def test_sparse_exact_error_code(self):
        self.assertEqual(ids(bm25_search("TS-999", CORPUS, top_k=1)), ["error-ts999"])

    def test_sparse_misses_english_vacation_synonym(self):
        self.assertNotIn("leave-policy", ids(bm25_search("vacation", CORPUS, top_k=3)))

    def test_semantic_like_vacation_synonym(self):
        self.assertEqual(
            ids(semantic_like_search("vacation approval", CORPUS, top_k=1)),
            ["leave-policy"],
        )

    def test_semantic_like_chinese_phrase_alias(self):
        self.assertIn(
            "android-cleartext",
            ids(semantic_like_search("cleartext 为什么被拒绝", CORPUS, top_k=3)),
        )

    def test_hybrid_finds_leave_policy(self):
        self.assertIn("leave-policy", ids(hybrid_search("vacation approval", top_k=3)))

    def test_private_document_filtered_by_default(self):
        result_ids = ids(hybrid_search("密码轮换", top_k=10))
        self.assertNotIn("tenant-b-private", result_ids)

    def test_private_document_visible_only_with_scope(self):
        result_ids = ids(
            hybrid_search(
                "密码轮换", top_k=10, scopes=frozenset({"public", "tenant-b"})
            )
        )
        self.assertIn("tenant-b-private", result_ids)

    def test_old_document_filtered_by_default(self):
        self.assertNotIn("rag-old-policy", ids(hybrid_search("检索政策", top_k=10)))

    def test_old_document_can_be_requested_for_history(self):
        result_ids = ids(hybrid_search("关键词匹配", top_k=10, current_only=False))
        self.assertIn("rag-old-policy", result_ids)

    def test_rrf_rewards_presence_in_two_lists(self):
        fused = reciprocal_rank_fusion(
            [("a", 0.9), ("b", 0.8)],
            [("b", 0.7), ("c", 0.6)],
            top_k=3,
        )
        self.assertEqual(fused[0][0], "b")

    def test_recall_at_k(self):
        self.assertEqual(recall_at_k(["a", "b"], frozenset({"b", "c"}), 2), 0.5)

    def test_empty_relevant_set_has_full_recall_by_convention(self):
        self.assertEqual(recall_at_k(["a"], frozenset(), 1), 1.0)

    def test_reciprocal_rank(self):
        self.assertEqual(reciprocal_rank(["x", "target"], frozenset({"target"})), 0.5)

    def test_mean_reciprocal_rank(self):
        score = mean_reciprocal_rank(
            [(["a"], frozenset({"a"})), (["x", "b"], frozenset({"b"}))]
        )
        self.assertEqual(score, 0.75)

    def test_valid_citations(self):
        self.assertEqual(
            validate_citations(["a", "b"], ["a", "b", "c"]),
            (True, ()),
        )

    def test_fabricated_citation_rejected(self):
        self.assertEqual(
            validate_citations(["a", "invented"], ["a", "b"]),
            (False, ("invented",)),
        )

    def test_existing_but_not_retrieved_citation_rejected(self):
        self.assertEqual(
            validate_citations(["webview-security"], ["android-cleartext"]),
            (False, ("webview-security",)),
        )

    def test_nonpositive_top_k_returns_empty(self):
        self.assertEqual(bm25_search("TS-999", CORPUS, top_k=0), [])
        self.assertEqual(semantic_like_search("vacation", CORPUS, top_k=0), [])

    def test_blank_query_returns_empty(self):
        self.assertEqual(bm25_search("   ", CORPUS), [])
        self.assertEqual(semantic_like_search("   ", CORPUS), [])


if __name__ == "__main__":
    unittest.main()
