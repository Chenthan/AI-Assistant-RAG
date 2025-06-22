from langchain.chains import RetrievalQA
from backend.llm.ollama_client import ollama_llm
from backend.retrieval.retriever import get_retriever
from backend.utils.logger import logger


def get_answer(query: str, document_name: str | None = None) -> str:
    """
    Generate an answer to a user query using a retrieval-augmented generation chain.
    Args:
        query (str): The user query.
        document_name (str, optional): The document to filter retrieval on.
    Returns:
        str: The generated answer or an error message.
    """
    try:
        # Build retrieval-augmented chain
        retriever = get_retriever(document_name=document_name)
        qa = RetrievalQA.from_chain_type(
            llm=ollama_llm,
            chain_type="stuff",
            retriever=retriever,
        )
        answer = qa.invoke(query)
        logger.info(f"LLM returned answer for query: {query}")
        return answer["result"]
    except Exception as e:
        logger.error(f"LLM chain failed: {e}")
        return "Sorry, I couldn't process your request."

async def generate_summary(chunks):
    """
    Generate a brief summary for a list of document chunks using the LLM.
    Args:
        chunks (list): List of Document objects to summarize.
    Returns:
        str: The generated summary or an error message.
    """
    try:
        text = " ".join([chunk.page_content for chunk in chunks[:10]])  # Limit to first 10 chunks
        prompt = (
            "Summarize the following document briefly:\n\n"
            f"{text}\n\nSummary:"
        )

        response = ollama_llm(prompt)
        return response.strip()
    except Exception as e:
        logger.error(f"Document summarization failed: {e}")
        return "Summary not available."