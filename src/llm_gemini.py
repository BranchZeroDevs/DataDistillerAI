"""
Google Gemini API integration for DataDistillerAI
Uses free tier - no payment required
"""

import os
import logging
from typing import Optional, List, Dict

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)


class PromptTemplate:
    """Structured prompt templates for Gemini"""
    
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


class GeminiClient:
    """Google Gemini API client wrapper"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google API key (if None, reads from GOOGLE_API_KEY env var)
            model: Model to use (default: gemini-pro)
        """
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai not installed. Run: pip install google-generativeai")
        
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        self.model_name = model
        logger.info(f"Initialized Gemini client with model: {model}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text using Gemini
        
        Args:
            prompt: User prompt
            system_prompt: System-level instructions
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)
        
        Returns:
            Generated text
        """
        try:
            # Combine system and user prompts
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                )
            )
            
            return response.text
        
        except Exception as e:
            logger.error(f"Gemini error: {e}")
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
        
        system_prompt = "You are a helpful assistant answering questions based on provided documents."
        
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


# Export
__all__ = ['GeminiClient', 'PromptTemplate']
