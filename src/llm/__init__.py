"""LLM client and integration utilities."""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class LLMClient:
    """OpenAI LLM client wrapper."""
    
    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 500
    ):
        """
        Initialize LLM client.
        
        Args:
            api_key: OpenAI API key
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum response tokens
        """
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = self._init_client()
    
    def _init_client(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            return OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai not installed. Use: pip install openai")
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generate response using LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
        
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM error: {e}")
            raise


class PromptTemplate:
    """Template for structured prompts."""
    
    def __init__(self, template: str, variables: List[str]):
        """
        Initialize prompt template.
        
        Args:
            template: Template string with {variable} placeholders
            variables: List of variable names
        """
        self.template = template
        self.variables = variables
    
    def format(self, **kwargs) -> str:
        """Format template with values."""
        return self.template.format(**kwargs)


# Pre-defined prompt templates
SYSTEM_PROMPTS = {
    "qa": """You are a knowledgeable assistant that answers questions based on provided documents. 
Always cite the source documents in your response. If the answer is not in the documents, say "I don't have enough information to answer this question."
""",
    
    "summarization": """You are an expert at summarizing documents. 
Create a concise summary that captures the main points and key information. 
Keep the summary clear and well-organized.""",
    
    "exploration": """You are a helpful research assistant.
Help the user explore and understand the provided documents.
Ask clarifying questions when needed and provide insights.""",
}

RAG_PROMPT = PromptTemplate(
    template="""Based on the following documents:

{context}

Answer the question: {question}

Provide a detailed answer grounded in the source material.""",
    variables=["context", "question"]
)

QA_PROMPT = PromptTemplate(
    template="""Question: {question}

Relevant context from documents:
{context}

Answer:""",
    variables=["question", "context"]
)

SUMMARIZATION_PROMPT = PromptTemplate(
    template="""Please summarize the following document:

{document}

Summary:""",
    variables=["document"]
)
