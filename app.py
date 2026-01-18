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

# Sidebar - Configuration
st.sidebar.title("⚙️ Configuration")

st.sidebar.info("🚀 **Primary LLM Backend:** Ollama (Local) - Privacy-first, completely free")

# Advanced backend selection (hidden by default)
with st.sidebar.expander("⚙️ Advanced Backend Options (Code-only)"):
    st.write("Available secondary options for development:")
    st.code("Claude (Haiku) - Cloud, low cost\nGemini - Cloud, free tier", language="text")
    st.write("To use these, modify the backend selection code.")

# Always use Ollama as primary
selected_backend = "ollama"

# Initialize RAG pipeline - Primary: Ollama
@st.cache_resource
def load_rag_pipeline(backend_name="ollama"):
    """Load RAG pipeline. Primary backend is Ollama (local, free).
    
    Secondary options available in code:
    - claude: RAGPipelineClaude
    - gemini: RAGPipelineGemini
    """
    try:
        if backend_name == "ollama":
            from src.workflows_ollama import RAGPipelineOllama
            pipeline = RAGPipelineOllama()
        elif backend_name == "claude":
            # Secondary option - requires ANTHROPIC_API_KEY
            from src.workflows_claude import RAGPipelineClaude
            pipeline = RAGPipelineClaude()
        elif backend_name == "gemini":
            # Secondary option - requires GOOGLE_API_KEY
            from src.workflows_gemini import RAGPipelineGemini
            pipeline = RAGPipelineGemini()
        else:
            raise ValueError(f"Unknown backend: {backend_name}")
        
        return pipeline
    except Exception as e:
        st.error(f"❌ Failed to load {backend_name}: {str(e)}")
        return None

# Index documents once
@st.cache_resource
def index_documents(_pipeline):
    try:
        with st.spinner(f"📚 Indexing documents..."):
            _pipeline.index_documents()
        return True
    except Exception as e:
        st.error(f"Error indexing: {str(e)}")
        return False

# Main title
st.title("🧠 DataDistillerAI")
st.markdown("*Intelligent Document Q&A powered by Ollama (Local)*")

# Load pipeline - always Ollama for primary
pipeline = load_rag_pipeline("ollama")

if pipeline is None:
    st.error("Could not initialize Ollama backend. Check if Ollama is running (http://localhost:11434)")
    st.stop()

# Index documents
indexed = index_documents(pipeline)
if not indexed:
    st.stop()

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📊 Documents", "🧠 Knowledge Graph", "ℹ️ About"])

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
        with st.spinner("🔍 Searching and thinking with Ollama..."):
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
    
    # Document upload section
    st.subheader("📤 Upload New Documents")
    
    uploaded_files = st.file_uploader(
        "Upload documents (PDF, DOCX, TXT, HTML, MD)",
        type=["pdf", "docx", "txt", "html", "md"],
        accept_multiple_files=True,
        help="Upload one or more documents to add to your knowledge base"
    )
    
    if uploaded_files:
        if st.button("📥 Process & Index Uploaded Files", key="upload_button"):
            doc_path = Path(pipeline.document_path)
            doc_path.mkdir(parents=True, exist_ok=True)
            
            uploaded_count = 0
            with st.spinner("📥 Processing uploaded files..."):
                try:
                    for uploaded_file in uploaded_files:
                        # Save file
                        file_path = doc_path / uploaded_file.name
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        uploaded_count += 1
                    
                    st.success(f"✅ Saved {uploaded_count} file(s)")
                    
                    # Re-index documents
                    with st.spinner("🔄 Re-indexing all documents..."):
                        # Clear cache to force re-indexing
                        st.cache_resource.clear()
                        pipeline.index_documents()
                    
                    st.success(f"✅ Successfully indexed {uploaded_count} new document(s)!")
                    st.info("💡 Refresh the page or ask a question to see the new documents in action")
                
                except Exception as e:
                    st.error(f"❌ Error processing files: {str(e)}")
    
    st.markdown("---")
    
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
        
        if docs:
            for doc in docs:
                with st.expander(f"📖 {doc.metadata.get('filename', 'Unknown')}"):
                    st.write(f"**Size:** {len(doc.content):,} characters")
                    st.text(doc.content[:500] + "..." if len(doc.content) > 500 else doc.content)
        else:
            st.info("📚 No documents indexed yet. Upload documents above to get started!")
                
    except Exception as e:
        st.error(f"Error loading documents: {str(e)}")

# TAB 3: KNOWLEDGE GRAPH
with tab3:
    from test_kg_phase2 import display_knowledge_graph_tab
    display_knowledge_graph_tab(pipeline)

# TAB 4: ABOUT
with tab4:
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
    
    ### � Primary Backend: Ollama
    
    | Feature | Ollama |
    |---------|--------|
    | **Type** | Local |
    | **Cost** | Free |
    | **Privacy** | 100% Local |
    | **Speed** | ⚡⚡⚡ |
    | **Quality** | ⭐⭐⭐⭐ |
    
    **Secondary backends available in code:**
    - Claude Haiku (Cloud, low cost)
    - Gemini (Cloud, free tier)
    
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
    st.subheader("🚀 Currently Using")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("**Backend:** Ollama (Primary)")
    
    with col2:
        st.success("**Cost:** FREE - Runs Locally")

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
