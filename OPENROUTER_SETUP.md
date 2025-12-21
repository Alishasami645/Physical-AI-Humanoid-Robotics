# OpenRouter Free Model Setup Guide

This guide explains how to use **free LLM models** from OpenRouter API instead of paid APIs like OpenAI.

## ✅ Why Use OpenRouter?

- **Free tier available** - No credit card required initially
- **Multiple free models** - Llama 2, Mistral, and more
- **OpenAI-compatible API** - Drop-in replacement for existing code
- **Cost-effective** - Perfect for development and testing

## 🔑 Getting Your OpenRouter API Key

### Step 1: Create Account
1. Go to [OpenRouter.ai](https://openrouter.ai)
2. Click **"Sign Up"** (top right)
3. Complete the registration

### Step 2: Get API Key
1. Go to [OpenRouter Settings/Keys](https://openrouter.ai/keys)
2. Click **"Create Key"**
3. Name it (e.g., "Robotics Book")
4. Copy the generated API key

**Keep this key safe! Don't share it publicly.**

## 🚀 Configuration

### Option 1: Using Environment Variables (Recommended)

Update your `.env` file in the `backend/` directory:

```dotenv
# OpenRouter Configuration
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxx
USE_OPENROUTER=true
OPENROUTER_MODEL=meta-llama/llama-2-7b-chat
```

### Option 2: Update .env File
```bash
cd backend
# Edit .env file and add/update:
OPENROUTER_API_KEY=your-api-key-here
```

## 🎯 Available Free Models

| Model | ID | Speed | Quality | Free? |
|-------|----|----|---------|-------|
| **Llama 2 7B** | `meta-llama/llama-2-7b-chat` | Very Fast | Good | ✅ |
| **Mistral 7B** | `mistralai/mistral-7b-instruct` | Very Fast | Good | ✅ |
| **Auto** (Best Available) | `openrouter/auto` | Variable | Best | ✅ |

### Choosing a Model

- **For speed**: Use `meta-llama/llama-2-7b-chat` (fastest)
- **For quality**: Use `openrouter/auto` (OpenRouter picks best free model)
- **Balanced**: Use `mistralai/mistral-7b-instruct`

Update `OPENROUTER_MODEL` in `.env`:

```dotenv
OPENROUTER_MODEL=openrouter/auto
```

## 🔄 How It Works

The application automatically switches between OpenRouter and OpenAI:

```
┌─ Check: Is USE_OPENROUTER=true AND api_key exists?
│
├─→ YES: Use OpenRouter (FREE)
│        - API Base: https://openrouter.ai/api/v1
│        - Model: From OPENROUTER_MODEL setting
│
└─→ NO: Fallback to OpenAI (requires OPENAI_API_KEY)
```

## 🧪 Testing the Setup

### Test 1: Environment Variables
```bash
cd backend
python -c "from config import settings; print(f'Using: {settings.model}')"
```

Expected output (if OpenRouter):
```
Using: meta-llama/llama-2-7b-chat
```

### Test 2: Start Backend
```bash
cd backend
python main.py
```

Should start without API errors.

### Test 3: Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is ROS 2?"
  }'
```

## ⚠️ Common Issues & Solutions

### Issue 1: "Invalid API Key"
**Cause**: OpenRouter API key not set or incorrect format

**Solution**:
```bash
# Verify key in .env
grep OPENROUTER_API_KEY backend/.env

# Should show: OPENROUTER_API_KEY=sk-or-xxxxxx
```

### Issue 2: "Model not found"
**Cause**: Model name is incorrect

**Solution**:
```dotenv
# Use a standard model:
OPENROUTER_MODEL=meta-llama/llama-2-7b-chat
```

### Issue 3: Slow Responses
**Cause**: Using a slower model

**Solution**:
```dotenv
# Switch to faster model:
OPENROUTER_MODEL=meta-llama/llama-2-7b-chat
```

### Issue 4: "USE_OPENROUTER not recognized"
**Cause**: Changes not reloaded

**Solution**:
```bash
# Restart backend
python main.py

# Or check if fallback to OpenAI is happening:
python -c "from config import settings; print(settings.use_openrouter)"
```

## 📊 Free Tier Limits

- **No credit card required** for initial free tier
- **Generous rate limits** for free models
- **Unlimited requests** on some models
- **Check dashboard** at [OpenRouter.ai](https://openrouter.ai) for usage

## 🔄 Switching Back to OpenAI

If you want to use OpenAI again:

```dotenv
USE_OPENROUTER=false
OPENAI_API_KEY=sk-xxxxxxxxxx
```

## 📚 More Information

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Available Models](https://openrouter.ai/models)
- [API Reference](https://openrouter.ai/docs/api/v1)

## ✨ Next Steps

1. ✅ Get OpenRouter API key
2. ✅ Update `.env` file  
3. ✅ Restart backend
4. ✅ Test with `/api/chat` endpoint
5. ✅ Enjoy free LLM powered chatbot!

---

**Questions?** Check the [OpenRouter Discord Community](https://discord.gg/openrouter)
