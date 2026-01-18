#!/usr/bin/env python3
"""
PHASE 1: Core Knowledge Graph Builder
Tests: Entity/concept extraction + basic graph building
"""

import logging
from pathlib import Path
from typing import List, Dict, Tuple
import spacy
import networkx as nx
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class SimpleKnowledgeGraphBuilder:
    """Phase 1: Simple, working knowledge graph builder"""
    
    def __init__(self):
        """Initialize with spaCy"""
        logger.info("Loading spaCy model...")
        self.nlp = spacy.load("en_core_web_sm")
        self.graph = nx.DiGraph()
        logger.info("✅ Knowledge graph builder initialized")
    
    def extract_entities_and_concepts(self, chunks: List) -> Dict:
        """Extract entities and noun phrases from chunks"""
        logger.info("Extracting entities and concepts...")
        
        entities = defaultdict(lambda: {"type": None, "chunks": set(), "count": 0})
        concepts = defaultdict(lambda: {"chunks": set(), "count": 0})
        
        for i, chunk in enumerate(chunks):
            # Get content from chunk object
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            
            # Process with spaCy
            doc = self.nlp(content[:5000])  # Limit to 5000 chars for speed
            
            # Extract named entities
            for ent in doc.ents:
                label = ent.label_
                text = ent.text.lower().strip()
                
                if len(text) > 2:  # Skip very short entities
                    entities[text]["type"] = label
                    entities[text]["chunks"].add(i)
                    entities[text]["count"] += 1
            
            # Extract noun phrases as concepts
            for chunk_np in doc.noun_chunks:
                text = chunk_np.text.lower().strip()
                if 3 <= len(text) <= 50 and len(text.split()) <= 4:  # 1-4 word phrases, 3-50 chars
                    concepts[text]["chunks"].add(i)
                    concepts[text]["count"] += 1
        
        logger.info(f"  Found {len(entities)} entities")
        logger.info(f"  Found {len(concepts)} concepts")
        
        return {
            "entities": dict(entities),
            "concepts": dict(concepts)
        }
    
    def build_graph(self, chunks: List, top_k: int = 30) -> nx.DiGraph:
        """Build knowledge graph from chunks"""
        logger.info("Building knowledge graph...")
        
        # Extract entities and concepts
        extracted = self.extract_entities_and_concepts(chunks)
        
        entities = extracted["entities"]
        concepts = extracted["concepts"]
        
        # Combine and sort by frequency
        all_nodes = {}
        for text, data in entities.items():
            all_nodes[text] = {
                "type": "entity",
                "entity_type": data["type"],
                "count": data["count"],
                "chunks": data["chunks"]
            }
        
        for text, data in concepts.items():
            all_nodes[text] = {
                "type": "concept",
                "count": data["count"],
                "chunks": data["chunks"]
            }
        
        # Keep top K nodes by frequency
        top_nodes = sorted(all_nodes.items(), key=lambda x: x[1]["count"], reverse=True)[:top_k]
        top_node_texts = set(text for text, _ in top_nodes)
        
        logger.info(f"  Keeping top {len(top_nodes)} nodes")
        
        # Add nodes to graph
        for text, data in top_nodes:
            self.graph.add_node(
                text,
                count=data["count"],
                type=data["type"],
                entity_type=data.get("entity_type", None),
                chunks=len(data["chunks"])
            )
        
        # Build edges based on co-occurrence in chunks
        logger.info("Building relationships...")
        edge_count = 0
        
        for i, chunk in enumerate(chunks):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            doc = self.nlp(content[:5000])
            
            # Get all node texts in this chunk
            chunk_nodes = []
            
            # Add entities in chunk
            for ent in doc.ents:
                text = ent.text.lower().strip()
                if text in top_node_texts:
                    chunk_nodes.append(text)
            
            # Add concepts in chunk
            for chunk_np in doc.noun_chunks:
                text = chunk_np.text.lower().strip()
                if text in top_node_texts:
                    chunk_nodes.append(text)
            
            # Create edges between co-occurring nodes
            for j, source in enumerate(chunk_nodes):
                for target in chunk_nodes[j+1:]:
                    if source != target:
                        if self.graph.has_edge(source, target):
                            self.graph[source][target]['weight'] += 1
                        else:
                            self.graph.add_edge(source, target, weight=1)
                            edge_count += 1
        
        logger.info(f"  Created {edge_count} relationships")
        logger.info(f"✅ Graph built: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
        
        return self.graph
    
    def get_importance_scores(self) -> Dict[str, float]:
        """Calculate importance of nodes using PageRank"""
        logger.info("Calculating importance scores...")
        if self.graph.number_of_nodes() == 0:
            return {}
        
        try:
            scores = nx.pagerank(self.graph)
            return scores
        except Exception as e:
            logger.error(f"Error calculating PageRank: {e}")
            return {}
    
    def get_top_concepts(self, n: int = 10) -> List[Tuple[str, float]]:
        """Get top N concepts by importance"""
        scores = self.get_importance_scores()
        top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:n]
        return top
    
    def get_graph_stats(self) -> Dict:
        """Get basic graph statistics"""
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
            "avg_clustering": nx.average_clustering(self.graph.to_undirected()) if self.graph.number_of_nodes() > 0 else 0
        }


