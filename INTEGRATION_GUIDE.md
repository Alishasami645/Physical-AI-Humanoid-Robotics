# RAG Chatbot Integration Guide

## Quick Start

### 1. Start Backend (Terminal 1)

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run setup (optional but recommended)
python setup.py

# Start server
python -m uvicorn main:app --reload --port 8000
```

The backend will be available at: **http://localhost:8000**
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 2. Start Frontend (Terminal 2)

```bash
# Make sure you're in the project root
npm start
```

The frontend will be available at: **http://localhost:3000**

### 3. Test the Chatbot

- Open http://localhost:3000
- Look for the chat button in the bottom-right corner
- Click it and start asking questions!

## Architecture

```
Frontend (React/Docusaurus)
    ↓
    ↓ HTTP Requests
    ↓
Backend (FastAPI)
    ├── LLM: OpenAI GPT-4
    ├── Vector DB: Qdrant
    └── Relational DB: Neon Postgres
```

## Features

### 1. Regular Q&A
Ask any question about the robotics book content.

**Example questions:**
- "What is ROS 2?"
- "How does a digital twin work?"
- "Explain the Gazebo simulation environment"
- "What is reinforcement learning in robotics?"

### 2. Selected Text Explanation
1. Select any text in the book
2. The chatbot will focus on explaining that specific content

**Example:**
Select: "URDF stands for Unified Robot Description Format"
Ask: "What does this mean?"

### 3. Multi-turn Conversations
The chatbot maintains conversation context for follow-up questions.

**Example conversation:**
- User: "What is ROS 2?"
- Assistant: [explains ROS 2]
- User: "Can you explain that more simply?"
- Assistant: [simplified explanation with context]

## Customization

### Change Backend URL

Create `.env.local` in project root:

```env
REACT_APP_BACKEND_URL=http://your-backend-url:8000
```

### Change Chatbot Appearance

Edit `src/components/RoboticsRAGChatbot/ChatBot.module.css`:

```css
.chatButton {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); /* Change colors */
  width: 60px;  /* Change size */
  height: 60px;
}

.chatContainer {
  width: 420px;  /* Change window width */
  max-height: 600px;  /* Change window height */
}
```

### Change System Prompt

Edit `backend/rag_agent.py`, method `_build_system_prompt()`:

```python
def _build_system_prompt(self) -> str:
    return """Your custom system prompt here..."""
```

### Change Number of Search Results

Edit `backend/rag_agent.py`:

```python
relevant_docs = vector_store.search_similar(query, limit=10)  # Change from 5
```

## API Usage

### Python Example

```python
import requests

# Send a question
response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "query": "What is ROS 2?",
        "selected_text": None,
        "conversation_history": []
    }
)

result = response.json()
print(result["answer"])
print(f"Sources: {len(result['sources'])}")
```

### JavaScript/TypeScript Example

```typescript
const response = await fetch("http://localhost:8000/api/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    query: "What is ROS 2?",
    selected_text: null,
    conversation_history: [],
  }),
});

const data = await response.json();
console.log(data.answer);
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is ROS 2?",
    "selected_text": null,
    "conversation_history": []
  }'
```

## Troubleshooting

### Issue: Chatbot doesn't appear

**Solution:**
1. Check browser console for errors (F12)
2. Verify backend is running: `curl http://localhost:8000/health`
3. Check CORS settings in `backend/config.py`

### Issue: "Failed to fetch from backend"

**Solution:**
1. Backend URL is incorrect or backend is not running
2. Check `.env.local` has correct `REACT_APP_BACKEND_URL`
3. Make sure backend is accessible: `http://localhost:8000/docs`

### Issue: Empty or generic responses

**Solution:**
1. Documents haven't been indexed yet
2. Run: `python backend/setup.py` → choose to index documents
3. Or manually: `python -c "from backend.document_indexer import index_robotics_book; index_robotics_book()"`

### Issue: "Invalid API Key" from OpenAI

**Solution:**
1. Check `.env` has correct `OPENAI_API_KEY`
2. Get key from: https://platform.openai.com/api-keys
3. Test with: `python backend/diagnostics.py`

### Issue: Database connection error

**Solution:**
1. Check `DATABASE_URL` in `.env`
2. Verify Neon database is running and accessible
3. Test with: `python backend/diagnostics.py`

### Issue: Qdrant connection error

**Solution:**
1. Check `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
2. Verify Qdrant instance is running
3. Test with: `python backend/diagnostics.py`

## Development Workflow

### 1. Making Changes to Backend

```bash
cd backend
# Backend auto-reloads with --reload flag
# Edit files and save, changes apply immediately
```

### 2. Making Changes to Frontend

```bash
# Frontend auto-reloads
# Edit files and save, browser refreshes automatically
```

### 3. Adding New Features

#### Backend Example: Add new API endpoint

```python
# In backend/main.py
@app.get("/api/new-feature")
async def new_feature():
    return {"message": "New feature"}
```

#### Frontend Example: Add new UI element

```typescript
// In src/components/RoboticsRAGChatbot/ChatBot.tsx
<div className={styles.newElement}>
  {/* Your UI */}
</div>
```

## Advanced Configuration

### Set Log Level

```python
# backend/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Enable Database Query Logging

```python
# backend/database.py
import psycopg2
psycopg2.extensions.set_wait_callback(...)
```

### Adjust LLM Parameters

```python
# backend/rag_agent.py
response = self.client.chat.completions.create(
    model=self.model,
    messages=messages,
    temperature=0.5,  # Lower = more consistent
    max_tokens=2000,  # Increase for longer responses
)
```

## Performance Tips

1. **Index Caching**: Results are cached in Postgres
2. **Embedding Optimization**: Using small embedding model (fast)
3. **Response Limiting**: Only retrieving top 5 relevant documents
4. **Connection Pooling**: Database connections are pooled

## Testing

### Test Backend

```bash
# Health check
curl http://localhost:8000/health

# API docs
http://localhost:8000/docs

# Test chat endpoint
python -c "
import requests
response = requests.post(
    'http://localhost:8000/api/chat',
    json={'query': 'test', 'selected_text': None, 'conversation_history': []}
)
print(response.json())
"
```

### Test Frontend

```bash
# Component loads
Check browser console for React errors

# Text selection works
Select any text on page, should show in chat input

# Messages send/receive
Type a question and press Enter
```

## Deployment

See [DEPLOYMENT_CONFIG.md](DEPLOYMENT_CONFIG.md) for production deployment instructions.

## Support

For issues or questions:
1. Check this guide first
2. Run `python backend/diagnostics.py` to check configuration
3. Check browser console (F12) for frontend errors
4. Check terminal output for backend errors

---

**Last Updated**: December 18, 2025
