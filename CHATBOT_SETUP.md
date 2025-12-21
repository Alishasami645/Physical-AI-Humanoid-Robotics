# Robotics Book RAG Chatbot Setup Guide

## Overview

This is a comprehensive Retrieval-Augmented Generation (RAG) chatbot integrated into the Physical AI & Humanoid Robotics Docusaurus book. The system uses:

- **Backend**: FastAPI with Python
- **LLM**: OpenAI GPT-4 Turbo
- **Vector Store**: Qdrant Cloud Free Tier
- **Database**: Neon Serverless Postgres
- **Frontend**: React with TypeScript

## Architecture

```
┌─────────────────────┐
│   Docusaurus Site   │
│   (React Frontend)  │
└──────────┬──────────┘
           │
           ↓ HTTP API Calls
┌─────────────────────┐
│   FastAPI Backend   │
│   (Python/Uvicorn)  │
└──────────┬──────────┘
           │
    ┌──────┴──────────┬──────────────┐
    ↓                 ↓              ↓
┌─────────┐    ┌──────────────┐  ┌───────────┐
│ OpenAI  │    │ Neon Postgres│  │  Qdrant   │
│  GPT-4  │    │  (Database)  │  │  (Vector) │
└─────────┘    └──────────────┘  └───────────┘
```

## Prerequisites

- Python 3.8+
- Node.js 20+
- npm or yarn
- Git

## Setup Instructions

### 1. Backend Setup

#### Step 1: Create Virtual Environment

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Neon Postgres Configuration
DATABASE_URL=postgresql://user:password@host/dbname

# Qdrant Configuration
QDRANT_URL=https://your-qdrant-instance.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key_here

# Server Configuration
BACKEND_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://physical-ai-humanoid-robotics.vercel.app

# LLM Configuration
MODEL_NAME=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-small
```

#### Step 4: Get API Keys

**OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy and paste into `.env`

**Qdrant Cloud:**
1. Sign up at https://cloud.qdrant.io
2. Create a free tier cluster
3. Copy API URL and API Key into `.env`

**Neon Postgres:**
1. Sign up at https://neon.tech
2. Create a new project and database
3. Copy connection string into `.env`

#### Step 5: Initialize Database and Index Documents

```bash
# Start Python shell
python

# Run these commands:
from database import db_manager
from document_indexer import index_robotics_book

# Initialize database tables
db_manager.init_db()

# Index all documents (this takes a few minutes)
stats = index_robotics_book(docs_path="../docs")
print(stats)

# Exit
exit()
```

#### Step 6: Start FastAPI Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Base URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### 2. Frontend Setup

The chatbot is already integrated into the Docusaurus site. You just need to add the backend URL configuration.

#### Step 1: Update Environment Variables

Create a `.env.local` file in the project root:

```env
REACT_APP_BACKEND_URL=http://localhost:8000
```

#### Step 2: Ensure Dependencies

The frontend dependencies are in `package.json`. If you need to add any:

```bash
npm install
```

#### Step 3: Start Docusaurus

```bash
npm start
```

The site will be available at http://localhost:3000

## API Documentation

### Chat Endpoint

**POST** `/api/chat`

Request body:
```json
{
  "query": "What is ROS 2?",
  "selected_text": "Optional selected text from the book",
  "conversation_history": [
    {
      "role": "user",
      "content": "Previous question"
    },
    {
      "role": "assistant",
      "content": "Previous answer"
    }
  ]
}
```

Response:
```json
{
  "answer": "ROS 2 is the Robot Operating System version 2...",
  "sources": [
    {
      "title": "ROS 2 Architecture",
      "chapter": "Chapter 2",
      "content": "...",
      "score": 0.92
    }
  ],
  "query": "What is ROS 2?",
  "selected_text": null
}
```

### Summarize Endpoint

**GET** `/api/summarize/{chapter_name}`

Response:
```json
{
  "chapter": "chapter-02-robotic-nervous-system-ros-2",
  "summary": "This chapter covers..."
}
```

### Admin Endpoints

**POST** `/api/admin/index/sync` - Synchronous indexing
**POST** `/api/admin/index` - Background indexing
**GET** `/health` - Health check

## Features

### 1. RAG Query Processing

- Retrieves relevant documents from Qdrant
- Uses OpenAI GPT-4 to generate contextual answers
- Provides source citations

### 2. Text Selection Support

- Users can select text in the book
- Chatbot focuses on explaining selected content
- Visual indicator shows selected text context

### 3. Conversation History

- Maintains multi-turn conversations
- Understands context from previous messages
- Stores interactions in Postgres for analytics

### 4. Source Attribution

- Shows which book sections were used
- Displays relevance scores
- Links to original content

## Deployment

### Frontend Deployment (Vercel)

The site is already deployed at https://physical-ai-humanoid-robotics.vercel.app

To redeploy after changes:

```bash
npm run build
# Push to GitHub, Vercel auto-deploys
```

### Backend Deployment

#### Option 1: Heroku

```bash
# Install Heroku CLI
# Then:
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
heroku config:set DATABASE_URL=your_db_url
heroku config:set QDRANT_URL=your_qdrant_url
heroku config:set QDRANT_API_KEY=your_key
git push heroku main
```

#### Option 2: Railway

```bash
# Install Railway CLI
railway init
railway link
railway variables add OPENAI_API_KEY your_key
# ... add other variables
railway up
```

#### Option 3: Docker

```bash
# Build image
docker build -t robotics-chatbot-backend .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e DATABASE_URL=your_db \
  -e QDRANT_URL=your_url \
  -e QDRANT_API_KEY=your_key \
  robotics-chatbot-backend
