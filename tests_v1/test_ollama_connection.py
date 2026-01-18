#!/usr/bin/env python3
"""
Quick test to verify Ollama connection and functionality
Run this to check if Ollama is properly configured
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

def test_ollama_connection():
    """Test if Ollama server is reachable"""
    logger.info("=" * 60)
    logger.info("OLLAMA CONNECTION TEST")
    logger.info("=" * 60)
    
    import requests
    
    try:
        logger.info("\n1. Checking Ollama server at http://localhost:11434...")
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            logger.info("✅ Ollama server is RUNNING")
            return True
        else:
            logger.error(f"❌ Ollama returned status code: {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        logger.error("❌ Cannot connect to Ollama server")
        logger.error("   Make sure Ollama is running:")
        logger.error("   $ ollama serve")
        return False
    
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


def test_available_models():
    """List available Ollama models"""
    logger.info("\n2. Checking available models...")
    
    import requests
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            
            if not models:
                logger.warning("   No models installed")
                logger.info("   Install a model with: ollama pull qwen2.5:3b")
                return None
            
            logger.info(f"   Found {len(models)} model(s):")
            for model in models:
                name = model.get('name', 'unknown')
                size = model.get('size', 0)
                size_gb = size / (1e9)
                logger.info(f"   • {name} ({size_gb:.1f} GB)")
            
            return models[0]['name'] if models else None
        
        return None
    
    except Exception as e:
        logger.error(f"   Error: {e}")
        return None


def test_ollama_client():
    """Test OllamaClient initialization"""
    logger.info("\n3. Testing OllamaClient initialization...")
    
    try:
        from src.llm_ollama import OllamaClient
        
        try:
            client = OllamaClient()
            logger.info(f"✅ OllamaClient initialized successfully")
            logger.info(f"   Model: {client.model}")
            logger.info(f"   URL: {client.base_url}")
            return client
        
        except ConnectionError as e:
            logger.error(f"❌ {e}")
            return None
        
        except ValueError as e:
            logger.error(f"❌ {e}")
            logger.info("   Available models:")
            client_check = OllamaClient.__init__.__doc__
            logger.info("   - qwen2.5:3b")
            logger.info("   - mistral")
            logger.info("   - llama2")
            return None
    
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return None


def test_simple_generation(client):
    """Test a simple text generation"""
    logger.info("\n4. Testing simple text generation...")
    
    if not client:
        logger.warning("   Skipped (no client available)")
        return False
    
    try:
        logger.info("   Sending test prompt...")
        response = client.generate(
            "What is machine learning? Answer in 1 sentence.",
            max_tokens=100
        )
        
        logger.info("✅ Generation successful!")
        logger.info(f"   Response: {response[:200]}...")
        return True
    
    except Exception as e:
        logger.error(f"❌ Generation failed: {e}")
        return False


def test_rag_pipeline():
    """Test RAGPipelineOllama"""
    logger.info("\n5. Testing RAGPipelineOllama...")
    
    try:
        from src.workflows_ollama import RAGPipelineOllama
        
        logger.info("   Initializing pipeline...")
        pipeline = RAGPipelineOllama()
        
        logger.info("✅ RAGPipelineOllama initialized successfully")
        logger.info(f"   Document path: {pipeline.document_path}")
        logger.info(f"   Vector store path: {pipeline.vector_store_path}")
        logger.info(f"   Model: {pipeline.model}")
        
        return pipeline
    
    except Exception as e:
        logger.error(f"❌ Pipeline initialization failed: {e}")
        return None


def main():
    """Run all tests"""
    print()
    
    # Step 1: Connection test
    if not test_ollama_connection():
        logger.error("\n" + "=" * 60)
        logger.error("OLLAMA NOT RUNNING")
        logger.error("=" * 60)
        logger.error("\nTo fix this:")
        logger.error("1. Install Ollama from https://ollama.ai")
        logger.error("2. Run: ollama serve")
        logger.error("3. In another terminal, pull a model:")
        logger.error("   ollama pull qwen2.5:3b")
        logger.error("4. Re-run this test\n")
        return False
    
    # Step 2: Check models
    default_model = test_available_models()
    
    # Step 3: Test client
    client = test_ollama_client()
    
    # Step 4: Test generation
    if client:
        test_simple_generation(client)
    
    # Step 5: Test pipeline
    pipeline = test_rag_pipeline()
    
    # Summary
    logger.info("\n" + "=" * 60)
    
    if client and pipeline:
        logger.info("✅ ALL TESTS PASSED - Ollama is working!")
        logger.info("=" * 60)
        logger.info("\nYou can now use:")
        logger.info("  • Web UI: streamlit run app.py")
        logger.info("  • Simple UI: streamlit run app_simple.py")
        logger.info("  • CLI: python cli.py")
        logger.info("")
        return True
    else:
        logger.error("❌ Some tests failed")
        logger.error("=" * 60)
        logger.error("\nCheck the error messages above for details.\n")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
