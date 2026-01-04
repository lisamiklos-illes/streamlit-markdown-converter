"""
Streamlit Markdown Converter

A cute web application for converting multiple file types (PDF, DOCX, PPTX, etc.)
to Markdown or Plain Text format using Microsoft's MarkItDown library.
"""

import streamlit as st
import zipfile
from io import BytesIO
from pathlib import Path
from markitdown import MarkItDown
from converter import convert_uploaded_file


# Configure page
st.set_page_config(
    page_title="Markdown Converter",
    page_icon="📝",
    layout="centered"
)


@st.cache_resource
def get_converter():
    """Cache the MarkItDown converter instance for reuse."""
    return MarkItDown()


def create_zip(results: list, extension: str) -> bytes:
    """
    Create a ZIP file containing all converted files.

    Args:
        results: List of tuples (original_filename, converted_content)
        extension: File extension for converted files (.md or .txt)

    Returns:
        ZIP file as bytes
    """
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for original_name, content in results:
            # Generate new filename with appropriate extension
            new_name = Path(original_name).stem + extension
            # Add to zip
            zf.writestr(new_name, content)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def main():
    """Main application logic."""

    # Header section
    st.title("📝 Streamlit Markdown Converter")
    st.markdown(
        "Convert your documents to **Markdown** or **Plain Text** using "
        "[MarkItDown](https://github.com/microsoft/markitdown) - "
        "Microsoft's powerful document conversion tool."
    )

    st.divider()

    # File upload section
    st.subheader("📁 Upload Files")
    uploaded_files = st.file_uploader(
        "Choose files to convert (supports PDF, DOCX, PPTX, XLSX, HTML, and more)",
        accept_multiple_files=True,
        help="Upload one or more files. Maximum 10 files at a time."
    )

    # Display file count
    if uploaded_files:
        file_count = len(uploaded_files)
        if file_count > 10:
            st.error("❌ Maximum 10 files allowed. Please upload fewer files.")
            st.stop()
        else:
            st.info(f"📊 {file_count} file(s) selected")

    st.divider()

    # Output format selection
    st.subheader("⚙️ Output Format")
    output_choice = st.radio(
        "Select output format:",
        options=["Markdown (.md)", "Plain Text (.txt)"],
        help="Markdown preserves structure; Plain Text is fully sanitized"
    )

    # Determine format for processing
    output_format = "markdown" if "Markdown" in output_choice else "text"
    extension = ".md" if output_format == "markdown" else ".txt"
    mime_type = "text/markdown" if output_format == "markdown" else "text/plain"

    # Expandable section for supported formats
    with st.expander("ℹ️ Supported File Formats"):
        st.markdown("""
        **MarkItDown supports:**
        - 📄 PDF documents
        - 📝 Word documents (.docx)
        - 📊 PowerPoint presentations (.pptx)
        - 📈 Excel spreadsheets (.xlsx)
        - 🌐 HTML files
        - 📋 Plain text files
        - 🔤 Markdown files
        - 📦 JSON, CSV, XML files
        - 📚 eBooks (ePub, MOBI)
        - 📄 RTF documents
        - 🖼️ Images with text (OCR)
        """)

    st.divider()

    # Conversion section
    if uploaded_files:
        if st.button("🚀 Convert Files", type="primary", use_container_width=True):
            converter = get_converter()
            results = []
            errors = []

            # Create progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Process each file
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Converting {uploaded_file.name}...")

                content, error = convert_uploaded_file(
                    uploaded_file,
                    converter,
                    output_format
                )

                if error:
                    errors.append((uploaded_file.name, error))
                else:
                    results.append((uploaded_file.name, content))

                # Update progress
                progress_bar.progress((i + 1) / len(uploaded_files))

            # Clear status text
            status_text.empty()
            progress_bar.empty()

            st.divider()

            # Display results
            if results:
                st.success(f"✅ Successfully converted {len(results)} file(s)!")

                # Individual download buttons
                st.subheader("📥 Download Converted Files")

                for original_name, content in results:
                    new_filename = Path(original_name).stem + extension

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f"📄 {new_filename}")
                    with col2:
                        st.download_button(
                            label="⬇️ Download",
                            data=content,
                            file_name=new_filename,
                            mime=mime_type,
                            key=f"download_{original_name}"
                        )

                # ZIP download for multiple files
                if len(results) > 1:
                    st.divider()
                    zip_data = create_zip(results, extension)
                    st.download_button(
                        label="📦 Download All as ZIP",
                        data=zip_data,
                        file_name=f"converted_files_{output_format}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )

            # Display errors
            if errors:
                st.error(f"❌ Failed to convert {len(errors)} file(s):")
                for filename, error_msg in errors:
                    st.text(f"  • {filename}: {error_msg}")

            # Summary
            st.divider()
            total = len(results) + len(errors)
            st.info(
                f"📊 **Summary:** {len(results)} succeeded, "
                f"{len(errors)} failed out of {total} total file(s)"
            )

    else:
        st.info("👆 Upload files above to get started!")

    # Footer
    st.divider()
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.9em;'>"
        "Built with ❤️ using Streamlit and MarkItDown"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
