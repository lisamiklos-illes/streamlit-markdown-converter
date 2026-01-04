"""
File conversion utilities using MarkItDown.

This module provides a wrapper around Microsoft's MarkItDown library for
converting various document formats (PDF, DOCX, PPTX, etc.) to Markdown or
plain text format.
"""

import tempfile
from pathlib import Path
from typing import Tuple, Optional
from markitdown import MarkItDown
from sanitizer import sanitize_text


def convert_uploaded_file(
    uploaded_file,
    converter: MarkItDown,
    output_format: str
) -> Tuple[Optional[str], Optional[str]]:
    """
    Convert a Streamlit UploadedFile to the desired output format.

    Args:
        uploaded_file: Streamlit UploadedFile object
        converter: MarkItDown instance
        output_format: Either "markdown" or "text"

    Returns:
        Tuple of (content, error):
            - content: The converted text content (None if error occurred)
            - error: Error message (None if successful)
    """
    # Create temporary file with original extension
    suffix = Path(uploaded_file.name).suffix
    tmp_path = None

    try:
        # Write uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        # Convert using MarkItDown
        result = converter.convert(tmp_path)

        # Process based on output format
        if output_format == "markdown":
            content = result.text_content
        else:  # plain text
            content = sanitize_text(result.text_content)

        return content, None

    except Exception as e:
        error_msg = f"Conversion failed: {str(e)}"
        return None, error_msg

    finally:
        # Clean up temporary file
        if tmp_path:
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except Exception:
                pass  # Ignore cleanup errors
