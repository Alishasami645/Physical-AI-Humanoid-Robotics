from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app FIRST (lightweight)
app = FastAPI(
    title="Robotics Book RAG Chatbot",
    description="Retrieval-Augmented Generation Chatbot for Physical AI & Humanoid Robotics Book",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to load heavy modules in background
FULL_FEATURES = False
try:
    from config import settings
    from rag_agent import rag_agent
    from database import db_manager
    from document_indexer import index_robotics_book
    from agents import user_personalization_agent, chapter_context_agent, translation_agent
    from better_auth import auth_manager, SignUpRequest, AuthResponse
    FULL_FEATURES = True
    logger.info("✅ All modules loaded successfully")
except Exception as e:
    logger.error(f"❌ Error loading modules: {e}")
    # Create stubs for missing modules
    class settings:
        cors_origins = ["*"]
    rag_agent = None
    db_manager = None
    auth_manager = None
    SignUpRequest = None
    AuthResponse = None


# Pydantic models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str
    selected_text: Optional[str] = None
    conversation_history: Optional[List[Dict[str, str]]] = None
    external_id: Optional[str] = None  # User ID for personalization


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str
    sources: List[Dict[str, Any]]
    query: str
    selected_text: Optional[str] = None


class IndexingStatusResponse(BaseModel):
    """Response model for indexing status."""
    status: str
    message: str
    stats: Optional[Dict[str, Any]] = None


# Auth models
class SignupRequest(BaseModel):
    external_id: Optional[str] = None
    email: Optional[str] = None
    software_background: str = Field(..., description="Beginner / Intermediate / Advanced")
    hardware_experience: str = Field(..., description="Low / Medium / High")
    programming_languages: List[str] = Field(default_factory=list)
    learning_goal: Optional[str] = None


class SigninRequest(BaseModel):
    external_id: Optional[str] = None
    email: Optional[str] = None


# Personalization and translation models
class PersonalizeRequest(BaseModel):
    external_id: Optional[str] = None
    profile: Dict[str, Any]


class TranslateRequest(BaseModel):
    content: str
    target: str = "ur"


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Robotics Book RAG Chatbot",
        "version": "1.0.0"
    }


# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process user query and return AI-generated response.
    
    Supports:
    - Regular questions about book content
    - Questions about selected text
    - Multi-turn conversations
    - Personalized responses (with external_id for logged-in users)
    """
    if not FULL_FEATURES:
        raise HTTPException(
            status_code=503,
            detail="Backend modules failed to load. Please check configuration and restart."
        )
    
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Fetch user profile if external_id provided
        user_profile = None
        if request.external_id:
            user = db_manager.get_user_by_external_id(request.external_id)
            if user:
                user_profile = {
                    "software_background": user.get("software_background"),
                    "hardware_experience": user.get("hardware_experience"),
                    "programming_languages": user.get("programming_languages"),
                    "learning_goal": user.get("learning_goal"),
                }
        
        # Get response from RAG agent with personalization
        result = rag_agent.answer_question(
            query=request.query,
            selected_text=request.selected_text,
            conversation_history=request.conversation_history,
            user_profile=user_profile
        )
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            query=result["query"],
            selected_text=result["selected_text"]
        )
    
    except Exception as e:
        logger.exception("Error processing chat request")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Summarize endpoint
@app.get("/api/summarize/{chapter_name}")
async def summarize_chapter(chapter_name: str):
    """Generate summary for a specific chapter."""
    try:
        summary = rag_agent.summarize_chapter(chapter_name)
        return {
            "chapter": chapter_name,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Index management endpoints
@app.post("/api/admin/index", response_model=IndexingStatusResponse)
async def start_indexing(background_tasks: BackgroundTasks):
    """Start indexing all documents (background task)."""
    try:
        background_tasks.add_task(index_robotics_book)
        return IndexingStatusResponse(
            status="started",
            message="Document indexing has been started in the background"
        )
    except Exception as e:
        logger.error(f"Error starting indexing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Signup endpoint - accepts profile questions and persists them
@app.post("/api/auth/signup")
async def signup(req: SignupRequest):
    try:
        # Save or update profile using external_id if provided
        profile = {
            "email": req.email,
            "software_background": req.software_background,
            "hardware_experience": req.hardware_experience,
            "programming_languages": req.programming_languages,
            "learning_goal": req.learning_goal,
        }

        user = user_personalization_agent.save_profile(req.external_id, profile)
        return {"status": "ok", "user": user}
    except Exception as e:
        logger.exception("Signup failed")
        raise HTTPException(status_code=500, detail=str(e))


# Signin endpoint - lightweight: returns user profile by external id or email
@app.post("/api/auth/signin")
async def signin(req: SigninRequest):
    try:
        user = None
        if req.external_id:
            user = db_manager.get_user_by_external_id(req.external_id)
        if not user and req.email:
            # lookup by email
            with db_manager.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM users WHERE email = %s", (req.email,))
                    row = cur.fetchone()
                    if row:
                        user = row

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"status": "ok", "user": user}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Signin failed")
        raise HTTPException(status_code=500, detail=str(e))


# Personalization endpoint - applies and returns personalized prompt or summary
@app.post("/api/agents/personalize")
async def personalize(req: PersonalizeRequest):
    try:
        user = None
        if req.external_id:
            user = db_manager.get_user_by_external_id(req.external_id)

        saved = user_personalization_agent.save_profile(req.external_id, req.profile)
        return {"status": "ok", "user": saved}
    except Exception as e:
        logger.exception("Personalization failed")
        raise HTTPException(status_code=500, detail=str(e))


# Chapter context endpoint
@app.get("/api/agents/chapter_context/{chapter_name}")
async def chapter_context(chapter_name: str):
    try:
        ctx = chapter_context_agent.get_chapter_context(chapter_name)
        return {"status": "ok", "context": ctx}
    except Exception as e:
        logger.exception("Chapter context failed")
        raise HTTPException(status_code=500, detail=str(e))


# Translation endpoint
@app.post("/api/agents/translate")
async def translate(req: TranslateRequest):
    try:
        if req.target.lower() not in ("ur", "urdu"):
            raise HTTPException(status_code=400, detail="Unsupported target language")

        translated = translation_agent.translate_to_urdu(req.content)
        return {"status": "ok", "translated": translated}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Translation failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/index/sync", response_model=IndexingStatusResponse)
async def sync_indexing():
    """Synchronously index all documents."""
    try:
        stats = index_robotics_book()
        return IndexingStatusResponse(
            status="completed",
            message="Document indexing completed successfully",
            stats=stats
        )
    except Exception as e:
        logger.error(f"Error during indexing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    try:
        logger.info("Initializing database...")
        db_manager.init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API documentation."""
    return {
        "service": "Robotics Book RAG Chatbot API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "chat": "/api/chat (POST)",
            "summarize": "/api/summarize (POST)",
            "index": "/api/index (GET)",
        }
    }


# Personalization Models
class UserProfile(BaseModel):
    """User profile for personalization."""
    external_id: Optional[str] = None
    email: Optional[str] = None
    software_background: str = "beginner"  # beginner, intermediate, advanced
    hardware_experience: str = "low"  # low, medium, high
    programming_languages: List[str] = []
    learning_goal: str = ""
    metadata: Optional[Dict[str, Any]] = None


class PersonalizeChapterRequest(BaseModel):
    """Request to personalize a chapter."""
    chapter_name: str
    chapter_content: str
    user_profile: UserProfile


class PersonalizeChapterResponse(BaseModel):
    """Personalized chapter content."""
    chapter_name: str
    original_length: int
    personalized_length: int
    personalized_content: str


# Translation Models
class TranslateRequest(BaseModel):
    """Request to translate content to Urdu."""
    content: str
    preserve_code_blocks: bool = True


class TranslateResponse(BaseModel):
    """Translated content."""
    original_length: int
    urdu_length: int
    urdu_content: str


