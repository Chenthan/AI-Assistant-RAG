from datetime import datetime, timezone
import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from backend.utils.logger import logger

DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

def store_embeddings(chunks, file_name: str):
    """
    Stores document chunks as embeddings in the Chroma vector store.
    Adds metadata to each chunk before storage.
    Args:
        chunks (list): List of Document objects to store.
        file_name (str): Name of the source file.
    Returns:
        list: The stored chunks with metadata.
    """
    logger.info(f"Storing embeddings")
    os.makedirs(DB_DIR, exist_ok=True)
    embedding_fn = OllamaEmbeddings(model=OLLAMA_MODEL)
    db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embedding_fn
    )
    # Add metadata to each chunk before storing
    upload_time = datetime.now(timezone.utc).isoformat()
    for chunk in chunks:
        chunk.metadata["document_name"] = file_name
        chunk.metadata["upload_time"] = upload_time

    logger.info(f"Adding documents to db")
    db.add_documents(chunks)
    logger.info(f"Stored {len(chunks)} embeddings")
    return chunks