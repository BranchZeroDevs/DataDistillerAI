#!/usr/bin/env python3
"""
PHASE 3: Semantic Flow - Chunk-wise Concept Progression
Visualizes how ideas progress through documents sequentially
"""

import logging
from pathlib import Path
from typing import List, Dict, Set, Tuple
import pandas as pd
import streamlit as st

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class SemanticFlowAnalyzer:
    """Analyze how concepts flow through document chunks"""
    
    def __init__(self, builder):
        """
        Initialize with a KnowledgeGraphBuilder
        
        Args:
            builder: SimpleKnowledgeGraphBuilder instance with graph already built
        """
        self.builder = builder
        self.graph = builder.graph
    
    def analyze_chunk_progression(self, chunks: List, top_k: int = 20) -> Dict:
        """
        Analyze how concepts progress through chunks
        
        Args:
            chunks: List of document chunks
            top_k: Number of top concepts to track
            
        Returns:
            Dictionary with flow analysis data
        """
        logger.info("Analyzing semantic flow through chunks...")
        
        # Get top concepts to track
        top_concepts = self.builder.get_top_concepts(top_k)
        top_concept_names = set(concept for concept, _ in top_concepts)
        
        # Track concepts per chunk
        chunk_data = []
        all_seen_concepts = set()
        
        for i, chunk in enumerate(chunks):
            content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            doc = self.builder.nlp(content[:5000])
            
            # Find concepts in this chunk
            chunk_concepts = set()
            
            # Add entities
            for ent in doc.ents:
                text = ent.text.lower().strip()
                if text in top_concept_names:
                    chunk_concepts.add(text)
            
            # Add noun phrases
            for chunk_np in doc.noun_chunks:
                text = chunk_np.text.lower().strip()
                if text in top_concept_names:
                    chunk_concepts.add(text)
            
            # Categorize concepts
            new_concepts = chunk_concepts - all_seen_concepts
            continuing_concepts = chunk_concepts & all_seen_concepts
            
            chunk_data.append({
                'chunk_id': i,
                'chunk_name': f"Chunk {i+1}",
                'all_concepts': chunk_concepts,
                'new_concepts': new_concepts,
                'continuing_concepts': continuing_concepts,
                'total_count': len(chunk_concepts),
                'new_count': len(new_concepts),
                'continuing_count': len(continuing_concepts)
            })
            
            # Update seen concepts
            all_seen_concepts.update(chunk_concepts)
        
        logger.info(f"✅ Analyzed {len(chunks)} chunks")
        
        return {
            'chunks': chunk_data,
            'tracked_concepts': top_concept_names,
            'total_chunks': len(chunks)
        }
    
    def get_concept_timeline(self, chunks: List, top_k: int = 10) -> pd.DataFrame:
        """
        Create a timeline showing when each concept appears
        
        Returns:
            DataFrame with chunks as rows, concepts as columns (1 if present, 0 if not)
        """
        flow_data = self.analyze_chunk_progression(chunks, top_k)
        
        # Create matrix of concepts x chunks
        concepts = sorted(flow_data['tracked_concepts'])
        chunk_ids = list(range(len(chunks)))
        
        # Build dataframe
        data = []
        for chunk_info in flow_data['chunks']:
            row = {concept: (1 if concept in chunk_info['all_concepts'] else 0) 
                   for concept in concepts}
            row['Chunk'] = chunk_info['chunk_name']
            data.append(row)
        
        df = pd.DataFrame(data)
        df = df.set_index('Chunk')
        
        return df


