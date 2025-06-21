import os
from fastapi import UploadFile
from datetime import datetime, timezone

BASE_DIR = os.getenv("DATA_DIR", "./data")

def save_file(file: UploadFile) -> str:
    os.makedirs(BASE_DIR, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(BASE_DIR, f"{timestamp}_{file.filename}")
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    return file_path