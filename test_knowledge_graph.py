#!/usr/bin/env python3
"""
Test Knowledge Graph Builder
Demonstrates semantic relationship extraction and visualization
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path('.env'))

print("\n" + "="*80)
print("🧠 KNOWLEDGE GRAPH BUILDER TEST")
print("="*80 + "\n")

# Test 1: Load documents
print("1️⃣  LOADING DOCUMENTS")
print("-" * 80)

try:
    from src.ingestion import DocumentLoader
    from src.processing.chunker import SemanticChunker
    
    loader = DocumentLoader()
    documents = loader.load_directory("./data/documents")
    print(f"✓ Loaded {len(documents)} documents\n")
    
    # Chunk documents
    chunker = SemanticChunker(chunk_size=1024, overlap=128)
    all_chunks = []
    for doc in documents:
        chunks = chunker.chunk(doc.content, metadata=doc.metadata)
        all_chunks.extend(chunks)
    
    print(f"✓ Created {len(all_chunks)} chunks\n")
    
except Exception as e:
    print(f"✗ Error: {e}\n")
    exit(1)

# Test 2: Build knowledge graph
print("2️⃣  BUILDING KNOWLEDGE GRAPH")
print("-" * 80)

try:
    from src.knowledge_graph import KnowledgeGraphBuilder
    
    kg = KnowledgeGraphBuilder()
    graph = kg.build_graph(all_chunks)
    
    print(f"✓ Graph built with {graph.number_of_nodes()} concepts")
    print(f"✓ Found {graph.number_of_edges()} relationships\n")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("  Install spaCy model: python -m spacy download en_core_web_sm\n")
    exit(1)

# Test 3: Concept importance
print("3️⃣  ANALYZING CONCEPT IMPORTANCE")
print("-" * 80)

try:
    importance = kg.get_node_importance()
    
    if importance:
        top_10 = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:10]
        
        print("Top 10 Most Important Concepts:\n")
        for i, (concept, score) in enumerate(top_10, 1):
            print(f"  {i:2d}. {concept.title():30s} | Importance: {score:.2%}")
        
        print()
    
except Exception as e:
    print(f"✗ Error: {e}\n")

# Test 4: Concept clusters
print("4️⃣  FINDING CONCEPT CLUSTERS")
print("-" * 80)

try:
    clusters = kg.find_concept_clusters()
    
    print(f"✓ Found {len(clusters)} concept clusters\n")
    
    for i, cluster in enumerate(clusters[:5], 1):
        print(f"  Cluster {i}: {', '.join(sorted(list(cluster))[:5])}...")
    
    print()
    
except Exception as e:
    print(f"⚠️  Could not find clusters: {e}\n")

# Test 5: Semantic flow
print("5️⃣  ANALYZING SEMANTIC FLOW")
print("-" * 80)

try:
    flows = kg.get_semantic_flow(all_chunks)
    
    print(f"✓ Analyzed semantic flow across {len(flows)} chunks\n")
    
    print("Sample Flow (first 3 chunks):\n")
    for flow in flows[:3]:
        print(f"  Chunk {flow['chunk']}:")
        if flow['new']:
            print(f"    New: {', '.join(flow['new'][:3])}")
        if flow['continuing']:
            print(f"    Continuing: {', '.join(flow['continuing'][:2])}")
        print()
    
except Exception as e:
    print(f"✗ Error: {e}\n")

# Test 6: Export graph
print("6️⃣  EXPORTING INTERACTIVE GRAPH")
print("-" * 80)

try:
    kg.export_html("knowledge_graph.html")
    print("✓ Graph exported to knowledge_graph.html")
    print("  Open in browser to explore interactive visualization\n")
    
except Exception as e:
    print(f"⚠️  Could not export graph: {e}\n")

print("="*80)
print("✅ KNOWLEDGE GRAPH TEST COMPLETE")
print("="*80)
print("\n📊 SUMMARY:")
print(f"   ✓ Documents loaded: {len(documents)}")
print(f"   ✓ Chunks created: {len(all_chunks)}")
print(f"   ✓ Concepts found: {graph.number_of_nodes()}")
print(f"   ✓ Relationships: {graph.number_of_edges()}")
print(f"   ✓ Clusters: {len(clusters) if 'clusters' in locals() else 'N/A'}")

print("\n💡 NEXT STEPS:")
print("   1. View interactive graph: Open knowledge_graph.html in browser")
print("   2. Drag nodes to explore connections")
print("   3. Use in Streamlit app: streamlit run app.py")
print("   4. Click 'Knowledge Graph' tab for semantic visualization\n")
