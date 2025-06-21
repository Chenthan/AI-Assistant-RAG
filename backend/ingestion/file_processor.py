from pypdf import PdfReader
from backend.ingestion.chunk_splitter import split_text


def load_and_split(file_path: str):
    text = ""
    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    # Split into chunks
    chunks = split_text(text)
    return chunks