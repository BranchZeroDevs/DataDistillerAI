"""
Knowledge Graph Builder - Extract and visualize semantic relationships
Identifies concepts, entities, and their relationships in documents
"""

import logging
from typing import List, Dict, Tuple, Set
import spacy
import networkx as nx
from collections import defaultdict
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)


class KnowledgeGraphBuilder:
    """
    Builds semantic knowledge graphs from document chunks
    Extracts entities, key concepts, and their relationships
    """
    
    def __init__(self):
        """Initialize with spaCy NLP model and sentence embeddings"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Use smaller model for embeddings to save memory
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.graph = nx.DiGraph()
        self.entity_chunks = defaultdict(set)  # Track which chunks contain each entity
        
    def extract_entities_and_concepts(self, chunks: List) -> Dict:
        """
        Extract entities and key concepts from chunks
        
        Args:
            chunks: List of chunk objects with content
            
        Returns:
            Dictionary with entities and their properties
        """
        if self.nlp is None:
            raise RuntimeError("spaCy model not loaded")
        
        entities = defaultdict(lambda: {"type": None, "chunks": set(), "count": 0})
        concepts = defaultdict(lambda: {"chunks": set(), "count": 0})
        
        for i, chunk in enumerate(chunks):
            # Extract named entities
            doc = self.nlp(chunk.content[:5000])  # Limit to 5000 chars for speed
            
            # Add entities
            for ent in doc.ents:
                label = ent.label_
                text = ent.text.lower()
                
                entities[text]["type"] = label
                entities[text]["chunks"].add(i)
                entities[text]["count"] += 1
            
            # Extract noun phrases as concepts
            noun_phrases = self._extract_noun_phrases(doc)
            for phrase in noun_phrases:
                concepts[phrase]["chunks"].add(i)
                concepts[phrase]["count"] += 1
        
        return {
            "entities": dict(entities),
            "concepts": dict(concepts)
        }
    
    def _extract_noun_phrases(self, doc) -> List[str]:
        """Extract noun phrases from spaCy doc"""
        phrases = []
        for chunk in doc.noun_chunks:
            text = chunk.text.lower()
            if len(text.split()) <= 3 and len(text) > 3:  # 1-3 word phrases
                phrases.append(text)
        return phrases
    
    def build_graph(self, chunks: List, top_k: int = 50) -> nx.DiGraph:
        """
        Build knowledge graph with entities and concepts
        
        Args:
            chunks: Document chunks
            top_k: Keep top K most frequent entities/concepts
            
        Returns:
            NetworkX directed graph
        """
        logger.info("Extracting entities and concepts...")
        extracted = self.extract_entities_and_concepts(chunks)
        
        entities = extracted["entities"]
        concepts = extracted["concepts"]
        
        # Filter by frequency
        top_entities = sorted(
            entities.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:top_k]
        
        top_concepts = sorted(
            concepts.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:top_k]
        
        # Create graph nodes
        for entity, props in top_entities:
            self.graph.add_node(
                entity,
                type="entity",
                entity_type=props["type"],
                size=min(30 + props["count"] * 5, 80),
                color="#FF6B6B"  # Red for entities
            )
        
        for concept, props in top_concepts:
            self.graph.add_node(
                concept,
                type="concept",
                size=min(20 + props["count"] * 3, 60),
                color="#4ECDC4"  # Teal for concepts
            )
        
        logger.info("Building relationships...")
        # Build relationships based on co-occurrence in chunks
        all_items = list(top_entities) + list(top_concepts)
        all_texts = [text for text, _ in all_items]
        
        for i, chunk in enumerate(chunks):
            # Find which entities/concepts appear together in this chunk
            chunk_items = [
                text for text, props in all_items
                if i in props.get("chunks", set())
            ]
            
            # Create edges for co-occurring items
            for j, item1 in enumerate(chunk_items):
                for item2 in chunk_items[j + 1:]:
                    if self.graph.has_edge(item1, item2):
                        self.graph[item1][item2]["weight"] += 1
                    else:
                        self.graph.add_edge(item1, item2, weight=1)
                    
                    if self.graph.has_edge(item2, item1):
                        self.graph[item2][item1]["weight"] += 1
                    else:
                        self.graph.add_edge(item2, item1, weight=1)
        
        logger.info(f"Graph built: {self.graph.number_of_nodes()} nodes, {self.graph.number_of_edges()} edges")
        return self.graph
    
    def get_semantic_flow(self, chunks: List) -> List[Dict]:
        """
        Extract semantic flow - how ideas progress through document
        
        Args:
            chunks: Document chunks in order
            
        Returns:
            List of concept flows with progression
        """
        if self.nlp is None:
            raise RuntimeError("spaCy model not loaded")
        
        flows = []
        concepts_by_chunk = defaultdict(list)
        
        # Extract key concepts from each chunk
        for i, chunk in enumerate(chunks):
            doc = self.nlp(chunk.content[:3000])
            
            # Get important tokens/entities
            important = []
            for token in doc:
                if token.is_stop or token.is_punct:
                    continue
                if token.pos_ in ["NOUN", "VERB", "ADJ"]:
                    important.append(token.text.lower())
            
            concepts_by_chunk[i] = list(set(important))
        
        # Track concept progression
        prev_concepts = set()
        for i in sorted(concepts_by_chunk.keys()):
            current = set(concepts_by_chunk[i])
            
            # Find new and continuing concepts
            new_concepts = current - prev_concepts
            continuing = current & prev_concepts
            
            if new_concepts or continuing:
                flows.append({
                    "chunk": i,
                    "new": list(new_concepts)[:5],  # Top 5 new
                    "continuing": list(continuing)[:3],  # Top 3 continuing
                    "total": len(current)
                })
            
            prev_concepts = current
        
        return flows
    
    def get_node_importance(self) -> Dict[str, float]:
        """
        Calculate node importance using PageRank
        
        Returns:
            Dictionary of node importance scores
        """
        if self.graph.number_of_nodes() == 0:
            return {}
        
        return nx.pagerank(self.graph)
    
    def find_concept_clusters(self) -> List[Set]:
        """
        Find clusters of related concepts
        
        Returns:
            List of concept clusters (sets of related terms)
        """
        if self.graph.number_of_nodes() < 3:
            return []
        
        # Convert to undirected for community detection
        undirected = self.graph.to_undirected()
        
        try:
            from networkx.algorithms import community
            communities = list(community.greedy_modularity_communities(undirected))
            return [set(c) for c in communities]
        except ImportError:
            logger.warning("Community detection requires networkx[all]")
            return []
    
    def export_html(self, filepath: str = "knowledge_graph.html"):
        """
        Export graph as interactive HTML using pyvis
        
        Args:
            filepath: Output HTML file path
        """
        try:
            from pyvis.network import Network
            
            # Create pyvis network
            net = Network(height="750px", directed=True)
            
            # Add nodes with properties
            for node, attrs in self.graph.nodes(data=True):
                net.add_node(
                    node,
                    label=node,
                    title=f"{node} ({attrs.get('entity_type', 'concept')})",
                    size=attrs.get('size', 25),
                    color=attrs.get('color', '#95E1D3'),
                    physics=True
                )
            
            # Add edges with weights
            for source, target, attrs in self.graph.edges(data=True):
                weight = attrs.get('weight', 1)
                net.add_edge(source, target, value=min(weight, 5), width=min(weight * 0.5, 3))
            
            # Configure physics
            net.set_options("""
            {
                "physics": {
                    "enabled": true,
                    "stabilization": {
                        "iterations": 200
                    },
                    "barnesHut": {
                        "gravitationalConstant": -30000,
                        "centralGravity": 0.3,
                        "springLength": 200,
                        "springConstant": 0.04
                    }
                }
            }
            """)
            
            net.show(filepath)
            logger.info(f"Graph exported to {filepath}")
            
        except ImportError:
            logger.error("pyvis not installed. Install with: pip install pyvis")
        except Exception as e:
            logger.error(f"Error exporting graph: {e}")


# Export
__all__ = ['KnowledgeGraphBuilder']
