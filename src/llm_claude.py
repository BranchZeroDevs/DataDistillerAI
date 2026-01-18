"""
Anthropic Claude API integration for DataDistillerAI
Professional AI model with excellent reasoning capabilities
"""

import os
import logging
from typing import Optional

try:
    from anthropic import Anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

logger = logging.getLogger(__name__)


class PromptTemplate:
    """Structured prompt templates for Claude"""
    
    RAG_PROMPT = """You are an expert assistant answering questions based on provided documents.

Context from documents:
{context}

User Question: {question}

Instructions:
1. Answer based ONLY on the provided context
2. If the answer is not in the context, say "The provided documents don't contain information about this"
3. Be concise and accurate
4. Cite which part of the context you're using

Answer:"""
    
    QA_PROMPT = """Answer the following question concisely:

Question: {question}

Context: {context}

Answer:"""
    
    SUMMARIZATION_PROMPT = """Create a concise summary of the following text in 3-4 sentences:

Text: {text}

Summary:"""
    
    @classmethod
    def format(cls, template: str, **kwargs) -> str:
        """Format a template with provided variables"""
        return template.format(**kwargs)


class ClaudeClient:
    """Anthropic Claude API client wrapper"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-haiku-20241022"):
        """
        Initialize Claude client
        
        Args:
            api_key: Anthropic API key (if None, reads from ANTHROPIC_API_KEY env var)
            model: Model to use (default: claude-3-5-haiku - cheapest, fastest)
        
        Available models:
            - claude-3-5-haiku-20241022 (cheapest, fastest, good quality) - RECOMMENDED
            - claude-3-5-sonnet-20241022 (better quality, more expensive)
            - claude-opus-4-1-20250805 (best quality, most expensive)
        """
        if not CLAUDE_AVAILABLE:
            raise ImportError("anthropic not installed. Run: pip install anthropic")
        
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        logger.info(f"Initialized Claude client with model: {model}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text using Claude
        
        Args:
            prompt: User prompt
            system_prompt: System-level instructions
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
        
        Returns:
            Generated text
        """
        try:
            # Build system message
            system_msg = system_prompt or ""
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_msg,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            
            return response.content[0].text
        
        except Exception as e:
            logger.error(f"Claude error: {e}")
            raise
    
    def query_with_context(
        self,
        question: str,
        context: str,
        top_k_results: int = 3
    ) -> str:
        """
        Answer a question with provided context (RAG)
        
        Args:
            question: User question
            context: Context from document retrieval
            top_k_results: Number of context results used
        
        Returns:
            Generated answer
        """
        prompt = PromptTemplate.format(
            PromptTemplate.RAG_PROMPT,
            context=context,
            question=question
        )
        
        system_prompt = "You are a helpful assistant answering questions based on provided documents. Be accurate and cite your sources."
        
        return self.generate(prompt, system_prompt)
    
    def summarize(self, text: str) -> str:
        """
        Summarize provided text
        
        Args:
            text: Text to summarize
        
        Returns:
            Summary
        """
        prompt = PromptTemplate.format(
            PromptTemplate.SUMMARIZATION_PROMPT,
            text=text
        )
        
        return self.generate(prompt, max_tokens=512)
    
    def get_model_info(self) -> dict:
        """Get information about the current model"""
        return {
            "model": self.model,
            "provider": "Anthropic",
            "type": "Claude"
        }


# Export
__all__ = ['ClaudeClient', 'PromptTemplate']