def display_semantic_flow_tab(pipeline, builder):
    """Display Semantic Flow analysis in Streamlit"""
    st.subheader("💡 Semantic Flow Analysis")
    
    st.markdown("""
    Track how concepts progress through your documents chunk by chunk.
    See which ideas are introduced, which continue, and how knowledge builds.
    """)
    
    # Get chunks
    try:
        chunks = pipeline.vector_store.get_all_documents()
        
        if not chunks:
            st.warning("No chunks available. Please index documents first.")
            return
        
        if len(chunks) < 2:
            st.info("Need at least 2 chunks for flow analysis. Add more documents!")
            return
        
        st.info(f"📊 Analyzing flow across {len(chunks)} chunks")
        
    except Exception as e:
        st.error(f"Error getting chunks: {e}")
        return
    
    # Create analyzer
    analyzer = SemanticFlowAnalyzer(builder)
    
    # Analyze flow
    with st.spinner("Analyzing semantic flow..."):
        flow_data = analyzer.analyze_chunk_progression(chunks, top_k=15)
    
    # Display chunk-by-chunk progression
    st.markdown("### 📊 Chunk-by-Chunk Progression")
    
    # Create metrics
    col1, col2, col3 = st.columns(3)
    
    total_new = sum(c['new_count'] for c in flow_data['chunks'])
    avg_concepts_per_chunk = sum(c['total_count'] for c in flow_data['chunks']) / len(flow_data['chunks'])
    max_chunk = max(flow_data['chunks'], key=lambda x: x['total_count'])
    
    with col1:
        st.metric("Total Unique Concepts", len(flow_data['tracked_concepts']))
    
    with col2:
        st.metric("Avg Concepts/Chunk", f"{avg_concepts_per_chunk:.1f}")
    
    with col3:
        st.metric("Richest Chunk", max_chunk['chunk_name'])
    
    st.markdown("---")
    
    # Progression chart
    st.markdown("### 📈 Concept Count Over Chunks")
    
    chart_data = pd.DataFrame([
        {
            'Chunk': c['chunk_name'],
            'New Concepts': c['new_count'],
            'Continuing Concepts': c['continuing_count']
        }
        for c in flow_data['chunks']
    ])
    
    st.bar_chart(chart_data.set_index('Chunk'))
    
    st.markdown("---")
    
    # Detailed chunk breakdown
    st.markdown("### 🔍 Detailed Chunk Analysis")
    
    for chunk_info in flow_data['chunks']:
        with st.expander(f"📄 {chunk_info['chunk_name']} - {chunk_info['total_count']} concepts"):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**🆕 New Concepts ({chunk_info['new_count']})**")
                if chunk_info['new_concepts']:
                    for concept in sorted(chunk_info['new_concepts']):
                        st.write(f"• {concept}")
                else:
                    st.write("*None*")
            
            with col2:
                st.markdown(f"**🔄 Continuing Concepts ({chunk_info['continuing_count']})**")
                if chunk_info['continuing_concepts']:
                    for concept in sorted(chunk_info['continuing_concepts']):
                        st.write(f"• {concept}")
                else:
                    st.write("*None*")
    
    # Concept timeline
    st.markdown("---")
    st.markdown("### 📅 Concept Timeline")
    st.markdown("Shows when each concept appears across chunks (✓ = present)")
    
    timeline_df = analyzer.get_concept_timeline(chunks, top_k=10)
    
    # Format for display
    display_df = timeline_df.replace({1: '✓', 0: '·'})
    st.dataframe(display_df, width='stretch')
    
    # Heatmap
    st.markdown("### 🔥 Concept Presence Heatmap")
    st.markdown("Darker = concept is present in that chunk")
    
    import numpy as np
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(timeline_df.T, cmap='YlOrRd', aspect='auto')
    
    ax.set_yticks(np.arange(len(timeline_df.columns)))
    ax.set_yticklabels(timeline_df.columns)
    ax.set_xticks(np.arange(len(timeline_df)))
    ax.set_xticklabels(timeline_df.index, rotation=45, ha='right')
    
    plt.colorbar(im, ax=ax, label='Present (1) / Absent (0)')
    plt.tight_layout()
    
    st.pyplot(fig)


def test_phase3():
    """Test Phase 3 - Semantic Flow"""
    logger.info("=" * 70)
    logger.info("PHASE 3: SEMANTIC FLOW TEST")
    logger.info("=" * 70)
    
    # Load graph from Phase 1
    logger.info("\n1. Loading knowledge graph...")
    try:
        from test_kg_phase1 import SimpleKnowledgeGraphBuilder
        from pathlib import Path
        
        # Load documents
        doc_path = Path("data/documents")
        
        class SimpleChunk:
            def __init__(self, content):
                self.content = content
        
        chunks = []
        for doc_file in doc_path.glob("*.txt"):
            with open(doc_file, 'r') as f:
                # Split into chunks (simulate real chunking)
                content = f.read()
                # Simple split by paragraphs
                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                for para in paragraphs:
                    if len(para) > 100:  # Only keep substantial paragraphs
                        chunks.append(SimpleChunk(para))
        
        logger.info(f"  Loaded {len(chunks)} chunks")
        
        builder = SimpleKnowledgeGraphBuilder()
        graph = builder.build_graph(chunks, top_k=20)
        logger.info(f"✅ Graph built")
    except Exception as e:
        logger.error(f"❌ Error loading graph: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test semantic flow analysis
    logger.info("\n2. Analyzing semantic flow...")
    try:
        analyzer = SemanticFlowAnalyzer(builder)
        flow_data = analyzer.analyze_chunk_progression(chunks, top_k=15)
        
        logger.info(f"✅ Flow analysis complete")
        logger.info(f"  Tracked {len(flow_data['tracked_concepts'])} concepts")
        logger.info(f"  Across {flow_data['total_chunks']} chunks")
    except Exception as e:
        logger.error(f"❌ Error analyzing flow: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Display results
    logger.info("\n3. Chunk-by-chunk progression:")
    for chunk_info in flow_data['chunks'][:5]:  # Show first 5
        logger.info(f"\n  {chunk_info['chunk_name']}:")
        logger.info(f"    Total: {chunk_info['total_count']} concepts")
        logger.info(f"    New: {chunk_info['new_count']}")
        logger.info(f"    Continuing: {chunk_info['continuing_count']}")
        
        if chunk_info['new_concepts']:
            logger.info(f"    🆕 New: {', '.join(list(chunk_info['new_concepts'])[:3])}")
    
    # Test timeline
    logger.info("\n4. Testing concept timeline...")
    try:
        timeline_df = analyzer.get_concept_timeline(chunks, top_k=10)
        logger.info(f"✅ Timeline created: {timeline_df.shape}")
        logger.info(f"  Concepts: {len(timeline_df.columns)}")
        logger.info(f"  Chunks: {len(timeline_df)}")
    except Exception as e:
        logger.error(f"❌ Error creating timeline: {e}")
        return False
    
    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("✅ PHASE 3 COMPLETE - SEMANTIC FLOW WORKING")
    logger.info("=" * 70)
    logger.info("\nPhase 3 Results:")
    logger.info(f"  • Tracked concept progression through {flow_data['total_chunks']} chunks")
    logger.info(f"  • Identified new vs continuing concepts")
    logger.info(f"  • Created timeline visualization")
    logger.info(f"  • Ready for Streamlit integration")
    logger.info("\nNext: Integrate into Streamlit app as 4th view in Knowledge Graph tab")
    
    return True


if __name__ == "__main__":
    success = test_phase3()
    exit(0 if success else 1)
