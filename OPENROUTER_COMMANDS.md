# OpenRouter Setup - Commands to Copy & Paste

## 🚀 5-Minute Setup

### Step 1: Get Your Free API Key (2 min)

**Skip to Step 2 if you already have a key starting with `sk-or-`**

Open in your browser:
```
https://openrouter.ai
```

Then:
1. Click **"Sign Up"** (top right)
2. Enter email + password
3. Click **Settings** → **API Keys**
4. Click **"Create Key"**
5. Copy the key (it looks like: `sk-or-xxxxxxxxxxxxxxxx`)

---

### Step 2: Edit Your .env File (1 min)

**Location:** `backend/.env`

Replace the OpenAI section with:
```dotenv
# OpenRouter Configuration (for free models)
OPENROUTER_API_KEY=sk-or-PASTE-YOUR-KEY-HERE
USE_OPENROUTER=true
OPENROUTER_MODEL=meta-llama/llama-2-7b-chat

# (The rest of the .env stays the same)
```

**Example with real key:**
```dotenv
OPENROUTER_API_KEY=sk-or-abc123def456ghi789
USE_OPENROUTER=true
OPENROUTER_MODEL=meta-llama/llama-2-7b-chat
```

---

### Step 3: Verify Configuration (1 min)

Open PowerShell and run:
```powershell
cd e:\Quarter-4\Q4\Hackathons\robotics-book\backend
python -c "from config import settings; print(f'Using: {settings.openrouter_model}'); print(f'OpenRouter: {settings.use_openrouter}')"
```

**You should see:**
```
Using: meta-llama/llama-2-7b-chat
OpenRouter: True
```

---

### Step 4: Start the Backend (1 min)

```powershell
cd e:\Quarter-4\Q4\Hackathons\robotics-book\backend
python main.py
```

**Look for:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

### Step 5: Test It Works (30 sec)

**Open a NEW PowerShell window** and run:
```powershell
curl -X POST http://localhost:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{"query": "What is robotics?"}'
```

Or **test in browser** by visiting:
```
http://localhost:8000/docs
```

Then click on `/api/chat` and click **Try it out**.

---

## 🎯 Complete Commands (Copy & Paste)

### On Windows PowerShell:

```powershell
# 1. Navigate to backend
cd e:\Quarter-4\Q4\Hackathons\robotics-book\backend

# 2. Verify key was added
(Get-Content .env) | Select-String "OPENROUTER"

# 3. Start backend
python main.py
```

### In Another PowerShell Window:

```powershell
# 4. Test the API
curl -X POST http://localhost:8000/api/chat `
  -H "Content-Type: application/json" `
  -d '{"query": "Hello!"}'
```

---

## 🔧 Common Commands

### Switch to Different Free Model

**Option A: Llama 2 (fastest)**
```powershell
# Edit backend/.env and change:
# OPENROUTER_MODEL=meta-llama/llama-2-7b-chat
```

**Option B: Mistral 7B (good alternative)**
```powershell
# Edit backend/.env and change:
# OPENROUTER_MODEL=mistralai/mistral-7b-instruct
```

**Option C: Auto (OpenRouter picks best)**
```powershell
# Edit backend/.env and change:
# OPENROUTER_MODEL=openrouter/auto
```

Then restart the backend.

---

### Verify Your API Key Works

```powershell
# If you have curl installed:
curl "https://openrouter.ai/api/v1/models" `
  -H "Authorization: Bearer sk-or-YOUR-KEY-HERE"
```

You should get a list of available models.

---

### Disable OpenRouter (Use OpenAI instead)

```powershell
# Edit backend/.env and change:
# USE_OPENROUTER=false
# OPENAI_API_KEY=sk-xxxxxxxxxx (your OpenAI key)
```

Then restart backend.

---

### Check What's Being Used

```powershell
python -c "from config import settings; print(f'Provider: {\"OpenRouter\" if settings.use_openrouter else \"OpenAI\"}'); print(f'Model: {settings.openrouter_model if settings.use_openrouter else settings.model_name}')"
```

---

## ❌ Troubleshooting

### Error: "Invalid API Key"

```powershell
# Check if key is in .env
(Get-Content backend/.env) | Select-String "OPENROUTER_API_KEY"

# Should show: OPENROUTER_API_KEY=sk-or-xxxxx

# If missing or wrong, edit backend/.env and add the correct key
```

### Error: "Model not found"

```powershell
# Use a known working model
# Edit backend/.env and use:
# OPENROUTER_MODEL=meta-llama/llama-2-7b-chat
```

### Error: "Connection refused"

```powershell
# Make sure backend is running
# Run: python main.py
# And test in a DIFFERENT PowerShell window
```

### Can't find backend/.env file

```powershell
# Check current directory
cd e:\Quarter-4\Q4\Hackathons\robotics-book\backend
ls -la .env
```

Should list the `.env` file.

---

## 📝 Commands by Scenario

### Scenario 1: First Time Setup
```powershell
# 1. Copy default config
Copy-Item backend\.env.example backend\.env

# 2. Edit .env with your key
notepad backend\.env

# 3. Start backend
cd backend
python main.py
```

### Scenario 2: Test Multiple Models
```powershell
cd backend

# Test Llama
(Get-Content .env) -replace 'OPENROUTER_MODEL=.*', 'OPENROUTER_MODEL=meta-llama/llama-2-7b-chat' | Set-Content .env
python main.py

# (in another window) curl test
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d '{"query":"test"}'
```

### Scenario 3: Migrate from OpenAI to OpenRouter
```powershell
cd backend

# Update .env
$env_content = Get-Content .env
$env_content = $env_content -replace 'OPENAI_API_KEY=.*', ''
$env_content = $env_content -replace '^# OpenAI.*', '#USE_OPENROUTER'
$env_content += "`nOPENROUTER_API_KEY=sk-or-your-key"
$env_content += "`nUSE_OPENROUTER=true"
$env_content | Set-Content .env

# Restart
python main.py
```

---

## 🎉 Success Signs

When everything works, you'll see:

✅ Backend starts without errors
✅ Chat endpoint responds quickly
✅ No "authentication" errors in logs
✅ Responses come from free model (may be slightly slower than OpenAI, but free!)

---

## 📞 Need Help?

1. **Check this file:** Commands to copy & paste
2. **Read:** `OPENROUTER_SETUP.md` - Full setup guide
3. **Look up:** `OPENROUTER_QUICK_FIX.md` - Common errors
4. **Understand:** `OPENROUTER_CHANGES.md` - Technical details

---

**You're all set!** 🚀 Your chatbot now uses free LLM models from OpenRouter.
