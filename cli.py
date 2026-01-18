"""Interactive CLI for DataDistillerAI."""

import os
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataDistillerCLI:
    """Command-line interface for DataDistillerAI."""
    
    def __init__(self):
        """Initialize CLI."""
        self.pipeline = None
    
    def setup(self):
        """Initialize the RAG pipeline - Using Ollama as primary backend."""
        from src.workflows_ollama import RAGPipelineOllama
        
        doc_path = input("Enter document path (default: ./data/documents): ") or "./data/documents"
        
        try:
            self.pipeline = RAGPipelineOllama(document_path=doc_path)
            logger.info("✓ Pipeline initialized with Ollama backend!")
            logger.info("Note: Secondary backends available - Claude, Gemini (code-only)")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama backend: {e}")
            logger.info("Make sure Ollama is running locally (http://localhost:11434)")
    
    def index(self):
        """Index documents."""
        if not self.pipeline:
            print("Please run 'setup' first.")
            return
        
        logger.info("Starting document indexing...")
        self.pipeline.index_documents()
        logger.info("Indexing complete!")
    
    def query(self):
        """Query the knowledge base."""
        if not self.pipeline:
            print("Please run 'setup' first.")
            return
        
        question = input("Enter your question: ")
        top_k = int(input("Number of results (default: 3): ") or "3")
        
        logger.info(f"Searching for answers to: {question}")
        response = self.pipeline.query(question, top_k=top_k)
        print(f"\nAnswer:\n{response}\n")
    
    def summarize(self):
        """Summarize documents."""
        if not self.pipeline:
            print("Please run 'setup' first.")
            return
        
        logger.info("Generating summary...")
        summary = self.pipeline.summarize()
        print(f"\nSummary:\n{summary}\n")
    
    def help(self):
        """Show help message."""
        print("""
Available commands:
  setup       - Initialize the RAG pipeline
  index       - Index documents from specified path
  query       - Ask a question about the documents
  summarize   - Generate a summary of documents
  help        - Show this help message
  exit        - Exit the application
        """)
    
    def run(self):
        """Run the CLI."""
        print("Welcome to DataDistillerAI!")
        print("Type 'help' for available commands.")
        
        commands = {
            'setup': self.setup,
            'index': self.index,
            'query': self.query,
            'summarize': self.summarize,
            'help': self.help,
        }
        
        while True:
            try:
                cmd = input("\n> ").strip().lower()
                
                if cmd == 'exit':
                    print("Goodbye!")
                    break
                
                if cmd in commands:
                    commands[cmd]()
                elif cmd:
                    print(f"Unknown command: {cmd}")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error: {e}")


if __name__ == "__main__":
    cli = DataDistillerCLI()
    cli.run()
