"""Better Auth server-side integration for FastAPI."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pydantic import BaseModel
from database import db_manager


class AuthUser(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    image: Optional[str] = None


class SignUpRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    software_background: str
    hardware_experience: str
    programming_languages: list[str]
    learning_goal: str


class SignInRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    success: bool
    user: Optional[AuthUser] = None
    token: Optional[str] = None
    message: str = ""


class BetterAuthManager:
    """Manages Better Auth integration with FastAPI backend."""

    def __init__(self):
        self.db = db_manager
        self.token_expiry = timedelta(days=7)

    def create_user(self, signup_data: SignUpRequest) -> Dict[str, Any]:
        """Create a new user with profile data."""
        # In production, use bcrypt or similar for password hashing
        import hashlib
        import secrets

        password_hash = hashlib.sha256(signup_data.password.encode()).hexdigest()
        user_id = secrets.token_urlsafe(16)

        # Create user in database with profile
        try:
            db_user_id = self.db.create_user(
                external_id=user_id,
                email=signup_data.email,
                software_background=signup_data.software_background,
                hardware_experience=signup_data.hardware_experience,
                programming_languages=signup_data.programming_languages,
                learning_goal=signup_data.learning_goal,
                metadata={
                    "password_hash": password_hash,
                    "name": signup_data.name or signup_data.email.split("@")[0],
                    "created_at": datetime.utcnow().isoformat(),
                },
            )
            user = self.db.get_user_by_id(db_user_id)
            return {
                "success": True,
                "user": AuthUser(
                    id=user_id,
                    email=user["email"],
                    name=signup_data.name or signup_data.email.split("@")[0],
                ),
                "token": self._generate_token(user_id),
                "message": "User created successfully",
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create user: {str(e)}",
            }

    def authenticate_user(self, signin_data: SignInRequest) -> Dict[str, Any]:
        """Authenticate user and return token."""
        import hashlib

        # Find user by email
        users = self.db.get_all_users()
        user = None
        for u in users:
            if u["email"] == signin_data.email:
                user = u
                break

        if not user:
            return {
                "success": False,
                "message": "User not found",
            }

        # Verify password
        password_hash = hashlib.sha256(signin_data.password.encode()).hexdigest()
        stored_hash = user.get("metadata", {}).get("password_hash")

        if password_hash != stored_hash:
            return {
                "success": False,
                "message": "Invalid password",
            }

        return {
            "success": True,
            "user": AuthUser(
                id=user["external_id"],
                email=user["email"],
                name=user.get("metadata", {}).get("name", user["email"]),
            ),
            "token": self._generate_token(user["external_id"]),
            "message": "Authenticated successfully",
        }

    def _generate_token(self, user_id: str) -> str:
        """Generate a simple JWT-like token."""
        import jwt
        from config import settings

        payload = {
            "sub": user_id,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + self.token_expiry,
        }
        try:
            return jwt.encode(
                payload, settings.secret_key or "dev-secret-key", algorithm="HS256"
            )
        except:
            # Fallback if jwt not available
            import base64

            return base64.b64encode(f"{user_id}:{datetime.utcnow().isoformat()}".encode()).decode()

    def verify_token(self, token: str) -> Optional[str]:
        """Verify token and return user_id."""
        try:
            import jwt
            from config import settings

            payload = jwt.decode(
                token, settings.secret_key or "dev-secret-key", algorithms=["HS256"]
            )
            return payload.get("sub")
        except:
            return None


# Singleton instance
auth_manager = BetterAuthManager()
