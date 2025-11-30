from typing import List, Dict
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class QAGenerator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found!")
        
        self.client = OpenAI(api_key=api_key)
        
        # Use GPT-3.5-turbo (cheaper and more widely available)
        # You can change this to gpt-4o or gpt-4o-mini if you have access
        self.model = "gpt-3.5-turbo"
    
    def generate_answer(self, query: str, retrieved_chunks: Dict) -> Dict:
        """Generate answer with citations"""
        
        # Prepare context from retrieved chunks
        context_parts = []
        for idx, (doc, meta) in enumerate(zip(
            retrieved_chunks['documents'],
            retrieved_chunks['metadatas']
        )):
            context_parts.append(
                f"[Source {idx+1}, Page {meta['page']}, Type: {meta['type']}]\n{doc}\n"
            )
        
        context = "\n".join(context_parts)
        
        # Create prompt
        prompt = f"""You are an expert analyst answering questions about Qatar's economy based on an IMF Article IV report.

Context from the document:
{context}

Question: {query}

Instructions:
1. Answer the question based ONLY on the provided context
2. Cite your sources using [Source X, Page Y] format
3. If the context doesn't contain enough information, say so
4. Be precise with numbers and dates
5. Structure your answer clearly

Answer:"""
        
        # Generate answer
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful financial analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            answer_text = response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating answer: {e}")
            answer_text = f"Error: {str(e)}\n\nRetrieved context:\n" + "\n".join([
                f"Source {i+1} (Page {meta['page']}): {doc[:200]}..."
                for i, (doc, meta) in enumerate(zip(retrieved_chunks['documents'], retrieved_chunks['metadatas']))
            ])
        
        # Extract sources
        sources = []
        for idx, meta in enumerate(retrieved_chunks['metadatas']):
            sources.append({
                'source_id': idx + 1,
                'page': meta['page'],
                'type': meta['type'],
                'relevance': 1.0 - retrieved_chunks['distances'][idx]
            })
        
        return {
            'answer': answer_text,
            'sources': sources,
            'context_used': len(retrieved_chunks['documents'])
        }