import os
from fastapi import FastAPI
from dotenv import load_dotenv
from backend.api.file_upload import router as upload_router
from backend.api.query_handler import router as query_router

# Load environment variables
load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Personal AI Assistant",
        description="Local-first AI assistant backend",
        version="0.1.0"
    )

    # Include routers
    app.include_router(upload_router, prefix="/upload", tags=["file-upload"])
    app.include_router(query_router, prefix="/query", tags=["query"])

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "backend.main:app",
        host=HOST,
        port=PORT,
        reload=True
    )