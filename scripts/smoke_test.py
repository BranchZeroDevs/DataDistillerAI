from src.workflows_ollama import RAGPipelineOllama

if __name__ == '__main__':
    print('Initializing Ollama RAG pipeline (index-only smoke test)')
    pipeline = RAGPipelineOllama()
    n = pipeline.index_documents()
    print(f'Indexed {n} chunks')

    print('Running a vector search for "machine learning"')
    results = pipeline.vector_store.search('machine learning', top_k=2)
    for i, (content, metadata, score) in enumerate(results, 1):
        print(f'[{i}] score={score:.4f} preview={content[:200]!r}')
