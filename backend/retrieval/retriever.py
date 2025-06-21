import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from backend.utils.logger import logger

DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Initialize once
_embedding_fn = OllamaEmbeddings(model=OLLAMA_MODEL)
_db = Chroma(
    persist_directory=DB_DIR,
    embedding_function=_embedding_fn
)


def get_retriever(k: int = 5):
    return _db.as_retriever(search_kwargs={"k": k})


def retrieve_chunks(query: str, k: int = 5):
    retriever = get_retriever(k)
    docs = retriever.invoke(query)
    logger.info(f"Retrieved {len(docs)} chunks for query: {query}")
    return docs