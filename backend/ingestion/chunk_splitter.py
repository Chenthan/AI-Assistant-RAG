from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def split_text(text: str):
    """
    Splits the input text into chunks suitable for LLM processing.
    Uses a large chunk size to match the context window of the Llama 3.2B model.
    Args:
        text (str): The input text to split.
    Returns:
        list: List of Document objects, each containing a chunk of the text.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=16000,  # Increased for large context window
        chunk_overlap=200
    )
    docs = [Document(page_content=text, metadata={})]
    chunks = splitter.split_documents(docs)
    return chunks