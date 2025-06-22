from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.repository.document_repository import save_document
from backend.utils.file_saver import save_file
from backend.ingestion.file_processor import load_and_split
from backend.retrieval.vector_store import store_embeddings
from backend.llm.summarization_chain import summarize_document

router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file, process it, store embeddings, generate a summary, and save metadata.
    Args:
        file (UploadFile): The file to upload and process.
    Returns:
        dict: Status, number of chunks stored, and the generated summary.
    """
    # Save file
    file_path = save_file(file)
    if not file_path:
        raise HTTPException(status_code=500, detail="File save failed")

    # Ingest and split
    chunks = load_and_split(file_path)

    # Store embeddings
    chunks = store_embeddings(chunks, file.filename)

    # Generate and save summary
    summary = summarize_document(file.filename, chunks)

    # Save document metadata to database
    await save_document(
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        chunk_count=len(chunks),
        summary=summary,
    )

    return {
        "status": "success",
        "chunks_stored": len(chunks),
        "summary": summary,
    }