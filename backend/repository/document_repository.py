from backend.repository.mongo_client import documents_collection
from datetime import datetime, timezone

async def save_document(file_name: str, file_path: str, file_type: str, chunk_count: int, summary: str):
    """
    Save a document's metadata to the MongoDB collection.
    Args:
        file_name (str): Name of the file.
        file_path (str): Path to the file.
        file_type (str): MIME type of the file.
        chunk_count (int): Number of chunks the file was split into.
        summary (str): Summary of the document.
    Returns:
        str: The document ID of the saved document.
    """
    document = {
        "_id": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"),
        "file_name": file_name,
        "file_path": file_path,
        "upload_time": datetime.now(timezone.utc).isoformat(),
        "file_type": file_type,
        "chunk_count": chunk_count,
        "summary": summary
    }
    await documents_collection.insert_one(document)
    return document["_id"]


async def list_document_names():
    """
    Returns a list of all document file names.
    Returns:
        list: List of file names (str).
    """
    docs = await documents_collection.find({}, {"file_name": 1, "_id": 0}).to_list(
        length=100
    )
    return [doc["file_name"] for doc in docs]


async def list_documents():
    """
    Returns a list of all documents in the collection.
    Returns:
        list: List of document dicts.
    """
    docs = await documents_collection.find().to_list(length=100)
    return docs

async def get_document_by_id(doc_id: str):
    """
    Retrieve a document by its ID.
    Args:
        doc_id (str): The document ID.
    Returns:
        dict or None: The document if found, else None.
    """
    return await documents_collection.find_one({"_id": doc_id})

async def delete_document(doc_id: str):
    """
    Delete a document by its ID.
    Args:
        doc_id (str): The document ID.
    Returns:
        int: The number of documents deleted (0 or 1).
    """
    result = await documents_collection.delete_one({"_id": doc_id})
    return result.deleted_count
