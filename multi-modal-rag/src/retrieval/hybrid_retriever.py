from typing import List, Dict
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    def __init__(self, embedder, alpha: float = 0.5):
        """
        alpha: weight for dense retrieval (1-alpha for sparse)
        """
        self.embedder = embedder
        self.alpha = alpha
        self.bm25 = None
        self.corpus = []
        self.metadata = []
    
    def build_bm25_index(self, chunks: List[Dict]):
        """Build BM25 index for sparse retrieval"""
        self.corpus = [chunk['content'] for chunk in chunks]
        self.metadata = [chunk['metadata'] for chunk in chunks]
        
        tokenized_corpus = [doc.lower().split() for doc in self.corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """Hybrid search combining dense and sparse retrieval"""
        
        # Dense retrieval (vector search)
        dense_results = self.embedder.search(query, n_results=n_results*2)
        
        # Sparse retrieval (BM25)
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        
        # Normalize scores
        dense_scores = np.array(dense_results['distances'])
        dense_scores = 1 / (1 + dense_scores)  # Convert distance to similarity
        
        bm25_scores_norm = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min() + 1e-10)
        
        # Combine scores
        combined_scores = self.alpha * dense_scores + (1 - self.alpha) * bm25_scores_norm[:len(dense_scores)]
        
        # Get top results
        top_indices = np.argsort(combined_scores)[-n_results:][::-1]
        
        final_results = {
            'documents': [dense_results['documents'][i] for i in top_indices],
            'metadatas': [dense_results['metadatas'][i] for i in top_indices],
            'distances': [1 - combined_scores[i] for i in top_indices]
        }
        
        return final_results