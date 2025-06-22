# 🎯 AI-Assistant-RAG

A **private, personal AI assistant** built using Retrieval-Augmented Generation (RAG). Upload your own documents and let the assistant answer questions *contextually*, with awareness of available files, summaries, and intelligent retrieval.

---

## 🚀 Features

### 🔹 Document Ingestion & Chunking
- Supports **PDF** and **plain text** uploads
- **Efficient chunking** using LangChain's `RecursiveCharacterTextSplitter`
- Chunks include metadata: `document_name`, `upload_time`

### 🔹 Vector Storage & Retrieval
- Uses **ChromaDB** vector store to store embeddings
- Supports **filtered retrieval** by document name
- Supports **semantic retrieval** across all documents

### 🔹 LLM Integration
- Powered by **Ollama** (local LLM) via `langchain-ollama`
- Enhanced prompt engineering to include document context
- **Cached responses** using Redis for faster repeat queries

### 🔹 Memory & Catalog
- Stores document metadata (name, path, upload time, chunk count, summary) in MongoDB
- Automatically **summarizes** each document on upload
- Makes the assistant **"aware" of available documents**

### 🔹 Smart Query Handling
- Intelligent document detection via **summary embedding similarity**
- Retrieval filters queries to appropriate document chunks
- Graceful fallback when no relevant document is identified

---

## 🏗️ Architecture & Flow

1. **Upload** → ingest, chunk, embed, store in ChromaDB (with metadata)
2. **Summarize** → generate a short summary for each uploaded document
3. **Store metadata** → MongoDB (`documents` collection)
4. **Query** → detect relevant document via summary similarity  
   → retrieve filtered chunks  
   → send context + query to LLM  
   → return answer (cached for next time)

---

## 🛠️ Tech Stack

| Layer               | Tools & Libraries                |
|---------------------|----------------------------------|
| API Framework       | FastAPI, Uvicorn                 |
| File Ingestion      | pypdf                            |
| Chunking            | langchain.text_splitter          |
| Embeddings & LLM    | langchain-ollama, Ollama         |
| Vector Store        | ChromaDB (langchain-chroma)      |
| Caching             | Redis                            |
| Metadata Storage    | MongoDB (motor)                  |
| Orchestration       | langchain                        |
| Config Management   | python-dotenv                    |
| Logging             | logging (Python stdlib)          |

---

## 📋 Quickstart Guide

### 1. Clone & set up environment
```bash
git clone https://github.com/Chenthan/AI-Assistant-RAG.git
cd AI-Assistant-RAG
python -m venv .venv
source .venv/bin/activate
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Run pre-req services
Make sure you have Docker Desktop running:
```bash
docker run -d --name redis -p 6379:6379 redis
docker run -d --name mongo -p 27017:27017 mongo
```
### 4. Configure .env
env
```
DATA_DIR="./data"
CHROMA_DB_DIR="./chroma_db"
REDIS_URL="redis://localhost:6379/0"
MONGO_URL=mongodb://localhost:27017
OLLAMA_BASE_URL="http://localhost:11434"
OLLAMA_MODEL="llama3.2"
HOST="0.0.0.0"
PORT="8000"
```
### 5. Start FastAPI server
```bash
uvicorn backend.main:app --reload --port "${PORT:-8000}"
```
### 6. Use the API
```
POST /upload/ – Upload your PDF or TXT file

GET /query/?q=<your question> – Ask anything! The assistant will detect relevant documents, retrieve related chunks, and answer using LLM.
```

### 📂 Repository Structure
pgsql
```
AI-Assistant-RAG/
├── backend/
│   ├── api/                # File upload & query handlers
│   ├── db/                 # MongoDB client & document repo
│   ├── ingestion/          # File reading & chunking
│   ├── retrieval/          # ChromaDB wrapper & retrieval logic
│   ├── llm/                # Ollama & chain logic for summarization & QA
│   ├── cache/              # Redis caching utilities
│   ├── utils/              # File saving, logging helpers
│   └── main.py             # FastAPI app
├── requirements.txt
└── README.md
```

### 🔗 Acknowledgments & References

* RAG architecture with LangChain and Ollama
* Dictionary and memory architecture with MongoDB and Redis
* Prompt enrichment and document-aware QA

