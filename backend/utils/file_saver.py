import os
from fastapi import UploadFile
from datetime import datetime, timezone
from backend.utils.logger import logger

BASE_DIR = os.getenv("DATA_DIR", "./data")

def save_file(file: UploadFile) -> str:
    """
    Save an uploaded file to the configured base directory with a timestamped filename.
    Args:
        file (UploadFile): The file to save.
    Returns:
        str: The path to the saved file.
    """
    logger.info(f"Saving file to {BASE_DIR}")
    os.makedirs(BASE_DIR, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(BASE_DIR, f"{timestamp}_{file.filename}")
    with open(file_path, "wb") as f:
        content = file.file.read()
        logger.info(f"Content read")
        f.write(content)
    logger.info(f"File saved to {file_path}")
    return file_path