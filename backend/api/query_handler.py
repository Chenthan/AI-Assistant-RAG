from fastapi import APIRouter, HTTPException
from backend.cache.cache_service import get_cached_response, cache_response
from backend.llm.llm_chain import get_answer

router = APIRouter()


@router.get("/")
async def query(q: str):
    # Normalize query
    key = q.strip().lower()

    # Check cache
    cached = get_cached_response(key)
    if cached:
        return {"answer": cached, "source": "cache"}

    # Get LLM answer
    answer = get_answer(q)
    if "couldn't process" in answer:
        raise HTTPException(status_code=500, detail=answer)

    # Cache and return
    cache_response(key, answer)
    return {"answer": answer, "source": "llm"}