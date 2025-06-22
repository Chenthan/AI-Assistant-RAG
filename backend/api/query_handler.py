from fastapi import APIRouter, HTTPException
from backend.cache.cache_service import get_cached_response, cache_response
from backend.llm.llm_chain import get_answer
from backend.repository.document_repository import list_documents, list_document_names
from langchain_ollama import OllamaEmbeddings
import numpy as np
import os
from backend.llm.document_detector import detect_document_in_query

router = APIRouter()


@router.get("/")
async def query(q: str):
    """
    Endpoint to handle user queries. Detects referenced document, injects document list into prompt,
    checks cache, and returns LLM answer.
    Args:
        q (str): The user query string.
    Returns:
        dict: The answer and its source (cache or llm).
    """
    # Detect which document, if any, the user is referring to
    detected_doc = await detect_document_in_query(q)

    # Normalize query for cache key, including the detected doc
    key = f"{detected_doc}:{q.strip().lower()}" if detected_doc else q.strip().lower()

    # Check cache
    cached = get_cached_response(key)
    if cached:
        return {"answer": cached, "source": "cache"}

    # Inject document list as system context
    doc_names = await list_document_names()
    doc_list = ", ".join(doc_names) if doc_names else "No documents are currently stored."
    system_context = (
        f"You are an assistant with access to the following documents: {doc_list}.\n"
        "If the user asks about available documents, answer using this list. "
        "If the user asks about the content of a specific document, answer using the document's content."
    )
    prompt = f"{system_context}\n\nUser question: {q}"

    # Get LLM answer, filtered by document if one was detected
    answer = get_answer(query=prompt, document_name=detected_doc)
    if "couldn't process" in answer:
        raise HTTPException(status_code=500, detail=answer)

    # Cache and return
    cache_response(key, answer)
    return {"answer": answer, "source": "llm"}


async def build_document_context():
    docs = await list_documents()
    if not docs:
        return "There are currently no documents available."

    context = "The following documents are available:\n"
    for doc in docs:
        context += f"- {doc['file_name']} (uploaded at {doc['upload_time']})\n"
    return context

async def detect_relevant_document(query: str):
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    docs = await list_documents()
    if not docs:
        return None  # fallback to global search

    embedding_fn = OllamaEmbeddings(model=OLLAMA_MODEL)
    query_embedding = embedding_fn.embed_query(query)

    max_score = 0
    selected_doc = None

    for doc in docs:
        doc_embedding = embedding_fn.embed_query(doc["summary"])
        similarity = cosine_similarity(query_embedding, doc_embedding)

        if similarity > max_score:
            max_score = similarity
            selected_doc = doc

    if max_score > 0.7:  # Adjust threshold based on real testing
        return selected_doc
    return None

def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))