import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from backend.utils.logger import logger

DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

def store_embeddings(chunks):
    os.makedirs(DB_DIR, exist_ok=True)
    embedding_fn = OllamaEmbeddings(model=OLLAMA_MODEL)
    db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embedding_fn
    )
    db.add_documents(chunks)
    logger.info(f"Stored {len(chunks)} embeddings")
    return db