from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os


def extract_resume_text(uploaded_file):
    """
    Extract text from an uploaded resume PDF using LangChain.
    """

    # Create a temporary PDF file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getbuffer()) # write expects bytes that's why we use getbuffer()
        temp_pdf_path = temp_file.name

    try:
        # Load PDF using LangChain
        loader = PyPDFLoader(temp_pdf_path)

        # Read all pages
        documents = loader.load()

        # Combine text from every page
        resume_text = ""

        for document in documents:
            resume_text += document.page_content
            resume_text += "\n\n"

        return resume_text

    finally:
        # Delete temporary file
        os.remove(temp_pdf_path)