def test_phase1():
    """Test Phase 1 functionality"""
    logger.info("=" * 70)
    logger.info("PHASE 1: KNOWLEDGE GRAPH BUILDER TEST")
    logger.info("=" * 70)
    
    # Load sample documents
    logger.info("\n1. Loading sample documents...")
    doc_path = Path("data/documents")
    
    if not doc_path.exists():
        logger.error(f"❌ Document directory not found: {doc_path}")
        return False
    
    # Simple chunk-like objects
    class SimpleChunk:
        def __init__(self, content):
            self.content = content
    
    chunks = []
    doc_count = 0
    
    for doc_file in doc_path.glob("*.txt"):
        try:
            with open(doc_file, 'r') as f:
                content = f.read()
                chunks.append(SimpleChunk(content))
                doc_count += 1
                logger.info(f"  ✅ Loaded {doc_file.name} ({len(content)} chars)")
        except Exception as e:
            logger.error(f"  ❌ Error loading {doc_file.name}: {e}")
    
    if not chunks:
        logger.error("❌ No documents loaded")
        return False
    
    logger.info(f"✅ Loaded {doc_count} documents ({len(chunks)} chunks)")
    
    # Test graph builder
    logger.info("\n2. Building knowledge graph...")
    try:
        builder = SimpleKnowledgeGraphBuilder()
        graph = builder.build_graph(chunks)
        logger.info("✅ Graph built successfully")
    except Exception as e:
        logger.error(f"❌ Error building graph: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test statistics
    logger.info("\n3. Graph statistics...")
    try:
        stats = builder.get_graph_stats()
        logger.info(f"  Nodes: {stats['nodes']}")
        logger.info(f"  Edges: {stats['edges']}")
        logger.info(f"  Density: {stats['density']:.4f}")
        logger.info(f"  Avg Clustering: {stats['avg_clustering']:.4f}")
        logger.info("✅ Statistics calculated")
    except Exception as e:
        logger.error(f"❌ Error calculating stats: {e}")
        return False
    
    # Test top concepts
    logger.info("\n4. Top concepts by importance...")
    try:
        top = builder.get_top_concepts(10)
        if top:
            for i, (concept, score) in enumerate(top, 1):
                logger.info(f"  {i:2}. {concept:30} {score:.4f}")
            logger.info("✅ Top concepts retrieved")
        else:
            logger.warning("⚠️  No top concepts found")
    except Exception as e:
        logger.error(f"❌ Error getting top concepts: {e}")
        return False
    
    # Test exporting graph
    logger.info("\n5. Testing graph export...")
    try:
        import json
        export_path = Path("data/knowledge_graph_phase1.json")
        
        # Export as JSON
        node_data = {}
        for node in graph.nodes():
            node_data[node] = {
                "attributes": dict(graph.nodes[node]),
                "connections": list(graph.successors(node))
            }
        
        with open(export_path, 'w') as f:
            json.dump(node_data, f, indent=2, default=str)
        
        logger.info(f"✅ Graph exported to {export_path}")
    except Exception as e:
        logger.error(f"❌ Error exporting: {e}")
        return False
    
    # Final summary
    logger.info("\n" + "=" * 70)
    logger.info("✅ PHASE 1 COMPLETE - ALL TESTS PASSED")
    logger.info("=" * 70)
    logger.info("\nPhase 1 Results:")
    logger.info(f"  • Knowledge graph built with {stats['nodes']} concepts")
    logger.info(f"  • {stats['edges']} semantic relationships discovered")
    logger.info(f"  • Top concept: {top[0][0]}")
    logger.info(f"  • Graph data exported for visualization")
    logger.info("\nNext: Phase 2 - Interactive visualization with Streamlit")
    
    return True


if __name__ == "__main__":
    success = test_phase1()
    exit(0 if success else 1)
