from src.ingestion.pdf_processor import MultiModalPDFProcessor
from src.chunking.smart_chunker import SmartChunker
from src.embedding.embedder import MultiModalEmbedder
from src.generation.qa_generator import QAGenerator
from config import Config

class RAGPipeline:
    def __init__(self):
        self.config = Config()
        self.embedder = MultiModalEmbedder(use_openai=self.config.USE_OPENAI_EMBEDDINGS)
        self.qa_generator = QAGenerator()
    
    def build_index(self):
        """Build the complete RAG index"""
        print("=" * 50)
        print("Starting Multi-Modal RAG Pipeline")
        print("=" * 50)
        
        # Step 1: Process PDF
        print("\n[1/4] Processing PDF...")
        processor = MultiModalPDFProcessor(self.config.PDF_PATH)
        chunks = processor.process_all()
        
        # Step 2: Smart chunking
        print("\n[2/4] Applying smart chunking...")
        chunker = SmartChunker(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP
        )
        chunks = chunker.chunk_text(chunks)
        chunks = chunker.add_context(chunks)
        
        # Step 3: Embed and store
        print("\n[3/4] Generating embeddings and building index...")
        self.embedder.embed_and_store(chunks)
        
        print("\n[4/4] ✓ Index built successfully!")
        print(f"Total indexed chunks: {len(chunks)}")
        
        return len(chunks)
    
    def query(self, question: str):
        """Query the system"""
        # Retrieve relevant chunks
        retrieved = self.embedder.search(question, n_results=self.config.TOP_K)
        
        # Generate answer with LLM
        result = self.qa_generator.generate_answer(question, retrieved)
        
        return result

if __name__ == "__main__":
    pipeline = RAGPipeline()
    pipeline.build_index()