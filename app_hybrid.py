"""
DataDistillerAI - Web UI with Streamlit (Hybrid Mode)
Works with both DataDistiller 1.0 (direct) and 2.0 (async API)
"""

import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os
import requests
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

# Sidebar - Mode Selection
st.sidebar.title("⚙️ Configuration")


def get_api_headers():
    """Build optional API auth headers."""
    api_key = os.getenv("DATADISTILLER_API_KEY")
    if api_key:
        return {"X-API-Key": api_key}
    return {}

# Check if 2.0 API is available
def check_api_available():
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

api_available = check_api_available()

# Mode selection (default to V2)
if api_available:
    st.sidebar.success("✅ DataDistiller 2.0 API detected")
else:
    st.sidebar.warning("⚠️ DataDistiller 2.0 API not running")

mode = st.sidebar.radio(
    "Select Mode:",
    ["🚀 2.0 Async API", "💻 1.0 Direct Pipeline"],
    index=0
)

USE_API = "2.0" in mode

if USE_API and not api_available:
    st.warning("🚫 2.0 API is not available. Start the API to use V2 mode, or switch to V1.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.info("🚀 **Primary LLM Backend:** Ollama (Local)")

# Initialize pipeline (1.0 mode only)
@st.cache_resource
def load_rag_pipeline():
    """Load RAG pipeline for 1.0 direct mode"""
    try:
        from src.workflows_ollama import RAGPipelineOllama
        pipeline = RAGPipelineOllama()
        return pipeline
    except Exception as e:
        st.error(f"❌ Failed to load pipeline: {str(e)}")
        return None

# Index documents (1.0 mode only)
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
if USE_API:
    st.markdown("*Connected to DataDistiller 2.0 Async API*")
else:
    st.markdown("*Running DataDistiller 1.0 Direct Mode*")

# Initialize based on mode
pipeline = None
if not USE_API:
    pipeline = load_rag_pipeline()
    if pipeline is None:
        st.error("Could not initialize pipeline. Check if Ollama is running.")
        st.stop()
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
        if USE_API:
            # 2.0 API Mode
            with st.spinner("🔍 Querying via async API..."):
                try:
                    response = requests.post(
                        "http://localhost:8000/api/v2/query",
                        json={"query": user_question, "top_k": top_k},
                        headers=get_api_headers(),
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("answer", "No answer returned")
                        sources = data.get("sources", [])
                        
                        st.markdown("### Answer")
                        st.markdown(answer)
                        
                        # Show sources
                        if sources:
                            with st.expander("📎 Retrieved Context"):
                                for i, source in enumerate(sources, 1):
                                    st.markdown(f"**Chunk {i}** (Score: {source.get('score', 0):.2%})")
                                    content = source.get('content', '')
                                    st.text(content[:300] + "..." if len(content) > 300 else content)
                                    st.divider()
                    else:
                        st.error(f"API Error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    st.error(f"Error querying API: {str(e)}")
        else:
            # 1.0 Direct Mode
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
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Store current message in history
    if user_question and st.button("Save to History", key="save_history"):
        st.session_state.messages.append({"role": "user", "content": user_question})
        if 'answer' in locals():
            st.session_state.messages.append({"role": "assistant", "content": answer})
        st.success("✅ Added to chat history")

# TAB 2: DOCUMENTS
with tab2:
    st.header("Document Information")
    
    if USE_API:
        # 2.0 API Mode - Show async upload
        st.subheader("📤 Upload Documents (Async)")
        
        uploaded_files = st.file_uploader(
            "Upload documents (TXT, PDF, MD, etc.)",
            type=["pdf", "docx", "txt", "html", "md"],
            accept_multiple_files=True,
            help="Upload documents - they'll be processed asynchronously"
        )
        
        if uploaded_files and st.button("🚀 Upload to Async Pipeline", key="async_upload"):
            with st.spinner("📤 Uploading documents..."):
                job_ids = []
                for uploaded_file in uploaded_files:
                    try:
                        # Determine correct MIME type based on file extension
                        file_ext = uploaded_file.name.split('.')[-1].lower()
                        mime_types = {
                            'pdf': 'application/pdf',
                            'txt': 'text/plain',
                            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            'md': 'text/plain',
                            'html': 'text/html',
                        }
                        mime_type = mime_types.get(file_ext, 'application/octet-stream')
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), mime_type)}
                        response = requests.post(
                            "http://localhost:8000/api/v2/documents/upload",
                            files=files,
                            headers=get_api_headers(),
                            timeout=10
                        )
                        
                        if response.status_code == 202:
                            data = response.json()
                            job_ids.append((uploaded_file.name, data["job_id"]))
                            st.success(f"✅ {uploaded_file.name} - Job ID: {data['job_id'][:8]}...")
                        else:
                            st.error(f"❌ {uploaded_file.name} failed: {response.status_code}")
                    except Exception as e:
                        st.error(f"❌ {uploaded_file.name} error: {str(e)}")
                
                if job_ids:
                    st.info("ℹ️ Documents are being processed in the background. Check 'Processing Jobs' below for status.")
        
        st.markdown("---")
        st.subheader("⚙️ Processing Jobs")
        
        # Show document list from API
        try:
            response = requests.get(
                "http://localhost:8000/api/v2/documents/list",
                headers=get_api_headers(),
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                st.metric("Total Documents", data.get("total", 0))
                
                if data.get("jobs"):
                    st.markdown("### Recent Jobs")
                    for doc in data["jobs"][:10]:
                        status_icon = {
                            "completed": "✅",
                            "embedding": "🔄",
                            "chunking": "✂️",
                            "processing": "⚙️",
                            "pending": "⏳",
                            "failed": "❌"
                        }.get(doc["status"], "❓")
                        
                        col1, col2, col3 = st.columns([3, 2, 1])
                        with col1:
                            st.write(f"{status_icon} **{doc['filename']}**")
                        with col2:
                            st.write(f"Status: {doc['status']}")
                        with col3:
                            st.write(f"{doc.get('progress', 0)}%")
                        
                        if doc["status"] not in ["completed", "failed"]:
                            st.progress(doc.get("progress", 0) / 100)
                else:
                    st.info("ℹ️ No documents uploaded yet. Upload documents above to get started!")
        except Exception as e:
            st.error(f"Could not fetch document list: {str(e)}")
    
    else:
        # 1.0 Direct Mode - Traditional upload
        st.subheader("📤 Upload New Documents")
        
        uploaded_files = st.file_uploader(
            "Upload documents (PDF, DOCX, TXT, HTML, MD)",
            type=["pdf", "docx", "txt", "html", "md"],
            accept_multiple_files=True,
            help="Upload one or more documents to add to your knowledge base"
        )
        
        if uploaded_files and st.button("📥 Process & Index Files", key="sync_upload"):
            doc_path = Path(pipeline.document_path)
            doc_path.mkdir(parents=True, exist_ok=True)
            
            uploaded_count = 0
            with st.spinner("📥 Processing uploaded files..."):
                try:
                    for uploaded_file in uploaded_files:
                        file_path = doc_path / uploaded_file.name
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        uploaded_count += 1
                    
                    st.success(f"✅ Saved {uploaded_count} file(s)")
                    
                    # Re-index
                    with st.spinner("🔄 Re-indexing..."):
                        st.cache_resource.clear()
                        pipeline.index_documents()
                    
                    st.success(f"✅ Indexed {uploaded_count} new document(s)!")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        st.markdown("---")
        st.subheader("📚 Indexed Documents")
        
        # Show document stats
        if pipeline and hasattr(pipeline, 'vector_store'):
            num_chunks = pipeline.vector_store.document_count
            st.metric("Total Chunks", num_chunks)
            
            # List documents
            doc_path = Path(pipeline.document_path)
            if doc_path.exists():
                docs = list(doc_path.glob("*"))
                st.write(f"**Files in {doc_path}:**")
                for doc in docs:
                    st.write(f"- {doc.name} ({doc.stat().st_size} bytes)")

# TAB 3: KNOWLEDGE GRAPH (only for 1.0 mode)
with tab3:
    if USE_API:
        st.info("📊 Knowledge Graph visualization is available in 1.0 Direct Mode")
        st.write("Switch to 1.0 mode in the sidebar to access Knowledge Graph features.")
    else:
        st.header("Knowledge Graph Visualization")
        
        try:
            from tests_v1.test_kg_phase2 import display_knowledge_graph_tab
            display_knowledge_graph_tab(pipeline)
        except Exception as e:
            st.error(f"Knowledge Graph not available: {str(e)}")

# TAB 4: ABOUT
with tab4:
    st.header("About DataDistillerAI")
    
    mode_info = "2.0 Async API" if USE_API else "1.0 Direct Pipeline"
    
    st.markdown(f"""
    ### Current Mode: {mode_info}
    
    **DataDistiller 2.0 Features (API Mode):**
    - ✅ Async document processing
    - ✅ Background workers for embedding generation
    - ✅ Job status tracking
    - ✅ Scalable architecture with Kafka
    - ✅ Production-ready infrastructure
    
    **DataDistiller 1.0 Features (Direct Mode):**
    - ✅ Direct Ollama integration
    - ✅ Knowledge Graph visualization
    - ✅ Interactive network graphs
    - ✅ Semantic flow analysis
    - ✅ AI-enhanced concept analysis
    
    **LLM Backend:** Ollama (qwen2.5:3b)
    - Runs completely locally
    - Privacy-first approach
    - No API costs
    
    **Components:**
    - Vector Database: FAISS
    - Embeddings: sentence-transformers/all-MiniLM-L6-v2
    - Message Queue: Kafka (2.0)
    - Storage: MinIO + PostgreSQL (2.0)
    """)
    
    if USE_API:
        st.markdown("---")
        st.subheader("🔧 System Status")
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ API Status: {data['status']}")
                st.json(data)
        except:
            st.error("❌ Cannot connect to API")
