# Project: Streamlit Web App with MarkItDown

## Overview
This is a Python-based web application deployed on **Streamlit Community Cloud** (not local). The app uses the `markitdown` library for document conversion and processing.

## Tech Stack
- **Frontend/Framework:** Streamlit
- **Backend:** Python
- **Core Library:** markitdown
- **Deployment:** Streamlit Community Cloud

## Important: Deployment Context
This project is deployed via **Streamlit Community Cloud**, NOT run locally. All dependency and environment considerations should account for this.

## Dependencies

### requirements.txt
All dependencies MUST be specified in `requirements.txt` at the project root. Streamlit Cloud reads this file automatically during deployment.

```
streamlit
markitdown[all]
```

Add any additional dependencies to `requirements.txt` as needed. Do NOT use `pip install` commands in code or expect local installations.

### If System Dependencies Are Needed
Create a `packages.txt` file at the project root for any apt-get packages (Linux dependencies). Streamlit Cloud will install these automatically.

```
# Example packages.txt
libmagic1
```

## File Structure
```
project-root/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies (REQUIRED)
├── packages.txt          # System dependencies (if needed)
├── .streamlit/
│   └── config.toml       # Streamlit configuration (optional)
└── README.md
```

## Code Patterns

### Streamlit App Entry Point
The main app file should be `app.py` or `streamlit_app.py` at the root level.

### MarkItDown Usage
```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("path/to/file")
markdown_content = result.text_content
```

### File Handling in Streamlit Cloud
- Use `st.file_uploader()` for user uploads
- Uploaded files are `UploadedFile` objects (file-like, use `.read()`, `.getvalue()`)
- For temp files, use `tempfile` module — Streamlit Cloud has ephemeral storage only

```python
import tempfile

uploaded_file = st.file_uploader("Upload a file")
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    # Now use tmp_path with markitdown
```

## Environment Variables / Secrets
Use Streamlit's secrets management for API keys or sensitive config:
- Create `.streamlit/secrets.toml` locally (DO NOT commit)
- Add secrets via Streamlit Cloud dashboard for production

Access in code:
```python
import streamlit as st
api_key = st.secrets["API_KEY"]
```

## Constraints & Gotchas
1. **No persistent storage** — Streamlit Cloud is ephemeral; don't rely on local file system persistence
2. **Memory limits** — Community Cloud has ~1GB RAM; be mindful with large file processing
3. **No GPU** — CPU only on free tier
4. **Cold starts** — Apps spin down after inactivity; first load may be slow
5. **markitdown temp files** — Always clean up temp files to avoid filling ephemeral storage

## Development Commands
For local testing (mirrors cloud behavior):
```bash
streamlit run app.py
```

## Deployment
1. Push code to GitHub
2. Connect repo to Streamlit Community Cloud
3. Select `app.py` as entry point
4. Deploy — dependencies auto-install from `requirements.txt`
