# Personal AI Assistant

This project is a backend service for a personal AI assistant. It leverages Retrieval-Augmented Generation (RAG) to answer questions based on documents you provide. You can upload files, and the system will ingest them into a vector database, allowing you to query their content using a large language model.

## Features

- **File Ingestion**: Upload PDF files through a REST API endpoint.
- **Vector Embeddings**: Automatically processes and stores file content in a ChromaDB vector store.
- **RAG Pipeline**: Uses LangChain to orchestrate a Retrieval-Augmented Generation pipeline with Ollama.
- **Question Answering**: Ask questions about your documents through a simple API.
- **Caching**: Caches responses with Redis to provide instant answers for repeated queries.
- **Async API**: Built with FastAPI for high performance.

## Project Structure

```
.
├── backend/
│   ├── api/                  # FastAPI endpoints (file_upload.py, query_handler.py)
│   ├── ingestion/            # File reading and text chunking
│   ├── retrieval/            # ChromaDB and retrieval logic
│   ├── cache/                # Redis utilities
│   ├── llm/                  # Ollama and LangChain integration
│   ├── utils/                # Common utilities (logging, etc.)
│   └── main.py               # FastAPI app factory
├── data/                     # Default directory for uploaded files
├── chroma_db/                # Default directory for ChromaDB persistence
├── .env                      # Environment variables
└── requirements.txt
```

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running.
- A running Redis instance.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd personal-ai-assistant
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

### 3. Install Dependencies

Install all the required packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Set Up Ollama

Pull a model for the assistant to use. We recommend `mistral` or `llama3`.

```bash
ollama pull mistral
```

### 5. Configure Environment Variables

Create a `.env` file in the root of the project by copying the example template.

```bash
# You can manually create a .env file
```

Add the following configuration to your `.env` file. These are the default values.

```env
# .env

# Data and DB paths
DATA_DIR="./data"
CHROMA_DB_DIR="./chroma_db"

# Redis configuration
REDIS_URL="redis://localhost:6379/0"

# Ollama configuration
OLLAMA_BASE_URL="http://localhost:11434"
OLLAMA_MODEL="mistral"

# Server configuration
HOST="0.0.0.0"
PORT="8000"
```

## Usage

### 1. Run the Application

Start the FastAPI server using Uvicorn.

```bash
uvicorn backend.main:app --reload
```

The server will be available at `http://localhost:8000`.

### 2. Upload a File

Use `curl` or any API client to upload a PDF document.

```bash
curl -X POST -F "file=@/path/to/your/document.pdf" http://localhost:8000/upload/
```

On success, you will receive a confirmation message.

### 3. Query Your Document

Ask a question related to the content of your uploaded document(s).

```bash
curl "http://localhost:8000/query/?q=What+is+this+document+about?"
```

The API will return a JSON response with the answer and the source (either `llm` or `cache`).

```json
{
  "answer": "The document is about...",
  "source": "llm"
}
```
