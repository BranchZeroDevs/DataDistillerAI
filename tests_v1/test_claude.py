#!/usr/bin/env python3
"""
Test script for Claude integration with DataDistillerAI RAG system
Professional AI with excellent reasoning and context understanding
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path('.env'))

print("\n" + "="*80)
print("🧠 CLAUDE (ANTHROPIC) - RAG SYSTEM TEST")
print("="*80 + "\n")

# Check if API key is set
api_key = os.getenv('ANTHROPIC_API_KEY')
if not api_key:
    print("⚠️  ANTHROPIC_API_KEY not found in .env")
    print("\nTo get a Claude API key:")
    print("1. Visit: https://console.anthropic.com/")
    print("2. Create account or sign in")
    print("3. Generate API key")
    print("4. Add to .env: ANTHROPIC_API_KEY=sk-ant-xxxxx")
    print("\nThen run this script again.\n")
    exit(1)

print(f"✓ API Key found: {api_key[:20]}...{api_key[-10:]}\n")

# Test 1: Basic connection
print("1️⃣  TESTING CLAUDE CONNECTION")
print("-" * 80)

try:
    from src.llm_claude import ClaudeClient
    client = ClaudeClient(api_key=api_key)
    model_info = client.get_model_info()
    print(f"✓ Claude client initialized successfully")
    print(f"  Model: {model_info['model']}")
    print(f"  Provider: {model_info['provider']}\n")
except Exception as e:
    print(f"✗ Error initializing Claude client: {e}\n")
    print("Need to install anthropic? Run:")
    print("  pip install anthropic\n")
    exit(1)

# Test 2: Simple generation
print("2️⃣  TESTING BASIC TEXT GENERATION")
print("-" * 80)

try:
    response = client.generate("Explain machine learning in 2 sentences.")
    print(f"✓ Generated text:\n   {response}\n")
except Exception as e:
    print(f"✗ Error: {e}\n")
    exit(1)

# Test 3: Load documents and test RAG
print("3️⃣  TESTING RAG WITH CLAUDE")
print("-" * 80)

try:
    from src.ingestion import DocumentLoader
    from src.processing.chunker import SemanticChunker
    from src.retrieval import VectorStore
    
    # Load and process documents
    print("   Loading documents...")
    loader = DocumentLoader()
    documents = loader.load_directory("./data/documents")
    print(f"   ✓ Loaded {len(documents)} documents")
    
    print("   Creating semantic chunks...")
    chunker = SemanticChunker(chunk_size=1024, overlap=128)
    all_chunks = []
    for doc in documents:
        chunks = chunker.chunk(doc.content, metadata=doc.metadata)
        all_chunks.extend(chunks)
    print(f"   ✓ Created {len(all_chunks)} chunks")
    
    print("   Indexing in FAISS...")
    vector_store = VectorStore()
    vector_store.add_documents(all_chunks)
    print(f"   ✓ Indexed {len(all_chunks)} chunks\n")
    
    # Test question
    query = "What is machine learning and how does it work?"
    results = vector_store.search(query, top_k=2)
    context = "\n\n".join([content for content, _, _ in results])
    
    print(f"   Query: '{query}'")
    print("   " + "-" * 76)
    
    answer = client.query_with_context(query, context)
    print(f"   Answer: {answer}\n")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Summarization
print("4️⃣  TESTING SUMMARIZATION")
print("-" * 80)

try:
    text = "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms and statistical models that allow computers to identify patterns in data. Deep learning is a specialized branch of machine learning that uses neural networks with multiple layers to process information in ways inspired by the brain."
    
    summary = client.summarize(text)
    print(f"   Original: {text[:100]}...")
    print(f"   Summary: {summary}\n")
    
except Exception as e:
    print(f"✗ Error: {e}\n")
    exit(1)

# Test 5: RAG Pipeline
print("5️⃣  TESTING FULL RAG PIPELINE")
print("-" * 80)

try:
    from src.workflows_claude import RAGPipelineClaude
    
    pipeline = RAGPipelineClaude()
    print("   Indexing documents...")
    num_chunks = pipeline.index_documents()
    print(f"   ✓ Indexed {num_chunks} chunks\n")
    
    # Ask a question
    question = "Explain the difference between machine learning and deep learning."
    print(f"   Question: {question}")
    print("   " + "-" * 76)
    answer = pipeline.query(question, top_k=2)
    print(f"   Answer: {answer}\n")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("="*80)
print("✅ ALL TESTS PASSED - CLAUDE IS WORKING!")
print("="*80)
print("\n📊 SUMMARY:")
print("   ✓ Claude API Connection: WORKING")
print("   ✓ Basic Generation: WORKING")
print("   ✓ RAG with Context: WORKING")
print("   ✓ Summarization: WORKING")
print("   ✓ Full RAG Pipeline: WORKING")
print("\n💡 CLAUDE ADVANTAGES:")
print("   • Excellent reasoning and analysis")
print("   • Superior context understanding")
print("   • Best for complex questions")
print("   • Professional quality output")
print("\n🚀 Your RAG system now works with Claude!\n")
