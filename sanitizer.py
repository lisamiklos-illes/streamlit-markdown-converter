"""
Text sanitization utilities for markdown conversion.

This module provides functions to clean and sanitize text content by removing
markdown syntax, special characters, and excessive whitespace.
"""

import re


def sanitize_text(text: str) -> str:
    """
    Sanitize markdown text for plain text output.

    Removes markdown syntax, special characters, and normalizes whitespace
    to produce clean, analysis-ready plain text.

    Args:
        text: Raw text content from MarkItDown

    Returns:
        Sanitized plain text with markdown syntax removed and whitespace normalized
    """
    if not text:
        return ""

    # Step 1: Remove markdown headers (# symbols)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

    # Step 2: Remove markdown bold/italic (**text**, *text*, __text__, _text_)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
    text = re.sub(r'__([^_]+)__', r'\1', text)      # Bold alt
    text = re.sub(r'_([^_]+)_', r'\1', text)        # Italic alt

    # Step 3: Remove markdown links [text](url) - keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # Step 4: Remove markdown images ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', text)

    # Step 5: Remove inline code backticks `code`
    text = re.sub(r'`([^`]+)`', r'\1', text)

    # Step 6: Remove code blocks ```
    text = re.sub(r'```[\s\S]*?```', '', text)

    # Step 7: Remove blockquotes >
    text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)

    # Step 8: Remove list markers (-, *, +, 1.)
    text = re.sub(r'^[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)

    # Step 9: Remove horizontal rules (---, ***, ___)
    text = re.sub(r'^[-*_]{3,}$', '', text, flags=re.MULTILINE)

    # Step 10: Remove HTML tags (if any leaked through)
    text = re.sub(r'<[^>]+>', '', text)

    # Step 11: Remove special characters (keep alphanumeric + basic punctuation)
    # Keep: letters, numbers, spaces, . , ! ? : ; - ( ) " ' newlines
    text = re.sub(r'[^a-zA-Z0-9\s.,!?:;\-()"\'\n]', '', text)

    # Step 12: Normalize whitespace
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)

    # Replace excessive newlines (more than 2) with 2 newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Remove leading/trailing whitespace from entire text
    text = text.strip()

    return text