class TranslateSectionRequest(BaseModel):
    """Request to translate a section."""
    title: str
    content: str


class TranslateSectionResponse(BaseModel):
    """Translated section with title."""
    title_en: str
    title_urdu: str
    content_urdu: str


class BonusAwardRequest(BaseModel):
    external_id: str
    chapter: str
    points: int = 50


@app.post("/api/users/award-bonus")
async def award_bonus(req: BonusAwardRequest):
    """Award bonus points to a user for translating a chapter to Urdu.

    Prevents double-award for the same user and chapter.
    """
    try:
        if not req.external_id or not req.chapter:
            raise HTTPException(status_code=400, detail="external_id and chapter are required")

        # Limit points per award to 50
        pts = int(req.points)
        if pts <= 0 or pts > 50:
            raise HTTPException(status_code=400, detail="points must be between 1 and 50")

        # Ensure user exists
        user = db_manager.get_user_by_external_id(req.external_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check current total and enforce participant cap
        total_before = db_manager.get_user_points(req.external_id)
        if total_before >= 50:
            return {"status": "ok", "awarded": False, "detail": "User has already reached maximum bonus points", "total_points": total_before}

        awarded = db_manager.award_bonus(req.external_id, req.chapter, pts)
        total_after = db_manager.get_user_points(req.external_id)

        if awarded == 0:
            # Could be duplicate chapter award or cap reached concurrently
            return {"status": "ok", "awarded": False, "detail": "No points awarded (already claimed or cap reached)", "total_points": total_after}

        return {"status": "ok", "awarded": True, "awarded_points": awarded, "total_points": total_after}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error awarding bonus")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/users/{external_id}/award-status/{chapter}")
