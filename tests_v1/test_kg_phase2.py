#!/usr/bin/env python3
"""
PHASE 2: Interactive Knowledge Graph Visualization
Adds interactive network graph to Streamlit app
"""

import streamlit as st
from pathlib import Path
import logging
from pyvis.network import Network
import tempfile

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def create_interactive_graph(graph, title="Knowledge Graph"):
    """
    Create interactive pyvis network from NetworkX graph
    
    Args:
        graph: NetworkX graph
        title: Title for the visualization
        
    Returns:
        HTML string of the interactive graph
    """
    # Create pyvis network
    net = Network(
        height="600px",
        width="100%",
        bgcolor="#ffffff",
        font_color="#000000",
        notebook=False
    )
    
    # Set physics for better layout
    net.barnes_hut(
        gravity=-5000,
        central_gravity=0.3,
        spring_length=100,
        spring_strength=0.01,
        damping=0.09
    )
    
    # Get node importance scores (using PageRank)
    try:
        import networkx as nx
        importance = nx.pagerank(graph)
    except:
        importance = {node: 1.0 for node in graph.nodes()}
    
    # Normalize importance for sizing
    max_importance = max(importance.values()) if importance else 1.0
    min_importance = min(importance.values()) if importance else 0.0
    importance_range = max_importance - min_importance if max_importance != min_importance else 1.0
    
    # Add nodes
    for node in graph.nodes():
        node_data = graph.nodes[node]
        node_importance = importance.get(node, 0.5)
        
        # Size based on importance (10-40)
        normalized_importance = (node_importance - min_importance) / importance_range
        size = 10 + (normalized_importance * 30)
        
        # Color based on type
        node_type = node_data.get('type', 'concept')
        if node_type == 'entity':
            color = '#e74c3c'  # Red for entities
        else:
            color = '#3498db'  # Blue for concepts
        
        # Title (hover text)
        count = node_data.get('count', 0)
        chunks = node_data.get('chunks', 0)
        entity_type = node_data.get('entity_type', '')
        
        title = f"{node}\n"
        title += f"Importance: {node_importance:.4f}\n"
        title += f"Occurrences: {count}\n"
        title += f"Chunks: {chunks}"
        if entity_type:
            title += f"\nType: {entity_type}"
        
        net.add_node(
            node,
            label=node,
            title=title,
            size=size,
            color=color
        )
    
    # Add edges
    for source, target, data in graph.edges(data=True):
        weight = data.get('weight', 1)
        
        # Edge width based on weight (1-5)
        width = min(1 + (weight / 2), 5)
        
        net.add_edge(
            source,
            target,
            value=weight,
            title=f"Connection strength: {weight}",
            width=width
        )
    
    # Generate HTML
    try:
        # Use temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as f:
            net.save_graph(f.name)
            with open(f.name, 'r') as html_file:
                html_content = html_file.read()
        
        return html_content
    
    except Exception as e:
        logger.error(f"Error generating graph HTML: {e}")
        return None


