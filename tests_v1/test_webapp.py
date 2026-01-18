#!/usr/bin/env python3
"""
Comprehensive verification script for DataDistillerAI web app
Tests all components needed by app.py
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test all required imports"""
    logger.info("=" * 70)
    logger.info("1. TESTING IMPORTS")
    logger.info("=" * 70)
    
    imports_to_test = [
        ("streamlit", "Streamlit web framework"),
        ("pathlib", "Path handling"),
        ("dotenv", "Environment variable loading"),
        ("requests", "HTTP requests for Ollama"),
        ("sentence_transformers", "Embedding model"),
        ("faiss", "Vector database"),
    ]
    
    all_good = True
    for module_name, description in imports_to_test:
        try:
            __import__(module_name)
            logger.info(f"✅ {module_name:30} - {description}")
        except ImportError as e:
            logger.error(f"❌ {module_name:30} - {description}")
            logger.error(f"   Error: {e}")
            all_good = False
    
    return all_good

def test_src_modules():
    """Test all src module imports"""
    logger.info("\n" + "=" * 70)
    logger.info("2. TESTING SRC MODULES")
    logger.info("=" * 70)
    
    try:
        from src.ingestion import DocumentLoader
        logger.info("✅ DocumentLoader             - Load documents from disk")
        
        from src.processing.chunker import SemanticChunker
        logger.info("✅ SemanticChunker            - Chunk text semantically")
        
        from src.retrieval import VectorStore
        logger.info("✅ VectorStore                - Vector database with FAISS")
        
        from src.llm_ollama import OllamaClient
        logger.info("✅ OllamaClient               - Ollama LLM client")
        
        from src.workflows_ollama import RAGPipelineOllama
        logger.info("✅ RAGPipelineOllama          - Complete RAG pipeline")
        
        return True
    
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False

def test_data_directory():
    """Test document directory"""
    logger.info("\n" + "=" * 70)
    logger.info("3. TESTING DATA DIRECTORY")
    logger.info("=" * 70)
    
    doc_path = Path("data/documents")
    
    if doc_path.exists():
        files = list(doc_path.glob("*"))
        if files:
            logger.info(f"✅ Documents directory exists with {len(files)} file(s):")
            for f in files[:5]:
                size = f.stat().st_size if f.is_file() else 0
                logger.info(f"   • {f.name} ({size:,} bytes)")
            if len(files) > 5:
                logger.info(f"   ... and {len(files)-5} more")
            return True
        else:
            logger.warning("⚠️  Documents directory is empty")
            logger.warning("   Add documents to data/documents/ to use the system")
            return True  # Not a blocker
    else:
        logger.warning("⚠️  Documents directory doesn't exist: data/documents/")
        logger.warning("   Creating it for you...")
        doc_path.mkdir(parents=True, exist_ok=True)
        logger.warning("   Add documents to data/documents/ to use the system")
        return True  # Not a blocker

def test_pipeline_initialization():
    """Test pipeline can be initialized"""
    logger.info("\n" + "=" * 70)
    logger.info("4. TESTING PIPELINE INITIALIZATION")
    logger.info("=" * 70)
    
    try:
        from src.workflows_ollama import RAGPipelineOllama
        
        logger.info("   Creating RAGPipelineOllama instance...")
        pipeline = RAGPipelineOllama()
        
        logger.info(f"✅ Pipeline initialized successfully")
        logger.info(f"   • Document path: {pipeline.document_path}")
        logger.info(f"   • Vector store path: {pipeline.vector_store_path}")
        logger.info(f"   • Model: {pipeline.model}")
        logger.info(f"   • Ollama URL: {pipeline.ollama_url}")
        
        # Test loader
        logger.info("\n   Testing DocumentLoader...")
        loader = pipeline.loader
        logger.info(f"✅ DocumentLoader supports: {loader.SUPPORTED_FORMATS}")
        
        # Test chunker
        logger.info("\n   Testing SemanticChunker...")
        chunker = pipeline.chunker
        logger.info(f"✅ SemanticChunker configured:")
        logger.info(f"   • Chunk size: {chunker.chunk_size}")
        logger.info(f"   • Overlap: {chunker.overlap}")
        
        # Test vector store
        logger.info("\n   Testing VectorStore...")
        vs = pipeline.vector_store
        logger.info(f"✅ VectorStore initialized")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Pipeline initialization failed: {e}")
        return False

