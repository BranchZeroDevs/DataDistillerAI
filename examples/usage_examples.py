"""Complete usage examples for DataDistillerAI."""

# Example 1: Basic RAG Pipeline
# ==========================

from src.workflows import RAGPipeline
from config.settings import settings

# Initialize pipeline
pipeline = RAGPipeline(
    document_path="./data/documents",
    vector_db_path=settings.VECTOR_DB_PATH,
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP,
)

# Index documents
pipeline.index_documents()

# Query the knowledge base
question = "What is machine learning?"
answer = pipeline.query(question, top_k=3)
print(f"Q: {question}")
print(f"A: {answer}")


# Example 2: Using Individual Components
# ======================================

from src.ingestion import DocumentLoader
from src.processing.chunker import SemanticChunker
from src.retrieval import VectorStore
from src.llm import LLMClient, RAG_PROMPT, SYSTEM_PROMPTS

# Step 1: Load documents
loader = DocumentLoader()
documents = loader.load_directory("./data/documents")

# Step 2: Chunk documents
chunker = SemanticChunker(chunk_size=1024, overlap=128)
all_chunks = []
for doc in documents:
    chunks = chunker.chunk(doc.content, metadata=doc.metadata)
    all_chunks.extend(chunks)

# Step 3: Create vector store and add chunks
vector_store = VectorStore()
vector_store.add_documents(all_chunks)

# Step 4: Search for similar documents
query = "Deep learning neural networks"
results = vector_store.search(query, top_k=5)

# Step 5: Format results for LLM
context = "\n---\n".join(
    f"[{metadata['source']}]\n{content}"
    for content, metadata, _ in results
)

# Step 6: Generate answer
llm = LLMClient()
prompt = RAG_PROMPT.format(context=context, question=query)
answer = llm.generate(prompt, system_prompt=SYSTEM_PROMPTS["qa"])
print(f"Answer: {answer}")


# Example 3: Document Summarization
# =================================

# Summarize all indexed documents
summary = pipeline.summarize()
print(f"Summary:\n{summary}")

# Or summarize a specific document
summary_specific = pipeline.summarize("./data/documents/specific_doc.txt")
print(f"Specific Summary:\n{summary_specific}")


# Example 4: Custom Workflow
# ==========================

class CustomAnalysisWorkflow:
    """Custom workflow for domain-specific analysis."""
    
    def __init__(self, pipeline):
        self.pipeline = pipeline
    
    def analyze_topics(self, topics_list):
        """Analyze multiple topics."""
        results = {}
        for topic in topics_list:
            query = f"Explain {topic}"
            results[topic] = self.pipeline.query(query, top_k=3)
        return results
    
    def compare_concepts(self, concept1, concept2):
        """Compare two concepts."""
        query = f"Compare and contrast {concept1} and {concept2}"
        return self.pipeline.query(query, top_k=5)


# Use custom workflow
workflow = CustomAnalysisWorkflow(pipeline)
topics = ["supervised learning", "unsupervised learning", "reinforcement learning"]
analysis = workflow.analyze_topics(topics)

comparison = workflow.compare_concepts("CNN", "RNN")
print(f"Comparison:\n{comparison}")


# Example 5: Batch Processing
# ============================

from pathlib import Path

def process_documents_batch(document_dir, batch_size=10):
    """Process large number of documents in batches."""
    
    loader = DocumentLoader()
    chunker = SemanticChunker()
    vector_store = VectorStore()
    
    doc_paths = list(Path(document_dir).glob("*.txt"))
    
    for i in range(0, len(doc_paths), batch_size):
        batch_paths = doc_paths[i:i+batch_size]
        batch_chunks = []
        
        for doc_path in batch_paths:
            doc = loader.load(str(doc_path))
            chunks = chunker.chunk(doc.content, metadata=doc.metadata)
            batch_chunks.extend(chunks)
        
        vector_store.add_documents(batch_chunks)
        print(f"Processed batch {i//batch_size + 1}")
    
    vector_store.save("./vector_store")
    return vector_store


# Example 6: Advanced Retrieval with Filtering
# =============================================

def retrieve_with_filtering(pipeline, query, source_filter=None, top_k=5):
    """Retrieve results with optional source filtering."""
    
    results = pipeline.vector_store.search(query, top_k=top_k*2)
    
    if source_filter:
        filtered = [
            r for r in results 
            if source_filter in r[1].get('source', '')
        ]
        return filtered[:top_k]
    
    return results[:top_k]


# Example 7: Caching Query Results
# ================================

from functools import lru_cache

class CachedRAGPipeline(RAGPipeline):
    """RAG pipeline with query result caching."""
    
    @lru_cache(maxsize=128)
    def query(self, question: str, top_k: int = 3) -> str:
        """Query with caching."""
        return super().query(question, top_k)


# Use cached pipeline
cached_pipeline = CachedRAGPipeline()
# First query - will compute
result1 = cached_pipeline.query("What is machine learning?")
# Second identical query - will use cache
result2 = cached_pipeline.query("What is machine learning?")


if __name__ == "__main__":
    print("See individual examples above for usage patterns.")
