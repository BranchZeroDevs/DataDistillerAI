"""
BM25 sparse retrieval index
"""

from typing import List, Dict, Tuple
import re

from rank_bm25 import BM25Okapi


def _tokenize(text: str) -> List[str]:
    return re.findall(r"\w+", text.lower())


class BM25Index:
    """Simple BM25 index over document chunks."""

    def __init__(self) -> None:
        self._bm25 = None
        self._documents: List[Dict] = []

    def build(self, documents: List[Dict]) -> None:
        """
        Build BM25 index.

        documents: list of {doc_id, content, metadata}
        """
        self._documents = documents
        tokenized = [_tokenize(doc.get('content', '')) for doc in documents]
        self._bm25 = BM25Okapi(tokenized) if tokenized else None

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, Dict, float, int]]:
        """
        Return list of (content, metadata, score, doc_id).
        """
        if not self._bm25 or not self._documents:
            return []

        scores = self._bm25.get_scores(_tokenize(query))
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for i in ranked:
            doc = self._documents[i]
            results.append((
                doc.get('content', ''),
                dict(doc.get('metadata', {}) or {}),
                float(scores[i]),
                int(doc.get('doc_id', i))
            ))

        return results
