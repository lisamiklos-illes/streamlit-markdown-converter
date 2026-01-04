# Streamlit Markdown Converter

A cute and user-friendly web application for converting multiple document formats to Markdown or Plain Text using Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library.

## Features

- **Batch Processing**: Upload and convert up to 10 files simultaneously
- **Multiple Output Formats**:
  - **Markdown (.md)**: Preserves document structure and formatting
  - **Plain Text (.txt)**: Fully sanitized text with markdown syntax removed
- **Wide Format Support**: PDF, DOCX, PPTX, XLSX, HTML, images with text, and more
- **Progress Tracking**: Real-time progress indicators during conversion
- **Flexible Downloads**:
  - Individual file downloads
  - Bulk ZIP download for multiple files
- **Error Resilience**: Per-file error handling - continues processing even if some files fail
- **Clean UI**: Beautiful, intuitive interface with emojis and clear messaging

## Supported File Formats

MarkItDown can convert:
- PDF documents
- Word documents (.docx)
- PowerPoint presentations (.pptx)
- Excel spreadsheets (.xlsx)
- HTML files
- Plain text files
- Markdown files
- JSON, CSV, XML files
- eBooks (ePub, MOBI)
- RTF documents
- Images with text (OCR capability)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or navigate to the project directory:
```bash
cd /Users/lisamiklosilles/Desktop/Code/streamlit_markdown_converter
```

2. (Optional but recommended) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

Run the Streamlit app:
```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

### Converting Files

1. **Upload Files**: Click the upload area or drag and drop files (up to 10 at once)
2. **Select Output Format**:
   - Choose **Markdown (.md)** to preserve document structure
   - Choose **Plain Text (.txt)** for fully sanitized text output
3. **Convert**: Click the "Convert Files" button
4. **Download**:
   - Download individual files using the download buttons
   - Or download all files as a ZIP archive

## Project Structure

```
streamlit_markdown_converter/
├── app.py              # Main Streamlit application
├── converter.py        # MarkItDown wrapper for file conversion
├── sanitizer.py        # Text cleaning and sanitization utilities
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore patterns
```

## How It Works

### Markdown Output
When you select Markdown output, the converter:
1. Uploads your file to a temporary location
2. Uses MarkItDown to extract structured content
3. Returns the markdown-formatted text from `result.text_content`

### Plain Text Output
When you select Plain Text output, the converter:
1. Converts the file to markdown (as above)
2. Applies comprehensive text sanitization:
   - Removes markdown headers (`#`)
   - Removes bold/italic markers (`**`, `*`)
   - Extracts text from links and images
   - Removes code blocks and inline code
   - Removes list markers and blockquotes
   - Strips special characters (keeps alphanumeric + basic punctuation)
   - Normalizes whitespace (collapses spaces, limits newlines)

## Technical Details

### Dependencies
- **streamlit**: Web application framework
- **markitdown**: Microsoft's document conversion library

### Architecture
- **Modular Design**: Separation of concerns between UI (app.py), conversion logic (converter.py), and text processing (sanitizer.py)
- **Caching**: Uses `@st.cache_resource` to cache the MarkItDown converter instance for better performance
- **Error Handling**: Graceful per-file error handling with detailed error messages
- **Temporary File Management**: Automatic cleanup of temporary files after conversion

## Development

### Running Tests
Currently, the project does not include automated tests. To manually test:
1. Upload various file types (PDF, DOCX, PPTX, etc.)
2. Try both output formats
3. Test batch uploads with multiple files
4. Verify error handling with corrupted or unsupported files

### Contributing
Feel free to submit issues or pull requests to improve the application!

## Credits

- Built with [Streamlit](https://streamlit.io/)
- Powered by [MarkItDown](https://github.com/microsoft/markitdown) by Microsoft
- Created for simple, efficient document conversion workflows

## License

This project is open source and available for personal and educational use.

---

Built with ❤️ using Streamlit and MarkItDown
