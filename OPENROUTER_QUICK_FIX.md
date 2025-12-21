# OpenRouter Free Module Chatbot - Quick Fix Guide

## 🚨 Common Errors & Fixes

### Error 1: `Authentication Error: Invalid API Key`

**What's happening?**
- Your OpenRouter API key is missing or incorrect
- Or `USE_OPENROUTER` is set but key is empty

**Quick Fix:**
```bash
# 1. Get your free key from https://openrouter.ai/keys
# 2. Update backend/.env:
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxx
USE_OPENROUTER=true

# 3. Restart the application
```

---

### Error 2: `Model Not Found` or `Invalid Model`

**What's happening?**
- The model name in `OPENROUTER_MODEL` doesn't exist or is misspelled

**Quick Fix:**
```dotenv
# Use a reliable free model:
OPENROUTER_MODEL=meta-llama/llama-2-7b-chat
# OR
OPENROUTER_MODEL=mistralai/mistral-7b-instruct
# OR (automatic best available)
OPENROUTER_MODEL=openrouter/auto
```

---

### Error 3: `Connection Timeout` or `Failed to Connect`

**What's happening?**
- Network issue or OpenRouter API is down (rare)
- Rate limit exceeded (uncommon on free tier)

**Quick Fix:**
```bash
# Test the connection:
curl https://openrouter.ai/api/v1/models

# If fails, check:
# 1. Internet connection
# 2. OpenRouter status: https://status.openrouter.ai
# 3. Try again in a few moments
```

---

### Error 4: `NameError: name 'settings' is not defined`

**What's happening?**
- Imports are missing or config.py has issues

**Quick Fix:**
```python
# In rag_agent.py or agents.py, ensure this import exists:
from config import settings

# Make sure config.py is in the same directory as the script
```

---

### Error 5: `Module 'openai' has no attribute 'OpenAI'`

**What's happening?**
- Old version of OpenAI Python library

**Quick Fix:**
```bash
# Update the OpenAI library:
pip install --upgrade openai

# Or install specific version (3.0+):
pip install openai>=1.0.0
```

---

## 🔧 Step-by-Step Setup (5 minutes)

### 1. Get OpenRouter Key (2 min)
```
→ Visit: https://openrouter.ai/keys
→ Sign up (free)
→ Create API Key
→ Copy the key (starts with "sk-or-")
```

### 2. Update Environment (1 min)
**File: `backend/.env`**
```dotenv
OPENROUTER_API_KEY=sk-or-your-actual-key-here
USE_OPENROUTER=true
OPENROUTER_MODEL=meta-llama/llama-2-7b-chat
```

### 3. Verify Configuration (1 min)
```bash
cd backend
python -c "from config import settings; print(f'Model: {settings.openrouter_model}'); print(f'Using OpenRouter: {settings.use_openrouter}')"
```

**Expected output:**
```
Model: meta-llama/llama-2-7b-chat
Using OpenRouter: True
```

### 4. Test Chat (1 min)
```bash
python main.py
# In another terminal:
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is robotics?"}'
```

---

## 💡 Pro Tips

### Tip 1: Use `openrouter/auto` for Best Results
```dotenv
# This lets OpenRouter pick the best available free model
OPENROUTER_MODEL=openrouter/auto
```

### Tip 2: Check Your Usage
- Visit: https://openrouter.ai/activity
- See real-time API usage
- Monitor free tier limits

### Tip 3: Fallback to OpenAI (if needed)
```bash
# Disable OpenRouter temporarily:
USE_OPENROUTER=false
OPENAI_API_KEY=sk-your-openai-key
```

### Tip 4: Test with Different Models
```bash
# Quick test script:
python -c "
from openai import OpenAI
from config import settings

client = OpenAI(
    api_key=settings.openrouter_api_key,
    base_url=settings.openrouter_api_base
)

response = client.chat.completions.create(
    model=settings.openrouter_model,
    messages=[{'role': 'user', 'content': 'Hello!'}],
    max_tokens=50
)

print(response.choices[0].message.content)
"
```

---

## 📋 Checklist Before Going Live

- [ ] OpenRouter account created
- [ ] API key obtained (starts with `sk-or-`)
- [ ] `.env` file updated with key
- [ ] `USE_OPENROUTER=true` set
- [ ] Model name is correct (e.g., `meta-llama/llama-2-7b-chat`)
- [ ] Backend restarted after changes
- [ ] Chat endpoint tested successfully
- [ ] No authentication errors in logs

---

## 🆘 Still Having Issues?

1. **Check the logs**: `python main.py` shows detailed errors
2. **Verify .env file**: `cat backend/.env | grep OPENROUTER`
3. **Test OpenRouter directly**:
   ```bash
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer sk-or-xxxxx"
   ```
4. **Reinstall dependencies**: `pip install -r requirements.txt`
5. **Check OpenRouter status**: https://status.openrouter.ai

---

## 🎯 Key Files Modified

| File | Change |
|------|--------|
| `backend/.env` | Added OpenRouter API key and settings |
| `backend/config.py` | Added OpenRouter configuration class |
| `backend/rag_agent.py` | Updated to use OpenRouter or fallback to OpenAI |
| `backend/agents.py` | Updated UserPersonalizationAgent to use OpenRouter |

---

**Ready to go!** Your chatbot now uses free models from OpenRouter. 🚀