```

## Troubleshooting

### Issue: "Connection refused" to backend

**Solution**: Make sure FastAPI server is running on port 8000
```bash
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

### Issue: Embedding model not found

**Solution**: Ensure OpenAI API key is valid and account has access to embedding models

```bash
python -c "
from openai import OpenAI
client = OpenAI(api_key='your_key')
response = client.embeddings.create(
    input='test',
    model='text-embedding-3-small'
)
print('Success!')
"
```

### Issue: Qdrant collection creation fails

**Solution**: Check Qdrant URL and API key, ensure they're correct

```bash
python -c "
from qdrant_client import QdrantClient
client = QdrantClient(url='your_url', api_key='your_key')
print(client.get_collections())
"
```

### Issue: Document indexing is slow

**Solution**: 
- This is normal for the first run (can take 5-10 minutes)
- Check that Qdrant and Postgres are responding
- Reduce batch size if needed in `document_indexer.py`

## File Structure

```
robotics-book/
├── backend/
│   ├── main.py                  # FastAPI application
│   ├── config.py                # Configuration management
│   ├── database.py              # Postgres/Neon operations
│   ├── vector_store.py          # Qdrant operations
│   ├── rag_agent.py             # OpenAI RAG logic
│   ├── document_indexer.py      # Document processing
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   └── .env                     # Local environment (gitignored)
├── src/
│   ├── components/
│   │   ├── RoboticsRAGChatbot/  # Main chatbot component
│   │   │   ├── ChatBot.tsx
│   │   │   ├── ChatBot.module.css
│   │   │   └── index.ts
│   │   └── ChatbotWrapper.tsx   # Wrapper for Docusaurus
│   ├── theme/
│   │   └── Root.tsx             # Theme wrapper for chatbot
│   └── ...
└── docs/
    ├── intro.md
    ├── chapter-*.../
    │   └── lesson-*.md
    └── ...
```

## Performance Optimization

### Vector Store Optimization

- Embedding model: `text-embedding-3-small` (efficient)
- Similarity threshold: 0.7 (adjustable in `vector_store.py`)
- Search limit: 5 results (adjustable in `rag_agent.py`)

### LLM Optimization

- Model: GPT-4 Turbo (best quality-to-cost ratio)
- Max tokens: 1500 per response
- Temperature: 0.7 (balanced creativity)

### Database Optimization

- Indexes on commonly searched columns
- Connection pooling enabled
- Queries optimized with proper WHERE clauses

## Security Considerations

1. **API Keys**: Keep all API keys in `.env` (never commit)
2. **CORS**: Whitelist specific origins in production
3. **Rate Limiting**: Implement rate limiting for public deployments
4. **Input Validation**: All inputs are validated with Pydantic
5. **Authentication**: Consider adding API key authentication for admin endpoints

## Future Enhancements

- [ ] User authentication and personalized conversation history
- [ ] Feedback mechanism to improve answer quality
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Fine-tuning on robotics-specific content
- [ ] Integration with robotics simulation tools
- [ ] Voice input/output support
- [ ] Export conversation as PDF

## Support and Contribution

For issues or contributions:
1. Check existing GitHub issues
2. Create detailed bug reports
3. Submit pull requests with tests

## License

This project is part of the Physical AI & Humanoid Robotics educational book.

---

**Last Updated**: December 18, 2025
**Version**: 1.0.0
