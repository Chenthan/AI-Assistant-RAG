from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = [Document(page_content=text, metadata={})]
    chunks = splitter.split_documents(docs)
    return chunks