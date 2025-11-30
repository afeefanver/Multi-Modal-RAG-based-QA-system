from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter

class SmartChunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def chunk_text(self, chunks: List[Dict]) -> List[Dict]:
        """Apply semantic chunking to text"""
        chunked = []
        
        for chunk in chunks:
            if chunk['type'] == 'text' and len(chunk['content']) > 1000:
                # Split long text
                splits = self.text_splitter.split_text(chunk['content'])
                for idx, split in enumerate(splits):
                    chunked.append({
                        **chunk,
                        'content': split,
                        'metadata': {
                            **chunk['metadata'],
                            'chunk_id': idx
                        }
                    })
            else:
                chunked.append(chunk)
        
        return chunked
    
    def add_context(self, chunks: List[Dict]) -> List[Dict]:
        """Add surrounding context to chunks"""
        for i, chunk in enumerate(chunks):
            # Add previous and next chunk content as context
            context = []
            if i > 0 and chunks[i-1]['page'] == chunk['page']:
                context.append(f"Previous: {chunks[i-1]['content'][:100]}...")
            if i < len(chunks)-1 and chunks[i+1]['page'] == chunk['page']:
                context.append(f"Next: {chunks[i+1]['content'][:100]}...")
            
            chunk['metadata']['context'] = " | ".join(context)
        
        return chunks