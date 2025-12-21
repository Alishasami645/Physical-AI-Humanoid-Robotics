# Robotics Book RAG Chatbot Backend

FastAPI backend for the Retrieval-Augmented Generation (RAG) chatbot integrated into the Physical AI & Humanoid Robotics book.

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Initialize and index
python setup.py

# 5. Start server
python -m uvicorn main:app --reload --port 8000
```

API will be available at: http://localhost:8000/docs

## Architecture

- **Framework**: FastAPI (async Python)
- **LLM**: OpenAI GPT-4 Turbo
- **Vector DB**: Qdrant (semantic search)
- **Relational DB**: Neon Postgres (data storage)
- **Deployment**: Docker, Heroku, Railway, AWS Lambda

## Key Components

### 1. `config.py`
Loads environment variables and manages application settings.

### 2. `database.py`
Manages Neon Postgres connections and operations.
- Tables: `documents`, `interactions`
- Operations: CRUD for documents and user interactions

### 3. `vector_store.py`
Manages Qdrant vector database for semantic search.
- Embedding model: `text-embedding-3-small`
- Distance metric: Cosine similarity
- Operations: Add documents, search similar

### 4. `rag_agent.py`
Main RAG (Retrieval-Augmented Generation) logic.
- Retrieves relevant documents
- Generates context-aware responses
- Maintains conversation history

### 5. `document_indexer.py`
Processes markdown files from the book and indexes them.
- Chunks documents for better retrieval
- Generates embeddings
- Stores in Qdrant and Postgres

### 6. `main.py`
FastAPI application with endpoints.
- POST `/api/chat`: Answer questions
- GET `/api/summarize/{chapter}`: Summarize chapter
- POST `/api/admin/index`: Index documents
- GET `/health`: Health check

## Environment Variables

```env
# OpenAI
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-small

# Neon Postgres
DATABASE_URL=postgresql://user:pass@host/db

# Qdrant
QDRANT_URL=https://...
QDRANT_API_KEY=...

# Server
BACKEND_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## API Endpoints

### POST /api/chat
Answer questions about the book.

```json
{
  "query": "What is ROS 2?",
  "selected_text": null,
  "conversation_history": []
}
```

### GET /api/summarize/{chapter_name}
Generate chapter summary.

### POST /api/admin/index
Index documents (background task).

### GET /api/admin/index/sync
Index documents (blocking).

### GET /health
Health check.

## Development

```bash
# Auto-reload on file changes
python -m uvicorn main:app --reload

# Check configuration
python diagnostics.py

# Run setup
python setup.py
```

## Production Deployment

See [DEPLOYMENT_CONFIG.md](../DEPLOYMENT_CONFIG.md) for:
- Docker deployment
- Heroku deployment
- Railway deployment
- AWS Lambda deployment
- GitHub Actions CI/CD

## Troubleshooting

```bash
# Run diagnostics
python diagnostics.py

# Check API docs
http://localhost:8000/docs

# Index documents
python -c "from document_indexer import index_robotics_book; index_robotics_book()"
```

## Performance

- **Embedding**: ~100ms (small model)
- **Semantic Search**: ~200ms (5 documents)
- **LLM Response**: ~2-5s (GPT-4 Turbo)
- **Total**: ~3-7s per query

## Security

- API keys in `.env` (never commit)
- CORS configured for specific origins
- Input validation with Pydantic
- SQL injection protection with parameterized queries

## License

Part of Physical AI & Humanoid Robotics book project.

---

For full documentation, see:
- [CHATBOT_SETUP.md](../CHATBOT_SETUP.md) - Complete setup guide
- [API_REFERENCE.md](../API_REFERENCE.md) - API documentation
- [INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md) - Integration steps
