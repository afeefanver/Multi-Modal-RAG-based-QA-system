from typing import List, Dict
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import pickle

class MultiModalEmbedder:
    def __init__(self, use_openai: bool = False):  # Changed default to False
        """Initialize embedder with FREE local model"""
        
        # Always use local embeddings (free)
        print("Using FREE local embeddings (Sentence Transformers)")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384
        
        # Initialize FAISS
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.metadatas = []
        
        # Try to load existing index
        self.index_path = "./faiss_index"
        self.load_index()
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding using FREE local model"""
        return self.model.encode(text).tolist()
    
    def embed_and_store(self, chunks: List[Dict]):
        """Embed all chunks and store in FAISS"""
        embeddings = []
        
        print(f"\nEmbedding {len(chunks)} chunks with local model...")
        
        for idx, chunk in enumerate(chunks):
            # Show progress every 50 chunks
            if (idx + 1) % 50 == 0 or idx == 0:
                print(f"  Progress: {idx + 1}/{len(chunks)} chunks")
            
            # Prepare text for embedding
            if chunk['type'] == 'table':
                text = f"Table: {chunk['content'][:500]}"
            else:
                text = chunk['content'][:1000]  # Limit length
            
            # Get embedding
            try:
                embedding = self.get_embedding(text)
                embeddings.append(embedding)
                
                # Store document and metadata
                self.documents.append(chunk['content'])
                metadata = {
                    'type': chunk['type'],
                    'page': chunk['page'],
                }
                if 'metadata' in chunk:
                    for key, value in chunk['metadata'].items():
                        metadata[key] = value
                
                self.metadatas.append(metadata)
                
            except Exception as e:
                print(f"  Warning: Failed to embed chunk {idx}: {e}")
                continue
        
        # Convert to numpy and add to FAISS
        embeddings_array = np.array(embeddings).astype('float32')
        self.index.add(embeddings_array)
        
        # Save index
        self.save_index()
        
        print(f"✓ Successfully stored {len(embeddings)} chunks\n")
    
    def search(self, query: str, n_results: int = 5) -> Dict:
        """Search for relevant chunks"""
        if len(self.documents) == 0:
            raise ValueError(
                "No documents in index!\n"
                "Please run: python pipeline.py"
            )
        
        query_embedding = self.get_embedding(query)
        query_array = np.array([query_embedding]).astype('float32')
        
        # Search
        distances, indices = self.index.search(query_array, n_results)
        
        # Prepare results
        results = {
            'documents': [self.documents[i] for i in indices[0]],
            'metadatas': [self.metadatas[i] for i in indices[0]],
            'distances': distances[0].tolist()
        }
        
        return results
    
    def save_index(self):
        """Save FAISS index and metadata"""
        os.makedirs(self.index_path, exist_ok=True)
        
        faiss.write_index(self.index, f"{self.index_path}/index.faiss")
        
        with open(f"{self.index_path}/documents.pkl", 'wb') as f:
            pickle.dump(self.documents, f)
        
        with open(f"{self.index_path}/metadatas.pkl", 'wb') as f:
            pickle.dump(self.metadatas, f)
    
    def load_index(self):
        """Load existing FAISS index"""
        try:
            index_file = f"{self.index_path}/index.faiss"
            docs_file = f"{self.index_path}/documents.pkl"
            meta_file = f"{self.index_path}/metadatas.pkl"
            
            if os.path.exists(index_file):
                self.index = faiss.read_index(index_file)
                
                with open(docs_file, 'rb') as f:
                    self.documents = pickle.load(f)
                
                with open(meta_file, 'rb') as f:
                    self.metadatas = pickle.load(f)
                
                print(f"✓ Loaded existing index with {len(self.documents)} documents")
        except Exception as e:
            print(f"No existing index found. Will create new one.")