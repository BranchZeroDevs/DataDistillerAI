"""Data processing and preparation utilities."""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class TextCleaner:
    """Utilities for text cleaning and normalization."""
    
    @staticmethod
    def clean(text: str, remove_urls: bool = True, remove_emails: bool = True) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove URLs
        if remove_urls:
            text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove emails
        if remove_emails:
            text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\'"]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