def test_llm_client():
    """Test LLM client initialization"""
    logger.info("\n" + "=" * 70)
    logger.info("5. TESTING LLM CLIENT")
    logger.info("=" * 70)
    
    try:
        from src.llm_ollama import OllamaClient
        
        logger.info("   Connecting to Ollama...")
        client = OllamaClient()
        
        logger.info(f"✅ OllamaClient initialized successfully")
        logger.info(f"   • Model: {client.model}")
        logger.info(f"   • Base URL: {client.base_url}")
        
        return True
    
    except ConnectionError as e:
        logger.error(f"❌ {e}")
        logger.error("   Ensure Ollama is running: ollama serve")
        return False
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

def test_webapp_components():
    """Test specific web app components"""
    logger.info("\n" + "=" * 70)
    logger.info("6. TESTING WEBAPP-SPECIFIC COMPONENTS")
    logger.info("=" * 70)
    
    try:
        from src.workflows_ollama import RAGPipelineOllama
        
        pipeline = RAGPipelineOllama()
        
        # Test methods called by app.py
        logger.info("   Checking pipeline.index_documents()...")
        assert hasattr(pipeline, 'index_documents'), "Missing index_documents method"
        logger.info("✅ pipeline.index_documents() - OK")
        
        logger.info("   Checking pipeline.query()...")
        assert hasattr(pipeline, 'query'), "Missing query method"
        logger.info("✅ pipeline.query() - OK")
        
        logger.info("   Checking pipeline.vector_store.search()...")
        assert hasattr(pipeline.vector_store, 'search'), "Missing search method"
        logger.info("✅ pipeline.vector_store.search() - OK")
        
        logger.info("   Checking pipeline.vector_store.get_all_documents()...")
        assert hasattr(pipeline.vector_store, 'get_all_documents'), "Missing get_all_documents method"
        logger.info("✅ pipeline.vector_store.get_all_documents() - OK")
        
        logger.info("   Checking pipeline.loader.load_directory()...")
        assert hasattr(pipeline.loader, 'load_directory'), "Missing load_directory method"
        logger.info("✅ pipeline.loader.load_directory() - OK")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

def test_streamlit_features():
    """Test Streamlit is working"""
    logger.info("\n" + "=" * 70)
    logger.info("7. TESTING STREAMLIT")
    logger.info("=" * 70)
    
    try:
        import streamlit as st
        
        logger.info(f"✅ Streamlit version: {st.__version__}")
        
        # Check key Streamlit components used in app.py
        methods = [
            'set_page_config', 'title', 'markdown', 'sidebar', 'text_input',
            'button', 'spinner', 'error', 'success', 'tabs', 'header',
            'columns', 'slider', 'metric', 'expander', 'chat_message',
            'session_state', 'cache_resource'
        ]
        
        all_available = True
        for method in methods:
            if hasattr(st, method):
                logger.info(f"✅ st.{method:30} - OK")
            else:
                logger.error(f"❌ st.{method:30} - MISSING")
                all_available = False
        
        return all_available
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False

def print_summary(results):
    """Print test summary"""
    logger.info("\n" + "=" * 70)
    logger.info("SUMMARY")
    logger.info("=" * 70)
    
    test_names = [
        "Imports",
        "Src Modules",
        "Data Directory",
        "Pipeline Init",
        "LLM Client",
        "Webapp Components",
        "Streamlit"
    ]
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    logger.info(f"\nTests Passed: {passed}/{total}\n")
    
    for name, result in zip(test_names, results):
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status:10} {name}")
    
    if all(results):
        logger.info("\n" + "=" * 70)
        logger.info("🎉 ALL TESTS PASSED - WEB APP IS READY!")
        logger.info("=" * 70)
        logger.info("\nRun the web app with:")
        logger.info("  streamlit run app.py")
        logger.info("\nOr try the simple version:")
        logger.info("  streamlit run app_simple.py")
        logger.info("")
        return True
    else:
        logger.info("\n" + "=" * 70)
        logger.info("⚠️  SOME TESTS FAILED")
        logger.info("=" * 70)
        logger.info("\nCheck the error messages above for details.")
        logger.info("")
        return False

def main():
    """Run all tests"""
    print()
    
    results = []
    
    results.append(test_imports())
    results.append(test_src_modules())
    results.append(test_data_directory())
    results.append(test_pipeline_initialization())
    results.append(test_llm_client())
    results.append(test_webapp_components())
    results.append(test_streamlit_features())
    
    success = print_summary(results)
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
