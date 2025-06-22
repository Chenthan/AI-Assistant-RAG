from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.llm.ollama_client import ollama_llm
from backend.repository.document_repository import list_document_names
from backend.utils.logger import logger

async def detect_document_in_query(query: str) -> str | None:
    """
    Uses an LLM to detect if a user's query refers to a specific document.
    Args:
        query (str): The user query string.
    Returns:
        str or None: The detected document name, or None if not found or ambiguous.
    """
    document_names = await list_document_names()
    if not document_names:
        return None

    system_prompt = """You are an expert at reading a user's question and identifying if it refers to one of the available documents.
Your goal is to return only the single, exact document name from the provided list if it is mentioned.
If the question does not seem to refer to any of the documents in the list, or if it is ambiguous, you must return the word 'None'.
Do not add any explanation or preamble. Only return the document name or 'None'.
"""

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Available documents: {document_list}\n\nUser question: {query}\n\nReferenced document:")
    ])

    chain = prompt_template | ollama_llm | StrOutputParser()

    logger.info(f"Detecting document reference in query: '{query}'")
    try:
        detected_name = await chain.ainvoke({
            "document_list": ", ".join(document_names),
            "query": query
        })

        # Clean up the output from the LLM
        detected_name = detected_name.strip().strip("'\"")

        if detected_name in document_names:
            logger.info(f"Detected document: {detected_name}")
            return detected_name
        else:
            logger.info("No specific document detected in query.")
            return None
    except Exception as e:
        logger.error(f"Error during document detection: {e}")
        return None 