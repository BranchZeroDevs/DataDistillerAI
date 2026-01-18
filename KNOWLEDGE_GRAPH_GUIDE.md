# 🧠 Knowledge Graph Visualization

## Overview

The Knowledge Graph feature automatically extracts, analyzes, and visualizes the semantic relationships and ideas in your documents. It shows:

- **Concepts**: Key ideas and entities extracted from documents
- **Relationships**: How concepts connect and relate to each other
- **Semantic Flow**: How ideas progress and build upon each other
- **Concept Clusters**: Groups of related ideas

## Features

### 📈 Interactive Network Graph
- **Drag & Explore**: Click and drag nodes to explore relationships
- **Node Size**: Indicates concept importance (larger = more important)
- **Edge Thickness**: Shows relationship strength (thicker = stronger connection)
- **Zoom & Pan**: Explore large networks easily

### 🔗 Relationship Analysis
Shows how top concepts connect:
- **Flows To**: Concepts this one leads to
- **Flows From**: Concepts that lead to this one
- **Connection Strength**: Numeric weight of relationships

### 💡 Semantic Flow
Visualizes idea progression through documents:
- **New Concepts**: Fresh ideas introduced in each chunk
- **Continuing Concepts**: Ideas that persist across chunks
- **Concept Count**: How many concepts appear in each section

### 📍 Concept Clusters
Discovers natural groupings:
- Automatically finds clusters of related concepts
- Shows importance within each cluster
- Helps understand document structure

## How It Works

### 1. Entity & Concept Extraction
```
Document Text
    ↓
spaCy NLP Processing
    ↓
Named Entities (PERSON, ORG, LOCATION, etc.)
+ Noun Phrases (natural language concepts)
```

### 2. Relationship Building
```
Extracted Concepts
    ↓
Co-occurrence Analysis (same chunk = related)
    ↓
Semantic Relationships (edges in graph)
```

### 3. Analysis
```
Knowledge Graph
    ↓
PageRank Algorithm → Concept Importance
Community Detection → Concept Clusters
Chunk-by-chunk Tracking → Semantic Flow
```

## Usage in Streamlit App

1. **Start the app**: `streamlit run app.py`
2. **Go to "Knowledge Graph" tab**
3. **Choose a view**:
   - **Network Graph**: Explore interactive visualization
   - **Relationships**: See how top concepts connect
   - **Semantic Flow**: Watch ideas evolve
   - **Clusters**: Understand concept groupings

## Command Line Usage

```python
from src.knowledge_graph import KnowledgeGraphBuilder

# Build from chunks
kg = KnowledgeGraphBuilder()
graph = kg.build_graph(chunks)

# Get importance scores
importance = kg.get_node_importance()
for concept, score in importance.items():
    print(f"{concept}: {score:.2%}")

# Find concept clusters
clusters = kg.find_concept_clusters()

# Analyze semantic flow
flows = kg.get_semantic_flow(chunks)

# Export interactive HTML
kg.export_html("graph.html")
```

## Test the Feature

```bash
python test_knowledge_graph.py
```

Output shows:
- Total concepts found
- Relationship count
- Top 10 important concepts
- Discovered clusters
- Semantic flow progression

## Example Output

```
Knowledge Graph Built:
├─ 80 concepts found
├─ 2,433 relationships
├─ 3 concept clusters
└─ Semantic flow across 5 chunks

Top Concepts:
  1. Machine Learning (3.39%)
  2. Deep Learning (2.88%)
  3. Neural Networks (2.65%)
  4. Data (2.04%)
  5. Training (1.80%)
```

## Interpreting the Graph

### Node Colors
- **Red**: Named entities (people, organizations, locations)
- **Teal**: Extracted concepts and ideas

### Edge Properties
- **Thickness**: Strong connections are thicker
- **Direction**: Arrows show relationship flow
- **Weight**: Number shows connection strength

### Layout
- **Close Nodes**: Strongly related concepts
- **Distant Nodes**: Loosely related
- **Node Clusters**: Natural groupings of ideas

## Advanced Features

### Importance Scoring
Uses PageRank algorithm:
- Concepts that connect to many others score higher
- Well-connected ideas are more central to documents

### Clustering
Uses modularity-based community detection:
- Finds natural groups of related concepts
- Helps identify document themes

### Semantic Flow
Tracks concept progression:
- Shows what's new at each stage
- Highlights continuing ideas
- Reveals document structure

## Limitations

- Requires spaCy language model: `python -m spacy download en_core_web_sm`
- Large documents may create complex graphs
- Some filtering is applied to top concepts only
- Relationships based on co-occurrence, not semantic similarity

## Tips for Better Results

1. **Larger Documents**: More data = better relationships
2. **Topic-Specific**: Works best on focused documents
3. **Clean Text**: Better extraction with well-formatted text
4. **Multiple Sources**: Compare graphs across different documents

## Example Workflows

### Workflow 1: Understand Document Structure
```
1. Open Knowledge Graph tab
2. View Semantic Flow
3. See how ideas progress
4. Understand document organization
```

### Workflow 2: Find Key Concepts
```
1. View Relationships tab
2. Look at top concepts
3. See what they connect to
4. Understand central themes
```

### Workflow 3: Explore Themes
```
1. Check Concept Clusters
2. See natural groupings
3. Understand main topics
4. Find related ideas
```

## Tech Stack

- **spaCy**: NLP and entity extraction
- **NetworkX**: Graph analysis and algorithms
- **pyvis**: Interactive visualization
- **Sentence Transformers**: Semantic embeddings (available)

---

**Transform your documents into visual knowledge networks!** 🧠✨
