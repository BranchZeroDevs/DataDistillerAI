"""
Hybrid retriever combining dense (FAISS) and sparse (BM25) results.
"""

from typing import List, Tuple, Dict

from src.retrieval.bm25_index import BM25Index


def _normalize(scores: Dict[int, float]) -> Dict[int, float]:
    if not scores:
        return {}
    values = list(scores.values())
    min_s, max_s = min(values), max(values)
    if max_s == min_s:
        return {k: 1.0 for k in scores}
    return {k: (v - min_s) / (max_s - min_s) for k, v in scores.items()}


class HybridRetriever:
    """Combine dense and BM25 results with weighted merge."""

    def __init__(self, vector_store) -> None:
        self.vector_store = vector_store
        self.bm25 = BM25Index()
        self._indexed_count = -1

    def _ensure_bm25(self) -> None:
        if self.vector_store.document_count != self._indexed_count:
            docs = self.vector_store.get_all_documents_with_ids()
            self.bm25.build(docs)
            self._indexed_count = self.vector_store.document_count

    def dense_search(self, query: str, top_k: int = 5) -> List[Tuple[str, Dict, float]]:
        return self.vector_store.search(query, top_k=top_k)

    def sparse_search(self, query: str, top_k: int = 5) -> List[Tuple[str, Dict, float]]:
        self._ensure_bm25()
        sparse = self.bm25.search(query, top_k=top_k)
        return [(content, metadata, score) for content, metadata, score, _ in sparse]

    def hybrid_search(
        self,
        query: str,
        top_k: int = 5,
        dense_weight: float = 0.5,
        sparse_weight: float = 0.5
    ) -> List[Tuple[str, Dict, float]]:
        self._ensure_bm25()

        dense = self.vector_store.search(query, top_k=top_k * 2)
        sparse = self.bm25.search(query, top_k=top_k * 2)

        dense_scores = {int(d[1].get('doc_id')): float(d[2]) for d in dense if d[1].get('doc_id') is not None}
        sparse_scores = {int(d[3]): float(d[2]) for d in sparse}

        dense_norm = _normalize(dense_scores)
        sparse_norm = _normalize(sparse_scores)

        merged: Dict[int, Dict] = {}

        for content, metadata, score in dense:
            doc_id = metadata.get('doc_id')
            if doc_id is None:
                continue
            merged.setdefault(doc_id, {
                'content': content,
                'metadata': metadata,
                'dense': 0.0,
                'sparse': 0.0
            })
            merged[doc_id]['dense'] = dense_norm.get(doc_id, 0.0)

        for content, metadata, score, doc_id in sparse:
            merged.setdefault(doc_id, {
                'content': content,
                'metadata': metadata,
                'dense': 0.0,
                'sparse': 0.0
            })
            merged[doc_id]['sparse'] = sparse_norm.get(doc_id, 0.0)

        scored = []
        for doc_id, item in merged.items():
            combined = (dense_weight * item['dense']) + (sparse_weight * item['sparse'])
            scored.append((item['content'], item['metadata'], combined))

        scored.sort(key=lambda x: x[2], reverse=True)
        return scored[:top_k]
