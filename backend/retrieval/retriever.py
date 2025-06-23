import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from backend.utils.logger import logger
from langchain_core.documents import Document

DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Initialize once
_embedding_fn = OllamaEmbeddings(model=OLLAMA_MODEL)
_db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=_embedding_fn
)


def get_retriever(k: int = 15, document_name: str | None = None):
    """
    Returns a retriever object for querying the vector store.
    Args:
        k (int): Number of results to retrieve.
        document_name (str, optional): Filter by document name.
    Returns:
        Retriever object.
    """
    search_kwargs = {"k": k}
    if document_name:
        search_kwargs["filter"] = {"document_name": document_name}
    return _db.as_retriever(search_kwargs=search_kwargs)


def get_all_chunks_for_document(document_name: str):
    """
    Fetches all document chunks from ChromaDB based on metadata filter.
    Args:
        document_name (str): The name of the document to filter by.
    Returns:
        list: List of Document objects for the specified document.
    """
    results = _db.get(where={"document_name": document_name})
    # Reconstruct Document objects from the retrieved data
    if not results or not results.get("documents"):
        return []
    return [
        Document(page_content=doc, metadata=meta)
        for doc, meta in zip(results["documents"], results["metadatas"])
    ]


def retrieve_chunks(query: str, k: int = 5):
    """
    Retrieves relevant document chunks for a given query.
    Args:
        query (str): The user query.
        k (int): Number of results to retrieve.
    Returns:
        list: List of relevant Document objects.
    """
    retriever = get_retriever(k)
    docs = retriever.invoke(query)
    logger.info(f"Retrieved {len(docs)} chunks for query: {query}")
    return docs