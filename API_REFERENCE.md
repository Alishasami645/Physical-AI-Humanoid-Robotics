# API Reference

## Base URL

- **Local Development**: `http://localhost:8000`
- **Production**: `https://your-backend-url.com`

## Authentication

Currently, no authentication is required for public endpoints. For production, implement API key authentication as shown in [DEPLOYMENT_CONFIG.md](DEPLOYMENT_CONFIG.md).

## Endpoints

### Health Check

Check if the API is running.

**Request:**
```http
GET /health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "Robotics Book RAG Chatbot",
  "version": "1.0.0"
}
```

---

### Chat

Process user query and get AI-generated response with sources.

**Request:**
```http
POST /api/chat
Content-Type: application/json

{
  "query": "What is ROS 2?",
  "selected_text": null,
  "conversation_history": []
}
```

**Query Parameters:**
- `query` (string, required): The user's question
- `selected_text` (string, optional): Text selected from the book to explain
- `conversation_history` (array, optional): Previous messages for context

**Conversation History Format:**
```json
[
  {
    "role": "user",
    "content": "What is ROS 2?"
  },
  {
    "role": "assistant",
    "content": "ROS 2 is..."
  }
]
```

**Response (200 OK):**
```json
{
  "answer": "ROS 2 (Robot Operating System 2) is a flexible...",
  "sources": [
    {
      "title": "ROS 2 Architecture Overview",
      "chapter": "Chapter 2",
      "content": "ROS 2 provides a standardized...",
      "score": 0.95,
      "embedding_id": "uuid-here"
    }
  ],
  "query": "What is ROS 2?",
  "selected_text": null
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Query cannot be empty"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "detail": "Internal server error: [error message]"
}
```

---

### Summarize Chapter

Generate a summary for a specific chapter.

**Request:**
```http
GET /api/summarize/{chapter_name}
```

**Path Parameters:**
- `chapter_name` (string): Name of the chapter (e.g., `chapter-02-robotic-nervous-system-ros-2`)

**Response (200 OK):**
```json
{
  "chapter": "chapter-02-robotic-nervous-system-ros-2",
  "summary": "This chapter covers the fundamentals of ROS 2... [comprehensive summary]"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "detail": "No content found for chapter: invalid-chapter"
}
```

---

### Admin: Index Documents (Background)

Start background document indexing task.

**Request:**
```http
POST /api/admin/index
```

**Response (200 OK):**
```json
{
  "status": "started",
  "message": "Document indexing has been started in the background"
}
```

---

### Admin: Index Documents (Sync)

Synchronously index all documents (blocking call).

**Request:**
```http
GET /api/admin/index/sync
```

**Response (200 OK):**
```json
{
  "status": "completed",
  "message": "Document indexing completed successfully",
  "stats": {
    "total_files": 42,
    "indexed_files": 42,
    "total_chunks": 156,
    "errors": [],
    "success": true
  }
}
```

**Response (500 Internal Server Error):**
```json
{
  "detail": "Internal server error: [error details]"
}
```

---

## Request/Response Examples

### Example 1: Basic Question

**Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain the concept of digital twins in robotics",
    "selected_text": null,
    "conversation_history": []
  }'
```

**Response:**
```json
{
  "answer": "A digital twin in robotics is...",
  "sources": [
    {
      "title": "Digital Twin Concept",
      "chapter": "Chapter 3",
      "content": "...",
      "score": 0.92
    }
  ],
  "query": "Explain the concept of digital twins in robotics",
  "selected_text": null
}
```

### Example 2: Selected Text Query

**Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does this mean?",
    "selected_text": "URDF is used to define the structure and properties of a robot",
    "conversation_history": []
  }'
```

**Response:**
```json
{
  "answer": "URDF (Unified Robot Description Format)...",
  "sources": [
    {
      "title": "Understanding URDF Files",
      "chapter": "Chapter 2",
      "content": "...",
      "score": 0.89
    }
  ],
  "query": "What does this mean?",
  "selected_text": "URDF is used to define the structure and properties of a robot"
}
```

### Example 3: Multi-turn Conversation

**Request 1:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is reinforcement learning?",
    "selected_text": null,
    "conversation_history": []
  }'
```

**Response 1:**
```json
{
  "answer": "Reinforcement learning is a machine learning approach...",
  "sources": [...],
  "query": "What is reinforcement learning?",
  "selected_text": null
}
```

**Request 2 (Follow-up):**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How is this applied to robotics?",
    "selected_text": null,
    "conversation_history": [
      {
        "role": "user",
        "content": "What is reinforcement learning?"
      },
      {
        "role": "assistant",
        "content": "Reinforcement learning is a machine learning approach..."
      }
    ]
  }'
```

**Response 2:**
```json
{
  "answer": "In robotics, reinforcement learning enables robots to learn...",
  "sources": [...],
  "query": "How is this applied to robotics?",
  "selected_text": null
}
```

---

## Status Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input (empty query, etc.) |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal error, API/DB issue |
| 503 | Service Unavailable | API temporarily down |

---

## Rate Limiting

Currently not enforced, but recommended for production:

```python
# Add to backend/main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: ChatRequest):
    ...
```

---

## Caching

For production, implement caching:

```python
# Add to backend/main.py
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cache_key(query: str) -> str:
    return hashlib.md5(query.encode()).hexdigest()
```

---

## CORS

By default, CORS is enabled for:
- `http://localhost:3000` (frontend dev)
- `http://localhost:8000` (API dev)
- `https://physical-ai-humanoid-robotics.vercel.app` (production)

To add more origins, update `CORS_ORIGINS` in `.env`:

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://example.com
```

---

## Error Handling

All errors return JSON with detail message:

```json
{
  "detail": "Descriptive error message"
}
```

**Example error:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "", "selected_text": null}'
```

**Response:**
```json
{
  "detail": "Query cannot be empty"
}
```

---

## Rate Limiting (Production)

Implement rate limiting per IP:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: ChatRequest):
    pass
```

---

## Monitoring

Monitor these metrics in production:

- **Response Time**: Time to generate response
- **Token Usage**: OpenAI tokens consumed
- **Cache Hit Rate**: Percentage of cached vs new queries
- **Error Rate**: Failed requests percentage
- **Concurrent Users**: Active connections

---

## Webhooks (Future)

For future implementation:

```python
@app.post("/api/webhooks/chat-completed")
async def on_chat_completed(webhook_data: dict):
    # Handle webhook
    pass
```

---

**Last Updated**: December 18, 2025
