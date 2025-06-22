from langchain.chains.summarize import load_summarize_chain
from backend.llm.ollama_client import ollama_llm
from backend.retrieval.retriever import get_all_chunks_for_document
from backend.utils.logger import logger


def summarize_document(document_name: str, docs) -> str:
    """
    Generates a summary for a document using a map-reduce strategy.
    Args:
        document_name (str): The name of the document being summarized.
        docs (list): List of Document objects to summarize.
    Returns:
        str: The generated summary or an error message.
    """
    logger.info(f"Starting summarization for document: {document_name}")
    if not docs:
        logger.warning(f"No document chunks found for {document_name}. Cannot summarize.")
        return "Could not summarize document. Not found."

    try:
        chain = load_summarize_chain(
            llm=ollama_llm,
            chain_type="map_reduce",
        )
        summary_result = chain.invoke(docs)
        logger.info(f"Successfully generated summary for {document_name}")
        return summary_result["output_text"]
    except Exception as e:
        logger.error(f"Failed to generate summary for {document_name}: {e}")
        return "Failed to generate summary due to an error." 