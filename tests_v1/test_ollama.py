#!/usr/bin/env python3
"""
Test script for Ollama integration with DataDistillerAI RAG system
Completely local, no API keys needed, no quotas!
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path('.env'))

print("\n" + "="*80)
print("🦙 OLLAMA - RAG SYSTEM TEST (100% LOCAL & FREE)")
print("="*80 + "\n")

# Check if Ollama is running
print("1️⃣  CHECKING OLLAMA CONNECTION")
print("-" * 80)

try:
    from src.llm_ollama import OllamaClient
    
    # Try to connect with qwen2.5 (fast & good quality)
    client = OllamaClient(model="qwen2.5")
    print("✓ Ollama server is running and connected")
    
    # List available models
    models = client.list_available_models()
    print(f"✓ Available models: {', '.join([m.split(':')[0] for m in models]) if models else 'None'}\n")
    
except ConnectionError as e:
    print(f"✗ Cannot connect to Ollama: {e}")
    print("\nTo start Ollama, run in a new terminal:")
    print("  ollama serve")
    print("\nTo pull a model (if not already done):")
    print("  ollama pull mistral")
    exit(1)
except ValueError as e:
    print(f"✗ Model not found: {e}")
    print("\nTo pull mistral model, run:")
    print("  ollama pull mistral")
    exit(1)
except Exception as e:
    print(f"✗ Error: {e}\n")
    exit(1)

# Test 2: Simple generation
print("2️⃣  TESTING BASIC TEXT GENERATION")
print("-" * 80)

try:
    print("   Generating text (this may take 10-30 seconds)...")
    response = client.generate("Explain machine learning in 2 sentences.")
    print(f"✓ Generated text:\n   {response}\n")
except Exception as e:
    print(f"✗ Error: {e}\n")
    exit(1)

# Test 3: Load documents and test RAG
print("3️⃣  TESTING RAG WITH OLLAMA")
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
    query = "What is machine learning?"
    results = vector_store.search(query, top_k=2)
    context = "\n\n".join([content for content, _, _ in results])
    
    print(f"   Query: '{query}'")
    print("   " + "-" * 76)
    print("   Generating answer with Ollama (this may take 30-60 seconds)...")
    
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
    text = "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms and statistical models that allow computers to identify patterns in data."
    
    print("   Summarizing text (this may take 20-40 seconds)...")
    summary = client.summarize(text)
    print(f"   Original: {text[:100]}...")
    print(f"   Summary: {summary}\n")
    
except Exception as e:
    print(f"✗ Error: {e}\n")
    exit(1)

print("="*80)
print("✅ ALL TESTS PASSED - OLLAMA IS WORKING!")
print("="*80)
print("\n📊 SUMMARY:")
print("   ✓ Ollama Server: CONNECTED")
print("   ✓ Basic Generation: WORKING")
print("   ✓ RAG with Context: WORKING")
print("   ✓ Summarization: WORKING")
print("\n💰 COST: $0 (100% free, runs locally)")
print("🚀 PERFORMANCE: Fast on CPU, instant with GPU")
print("🔐 PRIVACY: All data stays on your machine\n")

