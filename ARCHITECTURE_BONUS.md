# Architecture Overview: Tasks 4-7

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React/Docusaurus)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐         ┌──────────────────────┐     │
│  │   AuthProvider       │         │    ChapterActions    │     │
│  │  (Context API)       │         │  (Buttons UI)        │     │
│  │  - signup()          │────────▶│  - Personalize btn   │     │
│  │  - signin()          │         │  - Translate btn     │     │
│  │  - signout()         │         │                      │     │
│  │  - user state        │         └──────────────────────┘     │
│  └──────────────────────┘                   │                  │
│           │                                 │                  │
│           │                        ┌────────▼──────────┐       │
│           │                        │ SignupForm        │       │
│           │                        │ (Collects profile)│       │
│           │                        └──────────────────┘       │
│           │                                 │                  │
│           │                                 │                  │
│  ┌────────▼──────────────────────────────────────────────┐    │
│  │         RoboticsRAGChatbot                            │    │
│  │  - Reads external_id from localStorage               │    │
│  │  - Sends chat + external_id to backend               │    │
│  └────────┬──────────────────────────────────────────────┘    │
│           │                                                   │
└───────────┼───────────────────────────────────────────────────┘
            │
            │ HTTP Requests (with/without external_id)
            │
┌───────────▼───────────────────────────────────────────────────┐
│                    Backend (FastAPI)                          │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            API Endpoints                             │   │
│  │                                                      │   │
│  │  POST /api/auth/signup      ─────────┐              │   │
│  │  POST /api/auth/signin      ─────────┤┐             │   │
│  │  POST /api/agents/personalize ───────┤┤┐            │   │
│  │  GET  /api/agents/chapter_context ──┤┤┤┐           │   │
│  │  POST /api/agents/translate    ─────┤┤┤┤┐          │   │
│  │  POST /api/chat (with external_id)──┤┤┤┤┤          │   │
│  │                                      │││││          │   │
│  └──────────────────────────────────────┼┼┼┼┼──────────┘   │
│                                         │││││             │
│  ┌──────────────────────────────────────▼▼▼▼▼──────────┐   │
│  │         Agent Singletons (Task 4)                  │   │
│  │                                                    │   │
│  │  ┌──────────────────────────────────────────────┐ │   │
│  │  │ UserPersonalizationAgent                     │ │   │
│  │  │  - save_profile()                           │ │   │
│  │  │  - apply_personalization()                  │ │   │
│  │  │  ↓ Modifies RAG prompts                     │ │   │
│  │  └──────────────────────────────────────────────┘ │   │
│  │                                                    │   │
│  │  ┌──────────────────────────────────────────────┐ │   │
│  │  │ ChapterContextAgent                          │ │   │
│  │  │  - get_chapter_context()                    │ │   │
│  │  │  ↓ Returns chapter docs + summary           │ │   │
│  │  └──────────────────────────────────────────────┘ │   │
│  │                                                    │   │
│  │  ┌──────────────────────────────────────────────┐ │   │
│  │  │ TranslationAgent                             │ │   │
│  │  │  - translate_to_urdu()                       │ │   │
│  │  │  ↓ Preserves code blocks + headings          │ │   │
│  │  └──────────────────────────────────────────────┘ │   │
│  │                                                    │   │
│  └────────────────────────────────────────────────────┘   │
│                            │                              │
│  ┌────────────────────────▼─────────────────────────┐   │
│  │         RAG Agent                               │   │
│  │  - answer_question(user_profile)                │   │
│  │  - Applies personalization from profile        │   │
│  │  - Calls OpenAI with customized prompt          │   │
│  └────────────────┬────────────────────────────────┘   │
│                   │                                     │
│  ┌────────────────▼─────────────────────────────────┐   │
│  │         Database Manager                        │   │
│  │  - SQLite (dev) or PostgreSQL (prod)            │   │
│  │                                                  │   │
│  │  Tables:                                         │   │
│  │  ├─ users (with profile fields)                 │   │
│  │  ├─ documents (indexed book content)            │   │
│  │  └─ interactions (chat history)                 │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
            │
            ▼
    ┌──────────────────┐
    │  OpenAI API      │
    │  (Chat + Trans)  │
    └──────────────────┘
```

---

## Data Flow Diagrams

### Task 5 & 6: Signup → Personalization → Personalized Chat

```
User fills SignupForm
         │
         ▼
POST /api/auth/signup
{
  email, software_background, hardware_experience,
  programming_languages, learning_goal
}
         │
         ▼
UserPersonalizationAgent.save_profile()
         │
         ▼
DB: INSERT INTO users (...)
         │
         ▼
frontend: localStorage['external_id'] = user.id
         │
         ├─────────────────────────┐
         │                         │
         ▼                         ▼
User opens chatbot      (same user)
         │
         ▼
Sends: POST /api/chat
{
  query: "What is ROS 2?",
  external_id: "xyz123"   ◄── Sent automatically
}
         │
         ▼
Backend fetches user by external_id
         │
         ▼
RAG Agent applies personalization:
  - Adjusts explanation difficulty
  - Prefers code examples in user's languages
  - Aligns with user's learning goal
         │
         ▼
Response personalized ✓
```

### Task 7: Translate to Urdu

```
User clicks "Translate to Urdu" button
         │
         ▼
Frontend extracts chapter text
         │
         ▼
POST /api/agents/translate
{
  content: "# Chapter...\n```python\nimport rclpy\n```...",
  target: "ur"
}
         │
         ▼
TranslationAgent.translate_to_urdu()
         │
         ▼
LLM System Prompt:
  "Do NOT translate code blocks"
  "Preserve Markdown headings"
  "Use professional Urdu"
         │
         ▼
