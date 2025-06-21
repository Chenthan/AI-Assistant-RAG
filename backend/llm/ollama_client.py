import os
from langchain_community.llms import Ollama
from backend.utils.logger import logger

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

try:
    ollama_llm = Ollama(base_url=OLLAMA_BASE_URL, model=OLLAMA_MODEL)
    logger.info("Ollama LLM initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Ollama LLM: {e}")
    ollama_llm = None