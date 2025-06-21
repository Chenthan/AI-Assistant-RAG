from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.utils.file_saver import save_file
from backend.ingestion.file_processor import load_and_split
from backend.retrieval.vector_store import store_embeddings

router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    # Save file
    file_path = save_file(file)
    if not file_path:
        raise HTTPException(status_code=500, detail="File save failed")

    # Ingest and split
    chunks = load_and_split(file_path)

    # Store embeddings
    db = store_embeddings(chunks)
    return {"status": "success", "chunks_stored": len(chunks)}