LLM Response:
# باب ... (chapter heading)

```python
import rclpy  ◄── CODE BLOCK PRESERVED
```

مختلف اردو متن...
         │
         ▼
Opens in new tab ✓
```

---

## Task Mapping to Code

### Task 4: Reusable Agents
```
✓ backend/agents.py
  - UserPersonalizationAgent (class)
  - ChapterContextAgent (class)
  - TranslationAgent (class)
  - user_personalization_agent (singleton)
  - chapter_context_agent (singleton)
  - translation_agent (singleton)
```

### Task 5: Signup & Signin
```
✓ backend/database.py
  - users table schema
  - create_user()
  - get_user_by_id()
  - get_user_by_external_id()
  - update_user_profile()

✓ backend/main.py
  - POST /api/auth/signup (endpoint)
  - POST /api/auth/signin (endpoint)
  - SignupRequest (Pydantic model)
  - SigninRequest (Pydantic model)

✓ frontend: src/components/Auth/SignupForm.tsx
  - Form UI with all fields
  - Calls /api/auth/signup
  - Stores external_id in localStorage
```

### Task 6: Personalization Button
```
✓ backend/rag_agent.py
  - _apply_personalization(user_profile)
  - _build_user_message(..., user_profile)
  - answer_question(..., user_profile)

✓ backend/main.py
  - POST /api/chat (updated to fetch user by external_id)
  - POST /api/agents/personalize (endpoint)
  - ChatRequest (updated with external_id field)

✓ frontend: src/components/ChapterActions/ChapterActions.tsx
  - "Personalize this chapter" button
  - Shows SignupForm for logged-out users
  - Calls /api/agents/personalize for logged-in users

✓ frontend: src/components/RoboticsRAGChatbot/ChatBot.tsx
  - Reads external_id from localStorage
  - Passes external_id with every chat request
```

### Task 7: Urdu Translation
```
✓ backend/agents.py
  - TranslationAgent.translate_to_urdu(content)
  - LLM system prompt for code preservation

✓ backend/main.py
  - POST /api/agents/translate (endpoint)
  - TranslateRequest (Pydantic model)

✓ frontend: src/components/ChapterActions/ChapterActions.tsx
  - "Translate to Urdu" button
  - Extracts chapter content
  - Calls /api/agents/translate
  - Opens result in new tab
```

---

## Database Schema

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  external_id VARCHAR(255) UNIQUE,
  email VARCHAR(255) UNIQUE,
  software_background VARCHAR(50),        -- Beginner|Intermediate|Advanced
  hardware_experience VARCHAR(50),        -- Low|Medium|High
  programming_languages TEXT,             -- JSON array
  learning_goal TEXT,
  metadata TEXT,                          -- JSON
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE documents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title VARCHAR(255),
  chapter VARCHAR(255),
  content TEXT,
  source_url VARCHAR(255),
  embedding_id VARCHAR(255),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
INDEX: idx_documents_chapter

CREATE TABLE interactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_query TEXT,
  assistant_response TEXT,
  selected_text TEXT,
  document_id INTEGER,
  metadata TEXT,                          -- JSON
  created_at TIMESTAMP
);
INDEX: idx_interactions_created
```

---

## Request/Response Examples

### Signup (Task 5)
```json
POST /api/auth/signup

REQUEST:
{
  "email": "user@example.com",
  "software_background": "Intermediate",
  "hardware_experience": "Medium",
  "programming_languages": ["python", "cpp"],
  "learning_goal": "Master ROS 2"
}

RESPONSE:
{
  "status": "ok",
  "user": {
    "id": 1,
    "external_id": "usr_abc123",
    "email": "user@example.com",
    "software_background": "Intermediate",
    "hardware_experience": "Medium",
    "programming_languages": ["python", "cpp"],
    "learning_goal": "Master ROS 2"
  }
}
```

### Chat with Personalization (Task 6)
```json
POST /api/chat

REQUEST:
{
  "query": "Explain ROS 2 nodes",
  "external_id": "usr_abc123"
}

RESPONSE:
{
  "answer": "Nodes are... [explanation adjusted for Intermediate level, with Python examples]",
  "sources": [...],
  "query": "Explain ROS 2 nodes",
  "selected_text": null
}
```

### Translation (Task 7)
```json
POST /api/agents/translate

REQUEST:
{
  "content": "# Nodes\n```python\nimport rclpy\n```\nNodes are...",
  "target": "ur"
}

RESPONSE:
{
  "status": "ok",
  "translated": "# نوڈز\n```python\nimport rclpy\n```\nنوڈز ہیں..."
}
```

---

## Deployment Considerations

### Development (Current)
- SQLite: `sqlite:///./robotics_book.db`
- Backend: `http://127.0.0.1:8000`
- Frontend: `http://localhost:3000`
- No external services required

### Production
- PostgreSQL: Set `DATABASE_URL` to Neon/AWS RDS
- Backend: Deploy to Heroku/AWS/GCP
- Frontend: Deploy to Vercel/Netlify
- OpenAI API key required (already in `.env`)
- CORS: Update `CORS_ORIGINS` to production domain

---

## Points Summary

| Task | Agents Used | Points |
|------|------------|--------|
| 4 | UserPersonalization, ChapterContext, Translation (singletons, reusable) | +50 |
| 5 | UserPersonalization (save/retrieve) | +50 |
| 6 | UserPersonalization (apply to RAG) | +50 |
| 7 | Translation (Urdu with code preservation) | +50 |
| **TOTAL** | | **+200** |

---

**All 4 bonus tasks fully implemented and integrated!** 🎉
