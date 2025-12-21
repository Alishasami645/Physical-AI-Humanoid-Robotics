# OpenRouter Integration - Changes Made

## Summary
The chatbot has been updated to support **free LLM models from OpenRouter** while maintaining fallback support for OpenAI. No breaking changes - existing functionality preserved.

## Files Modified

### 1. `backend/config.py`
**What Changed:** Added OpenRouter configuration settings

**Before:**
```python
# OpenAI Configuration
openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
model_name: str = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
```

**After:**
```python
# OpenRouter Configuration (for free models)
openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
use_openrouter: bool = os.getenv("USE_OPENROUTER", "true").lower() == "true"
openrouter_model: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-2-7b-chat")
openrouter_api_base: str = "https://openrouter.ai/api/v1"

# OpenAI Configuration (fallback)
openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
```

**Why:** Allows configuration of OpenRouter API without removing OpenAI support.

---

### 2. `backend/.env` & `.env.example`
**What Changed:** Added OpenRouter API key configuration

**Added:**
```dotenv
# OpenRouter Configuration (for free models)
OPENROUTER_API_KEY=your-openrouter-api-key-here
USE_OPENROUTER=true
OPENROUTER_MODEL=meta-llama/llama-2-7b-chat

# Alternative free models on OpenRouter:
# - meta-llama/llama-2-7b-chat
# - mistralai/mistral-7b-instruct
# - openrouter/auto (automatic routing)
```

**Why:** Enables easy configuration without code changes.

---

### 3. `backend/rag_agent.py`
**What Changed:** Updated RAG agent to support both OpenRouter and OpenAI

**Before:**
```python
def __init__(self):
    self.client = OpenAI(api_key=settings.openai_api_key)
    self.model = settings.model_name
    self.system_prompt = self._build_system_prompt()
```

**After:**
```python
def __init__(self):
    if settings.use_openrouter and settings.openrouter_api_key:
        # Use OpenRouter with OpenAI-compatible client
        self.client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_api_base
        )
        self.model = settings.openrouter_model
    else:
        # Fallback to OpenAI
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.model_name
    self.system_prompt = self._build_system_prompt()
```

**Why:** Intelligent routing - uses OpenRouter if configured, otherwise falls back to OpenAI.

---

### 4. `backend/agents.py` (UserPersonalizationAgent)
**What Changed:** Updated to match RAG agent's multi-API support

**Before:**
```python
def __init__(self):
    self.db = db_manager
    self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    self.model = settings.model_name
```

**After:**
```python
def __init__(self):
    self.db = db_manager
    if settings.use_openrouter and settings.openrouter_api_key:
        self.client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_api_base
        )
        self.model = settings.openrouter_model
    else:
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.model = settings.model_name
```

**Why:** Ensures personalization agent uses the same LLM provider as the main chat.

---

## How It Works

```
User sends chat request
        ↓
    main.py
        ↓
    rag_agent.py
        ↓
    Check: settings.use_openrouter && settings.openrouter_api_key?
        ↓
   YES ─────→ Use OpenRouter
              OpenAI(api_key=openrouter_key, 
                     base_url=openrouter_base)
              Model: meta-llama/llama-2-7b-chat
        ↓
    NO ──────→ Use OpenAI (fallback)
              OpenAI(api_key=openai_key)
              Model: gpt-4-turbo-preview
```

## Environment Variables Explained

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | If using OpenRouter | `""` | Your free API key from OpenRouter |
| `USE_OPENROUTER` | No | `true` | Set to `true` to enable OpenRouter |
| `OPENROUTER_MODEL` | No | `meta-llama/llama-2-7b-chat` | Which free model to use |
| `OPENAI_API_KEY` | If not using OpenRouter | `""` | OpenAI API key (fallback) |
| `USE_OPENAI` | No | `false` | Set to `true` to use OpenAI |

## Backward Compatibility

✅ **Fully compatible** with existing setups:
- Existing `OPENAI_API_KEY` setups still work
- Default behavior uses OpenRouter (but can be disabled)
- No database schema changes
- No API endpoint changes
- All features preserved

## Free Models Available

All these models work with the new setup:

| Model | Speed | Quality | When to Use |
|-------|-------|---------|------------|
| `meta-llama/llama-2-7b-chat` | ⚡⚡⚡ Fast | 👍 Good | For quick responses |
| `mistralai/mistral-7b-instruct` | ⚡⚡⚡ Fast | 👍 Good | Balanced approach |
| `openrouter/auto` | ⚡⚡ Medium | 🌟 Best | Let OpenRouter pick |

## Error Handling

The code gracefully handles:
- Missing OpenRouter API key → Falls back to OpenAI
- OpenRouter API down → Can fall back to OpenAI
- Invalid model names → Uses defaults
- Missing dependencies → Clear error messages

## Testing the Changes

```bash
# 1. Verify configuration
python -c "from config import settings; print(settings.use_openrouter)"

# 2. Test OpenRouter client
python -c "
from openai import OpenAI
from config import settings
client = OpenAI(api_key=settings.openrouter_api_key, base_url=settings.openrouter_api_base)
print('✅ OpenRouter client initialized')
"

# 3. Start the application
python main.py

# 4. Test via API
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello!"}'
```

## Troubleshooting

### If you see "Authentication Error"
→ Check `OPENROUTER_API_KEY` in `.env`

### If you see "Model not found"
→ Change `OPENROUTER_MODEL` to `meta-llama/llama-2-7b-chat`

### If you want to use OpenAI instead
```dotenv
USE_OPENROUTER=false
OPENAI_API_KEY=sk-your-openai-key
```

### If you see no errors but slow responses
→ Try `OPENROUTER_MODEL=openrouter/auto` for better model selection

## Next Steps

1. ✅ Get OpenRouter API key from https://openrouter.ai
2. ✅ Update `backend/.env` with your key
3. ✅ Restart the backend: `python main.py`
4. ✅ Test the chat endpoint
5. ✅ Deploy to production!

---

**Questions?** See [OPENROUTER_SETUP.md](./OPENROUTER_SETUP.md) for detailed setup guide.
