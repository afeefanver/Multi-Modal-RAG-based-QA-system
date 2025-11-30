import streamlit as st
from pipeline import RAGPipeline
import time

st.set_page_config(
    page_title="Multi-Modal RAG QA System",
    page_icon="📊",
    layout="wide"
)

@st.cache_resource
def load_pipeline():
    return RAGPipeline()

def main():
    st.title("📊 Multi-Modal Document Intelligence System")
    st.markdown("**RAG-Based QA for Qatar IMF Article IV Report**")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ System Status")
        
        if st.button("🔄 Rebuild Index"):
            with st.spinner("Building index..."):
                pipeline = load_pipeline()
                chunks = pipeline.build_index()
                st.success(f"✓ Indexed {chunks} chunks")
        
        st.divider()
        
        st.header("📈 System Info")
        st.metric("Vector DB", "ChromaDB")
        st.metric("LLM Model", "GPT-3.5")
        st.metric("Embeddings", "OpenAI")
    
    # Main interface
    pipeline = load_pipeline()
    
    # Sample questions
    st.subheader("💡 Try these questions:")
    sample_questions = [
        "What was Qatar's GDP growth in 2023?",
        "What are the key fiscal policy recommendations?",
        "What is Qatar's debt sustainability outlook?",
        "What are the main risks to the economic outlook?",
        "What is the Third National Development Strategy (NDS3)?"
    ]
    
    cols = st.columns(3)
    for idx, q in enumerate(sample_questions):
        if cols[idx % 3].button(q, key=f"sample_{idx}"):
            st.session_state.question = q
    
    # Query input
    st.divider()
    question = st.text_area(
        "Ask a question about Qatar's economy:",
        value=st.session_state.get('question', ''),
        height=100,
        placeholder="e.g., What was Qatar's fiscal surplus in 2023?"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    if search_button and question:
        with st.spinner("Searching and generating answer..."):
            start_time = time.time()
            
            try:
                result = pipeline.query(question)
                latency = time.time() - start_time
                
                # Display answer
                st.success("✓ Answer generated")
                
                st.subheader("📝 Answer:")
                st.write(result['answer'])
                
                # Display sources
                st.subheader("📚 Sources:")
                for source in result['sources']:
                    with st.expander(f"Source {source['source_id']} - Page {source['page']} ({source['type']})"):
                        st.metric("Relevance", f"{source['relevance']*100:.1f}%")
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Response Time", f"{latency:.2f}s")
                col2.metric("Sources Used", result['context_used'])
                col3.metric("Confidence", "High")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
