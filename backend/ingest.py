from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


def create_vectorstore(resume_text):
    """
    Create a FAISS vector store from resume text.
    """

    print("Creating LangChain Document...")

    documents = [
        Document(page_content=resume_text)
    ]   # we convert on list

    print("Splitting into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    print(f"Total chunks: {len(chunks)}")

    print("Loading embedding model...")

    embedding_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    print("Creating FAISS vector store...")

    vectorstore = FAISS.from_documents(
        chunks,
        embedding_model
    )

    print("Done!")

    return vectorstore
