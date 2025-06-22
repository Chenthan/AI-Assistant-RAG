from pypdf import PdfReader
from backend.ingestion.chunk_splitter import split_text
from backend.utils.logger import logger

def load_and_split(file_path: str):
    """
    Loads a file (PDF or text), extracts its content, and splits it into chunks.
    Args:
        file_path (str): Path to the file to load.
    Returns:
        list: List of Document objects representing the file's content in chunks.
    """
    logger.info(f"Loading file from {file_path}")
    text = ""
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
        logger.info(f"Text extracted")
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    logger.info(f"Text loaded")
    # Split into chunks
    chunks = split_text(text)
    logger.info(f"Chunks split")
    return chunks