def display_knowledge_graph_tab(pipeline):
    """Display Knowledge Graph tab in Streamlit"""
    st.header("🧠 Knowledge Graph Visualization")
    
    st.markdown("""
    Explore the semantic relationships between concepts in your documents.
    The graph shows how ideas connect and which concepts are most important.
    """)
    
    # Build graph button
    if st.button("🔄 Build/Rebuild Knowledge Graph", key="build_kg"):
        with st.spinner("🧠 Building knowledge graph..."):
            try:
                # Import the builder
                from tests_v1.test_kg_phase1 import SimpleKnowledgeGraphBuilder
                
                # Get chunks from vector store
                chunks = pipeline.vector_store.get_all_documents()
                
                if not chunks:
                    st.error("❌ No documents indexed yet. Please index documents first in the Documents tab.")
                    return
                
                # Build graph
                builder = SimpleKnowledgeGraphBuilder()
                graph = builder.build_graph(chunks, top_k=30)
                
                # Store in session state
                st.session_state.kg_graph = graph
                st.session_state.kg_builder = builder
                
                st.success(f"✅ Knowledge graph built: {graph.number_of_nodes()} concepts, {graph.number_of_edges()} relationships")
            
            except Exception as e:
                st.error(f"❌ Error building knowledge graph: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
                return
    
    # Check if graph exists
    if 'kg_graph' not in st.session_state:
        st.info("👆 Click 'Build/Rebuild Knowledge Graph' to get started")
        return
    
    graph = st.session_state.kg_graph
    builder = st.session_state.kg_builder
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌐 Network Graph", "📊 Statistics", "🔝 Top Concepts", "💡 Semantic Flow", "🤖 AI Progression"])
    
    # TAB 1: Interactive Network
    with tab1:
        st.subheader("Interactive Network Visualization")
        
        st.markdown("""
        **How to use:**
        - 🖱️ **Drag nodes** to rearrange
        - 🔍 **Zoom** with mouse wheel
        - 👆 **Click nodes** to see details
        - 🔴 **Red nodes**: Named entities (people, places, etc.)
        - 🔵 **Blue nodes**: Concepts and ideas
        - **Larger nodes**: More important concepts
        - **Thicker edges**: Stronger relationships
        """)
        
        # Generate and display graph
        with st.spinner("Rendering graph..."):
            html_content = create_interactive_graph(graph)
            
            if html_content:
                # Display using components
                import streamlit.components.v1 as components
                components.html(html_content, height=620, scrolling=False)
            else:
                st.error("Error rendering graph visualization")
    
    # TAB 2: Statistics
    with tab2:
        st.subheader("Graph Statistics")
        
        stats = builder.get_graph_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Nodes", stats['nodes'])
        
        with col2:
            st.metric("Relationships", stats['edges'])
        
        with col3:
            st.metric("Density", f"{stats['density']:.3f}")
        
        with col4:
            st.metric("Clustering", f"{stats['avg_clustering']:.3f}")
        
        st.markdown("---")
        
        # Explanations
        st.markdown("""
        **What these metrics mean:**
        
        - **Nodes**: Number of key concepts extracted from your documents
        - **Relationships**: Number of connections between concepts
        - **Density**: How interconnected the graph is (0-1, higher = more connected)
        - **Clustering**: How concepts group together (0-1, higher = more clustered)
        """)
    
    # TAB 3: Top Concepts
    with tab3:
        st.subheader("Most Important Concepts")
        
        st.markdown("""
        Ranked by **PageRank** importance - concepts that are central to your documents.
        """)
        
        top_concepts = builder.get_top_concepts(20)
        
        if top_concepts:
            # Create a nice table
            import pandas as pd
            
            df = pd.DataFrame(
                [(i+1, concept, f"{score:.4f}", f"{score*100:.2f}%") 
                 for i, (concept, score) in enumerate(top_concepts)],
                columns=["Rank", "Concept", "Score", "Importance %"]
            )
            
            st.dataframe(df, width='stretch', hide_index=True)
            
            # Bar chart
            st.markdown("### Importance Distribution")
            chart_data = pd.DataFrame({
                'Concept': [c for c, _ in top_concepts[:10]],
                'Importance': [s for _, s in top_concepts[:10]]
            })
            st.bar_chart(chart_data.set_index('Concept'))
        
        else:
            st.warning("No concept importance data available")
    
    # TAB 4: Semantic Flow
    with tab4:
        from test_kg_phase3 import display_semantic_flow_tab
        
        # Get chunks
        try:
            chunks = pipeline.vector_store.get_all_documents()
            display_semantic_flow_tab(pipeline, builder)
        except Exception as e:
            st.error(f"Error loading semantic flow: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    # TAB 5: AI-Enhanced Progression
    with tab5:
        from test_kg_phase4 import display_ai_progression_tab
        
        try:
            display_ai_progression_tab(pipeline, builder)
        except Exception as e:
            st.error(f"Error loading AI progression: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


def test_phase2():
    """Test Phase 2 - visualization generation"""
    logger.info("=" * 70)
    logger.info("PHASE 2: INTERACTIVE VISUALIZATION TEST")
    logger.info("=" * 70)
    
    # Load the Phase 1 graph
    logger.info("\n1. Loading Phase 1 graph data...")
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
                chunks.append(SimpleChunk(f.read()))
        
        builder = SimpleKnowledgeGraphBuilder()
        graph = builder.build_graph(chunks)
        logger.info(f"✅ Loaded graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    except Exception as e:
        logger.error(f"❌ Error loading graph: {e}")
        return False
    
    # Test visualization generation
    logger.info("\n2. Generating interactive visualization...")
    try:
        html = create_interactive_graph(graph)
        if html:
            logger.info(f"✅ Generated HTML visualization ({len(html)} bytes)")
            
            # Save to file for manual testing
            output_file = Path("data/knowledge_graph_interactive.html")
            with open(output_file, 'w') as f:
                f.write(html)
            logger.info(f"✅ Saved to {output_file}")
            logger.info(f"   Open in browser to test: file://{output_file.absolute()}")
        else:
            logger.error("❌ Failed to generate HTML")
            return False
    except Exception as e:
        logger.error(f"❌ Error generating visualization: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("✅ PHASE 2 COMPLETE - VISUALIZATION WORKING")
    logger.info("=" * 70)
    logger.info("\nPhase 2 Results:")
    logger.info(f"  • Interactive network graph generated")
    logger.info(f"  • HTML file saved for testing")
    logger.info(f"  • Ready to integrate into Streamlit app")
    logger.info("\nNext Steps:")
    logger.info("  1. Open data/knowledge_graph_interactive.html in browser to test")
    logger.info("  2. Integrate into Streamlit app (app.py)")
    logger.info("  3. Test in live app")
    
    return True


if __name__ == "__main__":
    success = test_phase2()
    exit(0 if success else 1)
