"""
DataDistillerAI - Quick Start Web UI
Lightweight version - faster startup, documents indexed on-demand
"""

import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os
import time

# Load environment
load_dotenv(Path('.env'))

# Page config
st.set_page_config(
    page_title="DataDistillerAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧠 DataDistillerAI")
st.markdown("*Intelligent Document Q&A with Multiple LLM Backends*")

# Sidebar
st.sidebar.title("⚙️ Configuration")

st.sidebar.success("🚀 **Primary Backend:** Ollama (Local, Free)")

with st.sidebar.expander("⚙️ Advanced (Code-only backends)"):
    st.write("Secondary options for development:")
    st.write("- Claude (Cloud)\n- Gemini (Cloud)")
    st.write("Edit code to switch backends.")

# Always use Ollama
selected_backend = "ollama"

# Initialize pipeline - Primary: Ollama (without indexing on startup)
@st.cache_resource
def load_pipeline(backend_name="ollama"):
    """Load RAG pipeline. Primary backend is Ollama (local, free).
    
    Secondary options available in code:
    - claude: RAGPipelineClaude
    - gemini: RAGPipelineGemini
    """
    try:
        if backend_name == "ollama":
            from src.workflows_ollama import RAGPipelineOllama
            return RAGPipelineOllama()
        elif backend_name == "claude":
            # Secondary option - requires ANTHROPIC_API_KEY
            from src.workflows_claude import RAGPipelineClaude
            return RAGPipelineClaude()
        elif backend_name == "gemini":
            # Secondary option - requires GOOGLE_API_KEY
            from src.workflows_gemini import RAGPipelineGemini
            return RAGPipelineGemini()
        else:
            raise ValueError(f"Unknown backend: {backend_name}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Load pipeline - always Ollama for primary
pipeline = load_pipeline("ollama")

if pipeline is None:
    st.error("Could not initialize backend. Check API keys.")
    st.stop()

# Index status
if "indexed" not in st.session_state:
    st.session_state.indexed = False

# Tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Documents", "ℹ️ About"])

# TAB 1: CHAT
with tab1:
    st.header("Ask Questions About Your Documents")
    
    # Index if not done
    if not st.session_state.indexed:
        with st.spinner("📚 Indexing documents (first time only)..."):
            try:
                pipeline.index_documents()
                st.session_state.indexed = True
                st.success("✓ Documents indexed!")
            except Exception as e:
                st.error(f"Error indexing: {str(e)}")
                st.stop()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_question = st.text_input(
            "Your question:",
            placeholder="What would you like to know?",
            label_visibility="collapsed"
        )
        # Quick test button to verify pipeline + UI connectivity
        if st.button("Quick Test (Hello)"):
            test_query = "Hello"
            with st.spinner("🔍 Running quick test..."):
                try:
                    if not st.session_state.indexed:
                        pipeline.index_documents()
                        st.session_state.indexed = True
                    answer = pipeline.query(test_query, top_k=top_k)
                    st.markdown("### Quick Test Answer")
                    st.markdown(answer)

                    with st.expander("📎 Context Used"):
                        results = pipeline.vector_store.search(test_query, top_k=top_k)
                        for i, (content, metadata, score) in enumerate(results, 1):
                            st.markdown(f"**[{i}]** Relevance: {score:.1%}")
                            st.text(content[:250] + "..." if len(content) > 250 else content)
                            st.divider()
                except Exception as e:
                    st.error(f"Quick test error: {str(e)}")
    
    with col2:
        top_k = st.slider("Results", 1, 5, 3, label_visibility="collapsed")
    
    if user_question:
        with st.spinner("🔍 Thinking..."):
            try:
                answer = pipeline.query(user_question, top_k=top_k)
                st.markdown("### Answer")
                st.markdown(answer)
                
                with st.expander("📎 Context Used"):
                    results = pipeline.vector_store.search(user_question, top_k=top_k)
                    for i, (content, metadata, score) in enumerate(results, 1):
                        st.markdown(f"**[{i}]** Relevance: {score:.1%}")
                        st.text(content[:250] + "..." if len(content) > 250 else content)
                        st.divider()
            except Exception as e:
                st.error(f"Error: {str(e)}")

# TAB 2: DOCUMENTS
with tab2:
    st.header("Document Information")
    
    if not st.session_state.indexed:
        st.info("Index documents first by asking a question in the Chat tab")
    else:
        try:
            docs = pipeline.loader.load_directory(str(pipeline.document_path))
            chunks = pipeline.vector_store.get_all_documents()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Documents", len(docs))
            with col2:
                st.metric("Chunks", len(chunks))
            with col3:
                total_chars = sum(len(d.content) for d in docs)
                st.metric("Total Characters", f"{total_chars:,}")
            
            st.markdown("---")
            st.subheader("📄 Indexed Documents")
            
            for doc in docs:
                with st.expander(f"📖 {doc.metadata.get('filename', 'Unknown')}"):
                    st.write(f"Size: {len(doc.content):,} characters")
                    st.text(doc.content[:400] + "..." if len(doc.content) > 400 else doc.content)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")

# TAB 3: ABOUT
with tab3:
    st.header("About DataDistillerAI")
    
    st.markdown("""
    ### 🎯 What is DataDistillerAI?
    
    A Retrieval-Augmented Generation (RAG) system for intelligent document Q&A.
    
    ### ⚡ Quick Start
    
    1. Type a question in the **Chat** tab
    2. Documents auto-index (first time takes ~30 seconds)
    3. Get instant answers grounded in your documents
    
    ### � Primary Backend: Ollama
    
    - **Type**: Local (100% privacy)
    - **Cost**: Completely FREE
    - **Speed**: ⚡⚡⚡
    - **Quality**: ⭐⭐⭐⭐
    
    **Secondary backends available in code:**
    - Claude (Cloud)
    - Gemini (Cloud)
    
    ### 📚 Tech Stack
    
    - **LLM**: Ollama (primary), Claude & Gemini (secondary)
    - **Vector DB**: FAISS with sentence-transformers
    - **UI**: Streamlit
    - **Document Support**: PDF, DOCX, TXT, HTML, Markdown
    
    ### 📖 Documentation
    
    - `OLLAMA_GUIDE.md` - Ollama setup
    - `README.md` - Full documentation
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("**Backend:** Ollama (Primary)")
    with col2:
        st.success("**Cost:** FREE")
            st.success("**Cost:** Free tier")

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray; font-size: 0.9em;'>🧠 DataDistillerAI | RAG System</div>", unsafe_allow_html=True)
