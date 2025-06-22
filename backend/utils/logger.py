"""
Logger configuration for the Personal AI Assistant project.
Sets up a consistent logging format and log level for the application.
"""
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("personal_ai")