async def award_status(external_id: str, chapter: str):
    """Return whether the user has been awarded for this chapter and their total points."""
    try:
        user = db_manager.get_user_by_external_id(external_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        awarded = db_manager.has_awarded_bonus(external_id, chapter)
        total = db_manager.get_user_points(external_id)
        remaining = max(0, 50 - total)
        return {"status": "ok", "awarded": bool(awarded), "total_points": total, "remaining": remaining}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error getting award status")
        raise HTTPException(status_code=500, detail=str(e))


# Personalization Endpoints

@app.post("/api/personalize/profile", response_model=Dict[str, Any])
async def save_user_profile(profile: UserProfile):
    """Save or update user profile for personalization."""
    try:
        saved = user_personalization_agent.save_profile(
            external_id=profile.external_id,
            profile=profile.dict()
        )
        return {
            "status": "success",
            "user_id": saved.get("id") if saved else None,
            "profile": saved
        }
    except Exception as e:
        logger.exception("Error saving user profile")
        raise HTTPException(status_code=500, detail=f"Failed to save profile: {str(e)}")


@app.post("/api/personalize/chapter", response_model=PersonalizeChapterResponse)
async def personalize_chapter(request: PersonalizeChapterRequest):
    """Personalize a chapter based on user profile."""
    try:
        personalized = user_personalization_agent.personalize_chapter(
            chapter_content=request.chapter_content,
            user_profile=request.user_profile.dict()
        )
        
        return PersonalizeChapterResponse(
            chapter_name=request.chapter_name,
            original_length=len(request.chapter_content),
            personalized_length=len(personalized),
            personalized_content=personalized
        )
    except Exception as e:
        logger.exception("Error personalizing chapter")
        raise HTTPException(status_code=500, detail=f"Failed to personalize: {str(e)}")


@app.get("/api/chapters/{chapter_name}/context")
async def get_chapter_context(chapter_name: str):
    """Get chapter context including summary, concepts, and learning outcomes."""
    try:
        context = chapter_context_agent.get_chapter_context(chapter_name)
        return {
            "status": "success",
            "context": context
        }
    except Exception as e:
        logger.exception("Error getting chapter context")
        raise HTTPException(status_code=500, detail=f"Failed to get context: {str(e)}")


# Translation Endpoints

@app.post("/api/translate/urdu", response_model=TranslateResponse)
async def translate_to_urdu(request: TranslateRequest):
    """Translate content to Urdu while preserving code blocks."""
    try:
        logger.info(f"Translate request received. Content length: {len(request.content)}")
        print(f"[API] /api/translate/urdu called with content length: {len(request.content)}")
        
        urdu_content = translation_agent.translate_to_urdu(request.content)
        logger.info(f"Translation successful. Output length: {len(urdu_content)}")
        print(f"[API] Translation completed. Output length: {len(urdu_content)}")
        
        return TranslateResponse(
            original_length=len(request.content),
            urdu_length=len(urdu_content),
            urdu_content=urdu_content
        )
    except Exception as e:
        logger.exception("Error translating to Urdu")
        print(f"[API] Translation error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint to verify API is working."""
    return {"status": "ok", "message": "API is working"}


@app.post("/api/translate/section", response_model=TranslateSectionResponse)
async def translate_section(request: TranslateSectionRequest):
    """Translate a single section with title."""
    try:
        result = translation_agent.translate_section(
            title=request.title,
            content=request.content
        )
        
        return TranslateSectionResponse(
            title_en=result["title_en"],
            title_urdu=result["title_urdu"],
            content_urdu=result["content_urdu"]
        )
    except Exception as e:
        logger.exception("Error translating section")
        raise HTTPException(status_code=500, detail=f"Section translation failed: {str(e)}")


# Root endpoint with updated docs
@app.get("/")
async def root():
    """Root endpoint with API documentation."""
    return {
        "service": "Robotics Book RAG Chatbot API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "chat": "/api/chat (POST)",
            "summarize": "/api/summarize/{chapter_name}",
            "indexing": "/api/admin/index (POST) or /api/admin/index/sync (GET)",
            "personalization": {
                "save_profile": "/api/personalize/profile (POST)",
                "personalize_chapter": "/api/personalize/chapter (POST)",
                "get_context": "/api/chapters/{chapter_name}/context (GET)"
            },
            "translation": {
                "translate_content": "/api/translate/urdu (POST)",
                "translate_section": "/api/translate/section (POST)"
            }
        }
    }


# Better Auth endpoints
@app.post("/auth/signup", response_model=AuthResponse)
async def signup(request: SignUpRequest):
    """
    Register a new user with profile information.
    
    Args:
        request: SignUpRequest with email, password, and profile fields
    
    Returns:
        AuthResponse with user info and auth token
    """
    try:
        result = auth_manager.create_user(request)
        return AuthResponse(**result)
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return AuthResponse(success=False, message=f"Signup failed: {str(e)}")


@app.post("/auth/signin", response_model=AuthResponse)
async def signin(request: Dict[str, str]):
    """
    Sign in an existing user.
    
    Args:
        request: {"email": str, "password": str}
    
    Returns:
        AuthResponse with user info and auth token
    """
    try:
        from better_auth import SignInRequest
        signin_req = SignInRequest(**request)
        result = auth_manager.authenticate_user(signin_req)
        return AuthResponse(**result)
    except Exception as e:
        logger.error(f"Signin error: {str(e)}")
        return AuthResponse(success=False, message=f"Signin failed: {str(e)}")


@app.post("/auth/signout")
async def signout():
    """Sign out user (clear client-side tokens)."""
    return {"success": True, "message": "Signed out successfully"}


@app.get("/auth/user/{external_id}")
async def get_user(external_id: str):
    """Get user profile by external_id (Better Auth user ID)."""
    try:
        users = db_manager.get_all_users()
        user = None
        for u in users:
            if u.get("external_id") == external_id:
                user = u
                break
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "success": True,
            "user": {
                "id": user["external_id"],
                "email": user["email"],
                "software_background": user.get("software_background"),
                "hardware_experience": user.get("hardware_experience"),
                "programming_languages": user.get("programming_languages"),
                "learning_goal": user.get("learning_goal"),
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
