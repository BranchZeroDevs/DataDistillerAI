"""
Ollama API integration for DataDistillerAI
Runs completely locally - no API keys needed, no quotas
"""

import os
import logging
from typing import Optional
import requests
import json

logger = logging.getLogger(__name__)


class PromptTemplate:
    """Structured prompt templates for Ollama"""
    
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


class OllamaClient:
    """Ollama API client wrapper"""
    
    def __init__(self, model: str = "qwen2.5:3b", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama client
        
        Args:
            model: Model to use (default: mistral - fast and good quality)
            base_url: Ollama server URL (default: localhost:11434)
        
        Available models:
            - qwen2.5:3b (common on local Ollama installs)
            - gemma3:4b
            - gpt-oss:120b-cloud
            - deepseek-r1:latest
            - (or any model you have installed; change via `model` param)
        """
        self.base_url = base_url
        self.model = model
        self.api_endpoint = f"{base_url}/api/generate"
        
        # Verify Ollama is running
        if not self._check_connection():
            raise ConnectionError(
                f"Cannot connect to Ollama at {base_url}. "
                f"Make sure Ollama is running. Start with: ollama serve"
            )
        
        # Verify model exists
        if not self._check_model():
            raise ValueError(
                f"Model '{model}' not found. "
                f"Pull it with: ollama pull {model}"
            )
        
        logger.info(f"Initialized Ollama client with model: {model}")
    
    def _check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _check_model(self) -> bool:
        """Check if model is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                # Check for exact match or prefix match
                for model_name in model_names:
                    if model_name == self.model or model_name.startswith(self.model + ':'):
                        # Update to use the full model name
                        self.model = model_name
                        return True
        except:
            pass
        return False
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text using Ollama
        
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
            
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=300  # 5 minute timeout for longer responses
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                logger.error(f"Ollama error: {response.status_code}")
                raise Exception(f"Ollama request failed: {response.status_code}")
        
        except Exception as e:
            logger.error(f"Ollama error: {e}")
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
    
    def list_available_models(self) -> list:
        """List all available models on Ollama server"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return [m['name'] for m in models]
        except:
            pass
        return []


# Export
__all__ = ['OllamaClient', 'PromptTemplate']
