#!/usr/bin/env python3
"""
Test script for Google Gemini integration with DataDistillerAI RAG system
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path('.env'))

print("\n" + "="*80)
print("🟢 GOOGLE GEMINI - RAG SYSTEM TEST")
print("="*80 + "\n")

# Check if API key is set
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("⚠️  GOOGLE_API_KEY not found in .env")
    print("\nTo get a FREE API key:")
    print("1. Visit: https://ai.google.dev/")
    print("2. Click 'Get API Key'")
    print("3. Create new API key (no payment required)")
    print("4. Add to .env: GOOGLE_API_KEY=<your-key>")
    print("\nThen run this script again.\n")
    exit(1)

print(f"✓ API Key found: {api_key[:20]}...{api_key[-10:]}\n")

# Test 1: Basic connection
print("1️⃣  TESTING GEMINI CONNECTION")
print("-" * 80)

try:
    from src.llm_gemini import GeminiClient
    client = GeminiClient(api_key=api_key)
    print("✓ GeminiClient initialized successfully\n")
except Exception as e:
    print(f"✗ Error initializing GeminiClient: {e}\n")
    print("Need to install google-generativeai? Run:")
    print("  pip install google-generativeai\n")
    exit(1)

# Test 2: Simple generation
print("2️⃣  TESTING BASIC GENERATION")
print("-" * 80)

try:
    response = client.generate("Explain machine learning in 2 sentences.")
    print(f"✓ Generated text:\n   {response[:200]}...\n")
except Exception as e:
    print(f"✗ Error: {e}\n")
    exit(1)

# Test 3: Load documents and test RAG
print("3️⃣  TESTING RAG WITH GEMINI")
print("-" * 80)

try:
    from src.ingestion import DocumentLoader
    from src.processing.chunker import SemanticChunker
    from src.retrieval import VectorStore
    
    # Load and process documents
    loader = DocumentLoader()
    documents = loader.load_directory("./data/documents")
    print(f"   Loaded {len(documents)} documents")
    
    chunker = SemanticChunker(chunk_size=1024, overlap=128)
    all_chunks = []
    for doc in documents:
        chunks = chunker.chunk(doc.content, metadata=doc.metadata)
        all_chunks.extend(chunks)
    print(f"   Created {len(all_chunks)} chunks")
    
    vector_store = VectorStore()
    vector_store.add_documents(all_chunks)
    print(f"   Indexed {len(all_chunks)} chunks in FAISS")
    
    # Test question
    query = "What is machine learning?"
    results = vector_store.search(query, top_k=2)
    context = "\n\n".join([content for content, _, _ in results])
    
    print(f"\n   Query: '{query}'")
    print("   " + "-" * 76)
    
    answer = client.query_with_context(query, context)
    print(f"   Gemini Answer:\n   {answer}\n")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Summarization
print("4️⃣  TESTING SUMMARIZATION")
print("-" * 80)

try:
    text = "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms and statistical models that allow computers to identify patterns in data."
    
    summary = client.summarize(text)
    print(f"   Original: {text[:100]}...")
    print(f"   Summary: {summary}\n")
    
except Exception as e:
    print(f"✗ Error: {e}\n")
    exit(1)

print("="*80)
print("✅ ALL TESTS PASSED - GEMINI IS READY!")
print("="*80)
print("\n📊 SUMMARY:")
print("   ✓ Gemini API Connection: WORKING")
print("   ✓ Basic Generation: WORKING")
print("   ✓ RAG with Context: WORKING")
print("   ✓ Summarization: WORKING")
print("\n🎉 Your RAG system now works with FREE Google Gemini API!\n")

