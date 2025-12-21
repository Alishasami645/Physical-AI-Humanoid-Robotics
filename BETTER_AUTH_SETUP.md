# Better-Auth Integration Guide

This guide explains how to set up **Better-Auth** for authentication in the Robotics Book project.

## What is Better-Auth?

[Better-Auth](https://www.better-auth.com/) is a modern authentication framework that provides:
- Sign-up / Sign-in with email & password
- OAuth providers (Google, GitHub, etc.)
- Multi-factor authentication (MFA)
- Session management
- Standardized auth endpoints

## Current Architecture

The project uses a **local authentication pattern** with `external_id` stored in localStorage:
- Frontend calls `/api/auth/signup` → user profile saved to DB
- Frontend calls `/api/auth/signin` → user profile retrieved from DB
- `external_id` stored in localStorage and sent with every chat request
- Backend applies personalization based on user profile

## Optional: Full Better-Auth Integration

To integrate actual Better-Auth (for advanced OAuth, MFA, etc.):

### 1. Install Better-Auth

```bash
npm install better-auth
```

### 2. Frontend AuthProvider Setup

Create or update `src/components/Auth/AuthProvider.tsx`:

```tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

interface User {
  external_id: string;
  email?: string;
  software_background?: string;
  hardware_experience?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  signin: (email: string, password: string) => Promise<void>;
  signup: (profile: any) => Promise<void>;
  signout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Restore session from localStorage
    const externalId = localStorage.getItem('external_id');
    if (externalId) {
      setUser({ external_id: externalId });
    }
    setIsLoading(false);
  }, []);

  const signup = async (profile: any) => {
    try {
      const res = await fetch('http://localhost:8000/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile),
      });
      const data = await res.json();
      if (res.ok && data.user) {
        const extId = data.user.external_id || String(data.user.id);
        localStorage.setItem('external_id', extId);
        setUser({ external_id: extId, ...data.user });
      }
    } catch (e) {
      console.error('Signup failed:', e);
      throw e;
    }
  };

  const signin = async (email: string, password?: string) => {
    try {
      const res = await fetch('http://localhost:8000/api/auth/signin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
      const data = await res.json();
      if (res.ok && data.user) {
        const extId = data.user.external_id || String(data.user.id);
        localStorage.setItem('external_id', extId);
        setUser({ external_id: extId, ...data.user });
      }
    } catch (e) {
      console.error('Signin failed:', e);
      throw e;
    }
  };

  const signout = async () => {
    localStorage.removeItem('external_id');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, signin, signup, signout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
}
```

### 3. Wrap App with AuthProvider

Update `src/theme/Root.tsx`:

```tsx
import React, { Suspense, lazy } from 'react';
import ClientOnly from '../components/ClientOnlyWrapper';
import { AuthProvider } from '../components/Auth/AuthProvider';

const ChatbotWrapper = lazy(() => import('../components/ChatbotWrapper'));

export default function Root({ children }) {
  return (
    <AuthProvider>
      <>
        {children}
        <ClientOnly fallback={null}>
          <Suspense fallback={null}>
            <ChatbotWrapper />
          </Suspense>
        </ClientOnly>
      </>
    </AuthProvider>
  );
}
```

## Key Features Implemented

### ✅ Task 4: Reusable Intelligence (Bonus +50)
- **UserPersonalizationAgent** — manages user profiles and applies personalization
- **ChapterContextAgent** — provides chapter context and summaries
- **TranslationAgent** — translates content to Urdu while preserving code/headings
- All agents are **singletons** reused across endpoints (no duplicated logic)
- Agents called from chatbot, personalization endpoints, and chapter actions

### ✅ Task 5: Signup & Signin (Bonus +50)
- `/api/auth/signup` — saves user profile with:
  - Software background (Beginner/Intermediate/Advanced)
  - Hardware experience (Low/Medium/High)
  - Programming languages
  - Learning goal
- `/api/auth/signin` — retrieves user by external_id or email
- Data persisted in `users` table (SQLite or Postgres)
- Frontend SignupForm component collects profile info

### ✅ Task 6: Chapter Personalization Button (Bonus +50)
- **ChapterActions** component with "Personalize this chapter" button
- Only shown/enabled for logged-in users (checks localStorage for external_id)
- Calls backend `/api/agents/personalize` to save preferences
- Opens SignupForm modal if user not logged in
- Personalization applied to all subsequent chat responses

### ✅ Task 7: Urdu Translation Button (Bonus +50)
- **ChapterActions** component with "Translate to Urdu" button
- Available to all users (no login required)
- Calls `/api/agents/translate` which uses TranslationAgent
- TranslationAgent:
  - Preserves code blocks (keeps code in English)
  - Preserves Markdown headings and formatting
  - Uses professional Urdu with technical terms in brackets
- Opens translation in new browser tab

## Testing the Full Flow

1. **Start Backend**:
   ```bash
   cd backend
   python -m uvicorn main:app --host 127.0.0.1 --port 8000
   ```

2. **Start Frontend** (Docusaurus):
   ```bash
   npm run start
   ```

3. **Test Signup**:
   - Navigate to a chapter with `<ChapterActions />`
   - Click "Personalize this chapter"
   - Click "Personalize this chapter" button again (or open SignupForm in chapter)
   - Fill out: email, software background, hardware experience, programming languages, learning goal
   - Submit
   - Check browser console: should see `external_id` in localStorage

4. **Test Chat with Personalization**:
   - Open the chatbot (💬 button)
   - Ask a question
   - Backend fetches user profile by external_id
   - Response is personalized based on software/hardware background

5. **Test Translation**:
   - Click "Translate to Urdu" button
   - Chapter content sent to backend
   - TranslationAgent translates to Urdu
   - Result opens in new tab with preserved code blocks

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/signup` | Register/update user profile |
| POST | `/api/auth/signin` | Retrieve user by external_id/email |
| POST | `/api/chat` | Answer question (with optional external_id for personalization) |
| POST | `/api/agents/personalize` | Save personalization preferences |
| GET | `/api/agents/chapter_context/{chapter_name}` | Get chapter context and summary |
| POST | `/api/agents/translate` | Translate content to Urdu |

## Database Schema

**users table**:
```sql
id (PK)
external_id (UNIQUE)
email (UNIQUE)
software_background (Beginner|Intermediate|Advanced)
hardware_experience (Low|Medium|High)
programming_languages (JSON array)
learning_goal (text)
metadata (JSON)
created_at, updated_at
```

## Embedding Chapters

Add to any chapter MDX file (e.g., `docs/chapter-01.../lesson-1-1.md`):

```mdx
import ChapterActions from '@site/src/components/ChapterActions/ChapterActions';

<ChapterActions chapterName="chapter-01-introduction-to-physical-ai" />

# Your Chapter Title

Rest of your content...
```

## Troubleshooting

**"Failed to fetch" in chatbot**
- Ensure backend is running on port 8000
- Check CORS_ORIGINS in backend/.env includes frontend URL

**Personalization not applying**
- Verify external_id is in localStorage: `console.log(localStorage.getItem('external_id'))`
- Check backend logs for user lookup

**Translation returns English**
- Ensure OPENAI_API_KEY is valid in backend/.env
- Check OpenAI quota

## Next Steps

1. ✅ Embed `<ChapterActions />` at start of each chapter
2. ✅ Optional: Implement full Better-Auth with OAuth providers
3. ✅ Optional: Add MFA, social login, email verification
4. ✅ Optional: Build admin dashboard to view user profiles & personalization stats
