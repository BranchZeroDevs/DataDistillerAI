"""
DataDistillerAI - Web UI with Streamlit
Simple chat interface for RAG system with multiple LLM backends
"""

import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment
load_dotenv(Path('.env'))

# Page config
st.set_page_config(
    page_title="DataDistillerAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Backend Selection
st.sidebar.title("⚙️ Configuration")

backend = st.sidebar.radio(
    "Choose LLM Backend",
    ["Claude (Haiku)", "Ollama (Local)", "Gemini (Free)"],
    index=0,
    help="Select which LLM to use for answering questions"
)

backend_map = {
    "Claude (Haiku)": "claude",
    "Ollama (Local)": "ollama",
    "Gemini (Free)": "gemini"
}

selected_backend = backend_map[backend]

# Initialize RAG pipeline based on backend
@st.cache_resource
def load_rag_pipeline(backend_name):
    try:
        if backend_name == "claude":
            from src.workflows_claude import RAGPipelineClaude
            pipeline = RAGPipelineClaude()
        elif backend_name == "ollama":
            from src.workflows_ollama import RAGPipelineOllama
            pipeline = RAGPipelineOllama()
        elif backend_name == "gemini":
            from src.workflows_gemini import RAGPipelineGemini
            pipeline = RAGPipelineGemini()
        
        return pipeline
    except Exception as e:
        st.error(f"❌ Failed to load {backend_name}: {str(e)}")
        return None

# Index documents once
@st.cache_resource
def index_documents(pipeline):
    try:
        with st.spinner(f"📚 Indexing documents..."):
            pipeline.index_documents()
        return True
    except Exception as e:
        st.error(f"Error indexing: {str(e)}")
        return False

# Main title
st.title("🧠 DataDistillerAI")
st.markdown("*Intelligent Document Q&A with Multiple LLM Backends*")

# Load pipeline
pipeline = load_rag_pipeline(selected_backend)

if pipeline is None:
    st.error(f"Could not initialize {backend} backend. Check your API keys and setup.")
    st.stop()

# Index documents
indexed = index_documents(pipeline)
if not indexed:
    st.stop()

# Create tabs
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Documents", "ℹ️ About"])

# TAB 1: CHAT
with tab1:
    st.header("Ask Questions About Your Documents")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_question = st.text_input(
            "Your question:",
            placeholder="What would you like to know about your documents?",
            label_visibility="collapsed"
        )
    
    with col2:
        top_k = st.slider("Top results", 1, 5, 3, label_visibility="collapsed")
    
    if user_question:
        with st.spinner(f"🔍 Searching and thinking with {backend}..."):
            try:
                answer = pipeline.query(user_question, top_k=top_k)
                
                st.markdown("### Answer")
                st.markdown(answer)
                
                # Show retrieval details
                with st.expander("📎 Retrieved Context"):
                    results = pipeline.vector_store.search(user_question, top_k=top_k)
                    for i, (content, metadata, score) in enumerate(results, 1):
                        st.markdown(f"**Chunk {i}** (Relevance: {score:.2%})")
                        st.text(content[:300] + "..." if len(content) > 300 else content)
                        st.divider()
                
            except Exception as e:
                st.error(f"Error processing question: {str(e)}")
    
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    st.markdown("---")
    st.subheader("💭 Chat History")
    
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Store current message in history
    if user_question and st.button("Save to History", key="save_history"):
        st.session_state.messages.append({"role": "user", "content": user_question})
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.success("✅ Added to chat history")

# TAB 2: DOCUMENTS
with tab2:
    st.header("Document Information")
    
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
                st.write(f"**Size:** {len(doc.content):,} characters")
                st.text(doc.content[:500] + "..." if len(doc.content) > 500 else doc.content)
                
    except Exception as e:
        st.error(f"Error loading documents: {str(e)}")

# TAB 3: ABOUT
with tab3:
    st.header("About DataDistillerAI")
    
    st.markdown("""
    ### 🎯 What is DataDistillerAI?
    
    
    A powerful Retrieval-Augmented Generation (RAG) system that lets you:
    - 📚 Index and search your documents
    - 🧠 Ask intelligent questions about your data
    - 🔗 Get answers grounded in your documents
    - 🔄 Switch between multiple LLM backends
    
    ### 🚀 Features
    
    - **Multiple Backends**: Choose between Claude, Ollama, or Gemini
    - **Vector Search**: FAISS-based semantic search
    - **Smart Chunking**: Intelligent paragraph-aware text splitting
    - **RAG Pipeline**: Retrieval-augmented generation for accurate answers
    - **Document Support**: PDF, DOCX, TXT, HTML, Markdown
    
    ### 💡 How It Works
    
    1. **Document Indexing**: Your documents are loaded and split into chunks
    2. **Embedding**: Chunks are converted to embeddings using sentence-transformers
    3. **Vector Search**: When you ask a question, relevant chunks are retrieved
    4. **LLM Generation**: The LLM generates an answer based on retrieved context
    5. **Grounded Response**: Answers are grounded in your actual documents
    
    ### 🔧 Backends Available
    
    | Backend | Type | Cost | Speed | Quality |
    |---------|------|------|-------|---------|
    | **Claude Haiku** | Cloud | Low | ⚡⚡⚡ | ⭐⭐⭐⭐ |
    | **Ollama** | Local | Free | ⚡⚡⚡ | ⭐⭐⭐⭐ |
    | **Gemini** | Cloud | Free Tier | ⚡⚡ | ⭐⭐⭐⭐ |
    
    ### 📚 Tech Stack
    
    - **LLM Frameworks**: LangChain, Anthropic SDK
    - **Vector DB**: FAISS
    - **Embeddings**: sentence-transformers
    - **Backend**: Python, FastAPI ready
    - **UI**: Streamlit
    
    ### 📖 Documentation
    
    - `CLAUDE_SETUP.md` - Claude setup guide
    - `OLLAMA_GUIDE.md` - Ollama local setup
    - `MULTI_LLM_GUIDE.md` - Multi-backend guide
    - `README.md` - Main documentation
    
    ---
    
    **Built with ❤️ for intelligent document analysis**
    """)
    
    # Backend info
    st.markdown("---")
    st.subheader("Currently Using")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Backend:** {backend}")
    
    with col2:
        if selected_backend == "claude":
            st.success("**Cost:** ~$0.80/1M input tokens")
        elif selected_backend == "ollama":
            st.success("**Cost:** FREE (runs locally)")
        else:
            st.success("**Cost:** Free tier available")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
    🧠 DataDistillerAI | Multi-LLM RAG System | Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
