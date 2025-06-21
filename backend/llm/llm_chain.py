from langchain.chains import RetrievalQA
from backend.llm.ollama_client import ollama_llm
from backend.retrieval.retriever import get_retriever
from backend.utils.logger import logger


def get_answer(query: str) -> str:
    try:
        # Build retrieval-augmented chain
        retriever = get_retriever()
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
