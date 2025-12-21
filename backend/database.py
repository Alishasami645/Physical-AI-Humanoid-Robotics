import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from config import settings
from typing import List, Dict, Any
import json
import sqlite3
import os


class DatabaseManager:
    """Manages connections and operations with Postgres or SQLite database."""
    
    def __init__(self):
        self.connection_string = settings.database_url
        self.db_type = "sqlite" if self.connection_string.startswith("sqlite://") else "postgres"
        if self.db_type == "sqlite":
            self.db_path = self.connection_string.replace("sqlite:///", "").replace("sqlite://", "")
            os.makedirs(os.path.dirname(self.db_path) if os.path.dirname(self.db_path) else ".", exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        if self.db_type == "sqlite":
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()
        else:
            conn = psycopg2.connect(self.connection_string)
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()
    
    def init_db(self):
        """Initialize database tables. Works with both SQLite and Postgres."""
        try:
            with self.get_connection() as conn:
                if self.db_type == "sqlite":
                    cur = conn.cursor()
                else:
                    cur = conn.cursor()
                
                # Documents table
                if self.db_type == "sqlite":
                    cur.execute("""CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title VARCHAR(255) NOT NULL,
                        chapter VARCHAR(255),
                        content TEXT NOT NULL,
                        source_url VARCHAR(255),
                        embedding_id VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""")
                else:
                    cur.execute("""CREATE TABLE IF NOT EXISTS documents (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        chapter VARCHAR(255),
                        content TEXT NOT NULL,
                        source_url VARCHAR(255),
                        embedding_id VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""")
                
                # Interactions table
                if self.db_type == "sqlite":
                    cur.execute("""CREATE TABLE IF NOT EXISTS interactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_query TEXT NOT NULL,
                        assistant_response TEXT NOT NULL,
                        selected_text TEXT,
                        document_id INTEGER,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""")
                else:
                    cur.execute("""CREATE TABLE IF NOT EXISTS interactions (
                        id SERIAL PRIMARY KEY,
                        user_query TEXT NOT NULL,
                        assistant_response TEXT NOT NULL,
                        selected_text TEXT,
                        document_id INTEGER REFERENCES documents(id),
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""")
                
                # Users table
                if self.db_type == "sqlite":
                    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        external_id VARCHAR(255) UNIQUE,
                        email VARCHAR(255) UNIQUE,
                        points INTEGER DEFAULT 0,
                        software_background VARCHAR(50),
                        hardware_experience VARCHAR(50),
                        programming_languages TEXT,
                        learning_goal TEXT,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""")
                else:
                    cur.execute("""CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        external_id VARCHAR(255) UNIQUE,
                        email VARCHAR(255) UNIQUE,
                        points INTEGER DEFAULT 0,
                        software_background VARCHAR(50),
                        hardware_experience VARCHAR(50),
                        programming_languages JSONB,
                        learning_goal TEXT,
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""")
                
                # Indexes
                try:
                    cur.execute("CREATE INDEX IF NOT EXISTS idx_documents_chapter ON documents(chapter)")
                except:
                    pass
                try:
                    cur.execute("CREATE INDEX IF NOT EXISTS idx_interactions_created ON interactions(created_at DESC)")
                except:
                    pass

                # Bonus awards table to track per-user per-chapter awards
                if self.db_type == "sqlite":
                    cur.execute("""CREATE TABLE IF NOT EXISTS bonus_awards (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        external_id VARCHAR(255),
                        chapter VARCHAR(255),
                        points INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(external_id, chapter)
                    )""")
                else:
                    cur.execute("""CREATE TABLE IF NOT EXISTS bonus_awards (
                        id SERIAL PRIMARY KEY,
                        external_id VARCHAR(255),
                        chapter VARCHAR(255),
                        points INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(external_id, chapter)
                    )""")
                
                if self.db_type == "sqlite":
                    conn.commit()
        except Exception as e:
            print(f"Database initialization skipped: {str(e)}")
    
    def save_document(self, title: str, chapter: str, content: str, 
                     source_url: str, embedding_id: str) -> int:
        """Save document to database."""
        with self.get_connection() as conn:
            cur = conn.cursor()
            if self.db_type == "sqlite":
                cur.execute("""
                    INSERT INTO documents (title, chapter, content, source_url, embedding_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (title, chapter, content, source_url, embedding_id))
                conn.commit()
                return cur.lastrowid
            else:
                cur.execute("""
                    INSERT INTO documents (title, chapter, content, source_url, embedding_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (title, chapter, content, source_url, embedding_id))
                return cur.fetchone()[0]
    
    def save_interaction(self, user_query: str, assistant_response: str,
                        selected_text: str = None, document_id: int = None,
                        metadata: Dict[str, Any] = None) -> int:
        """Save user interaction."""
        with self.get_connection() as conn:
            cur = conn.cursor()
            meta_str = json.dumps(metadata) if metadata else None
            if self.db_type == "sqlite":
                cur.execute("""
                    INSERT INTO interactions 
                    (user_query, assistant_response, selected_text, document_id, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_query, assistant_response, selected_text, document_id, meta_str))
                conn.commit()
                return cur.lastrowid
            else:
                cur.execute("""
                    INSERT INTO interactions 
                    (user_query, assistant_response, selected_text, document_id, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (user_query, assistant_response, selected_text, document_id, meta_str))
                return cur.fetchone()[0]

    def create_user(self, external_id: str = None, email: str = None,
                    software_background: str = None, hardware_experience: str = None,
                    programming_languages: List[str] = None, learning_goal: str = None,
                    metadata: Dict[str, Any] = None) -> int:
        """Create a user and return the user id."""
        with self.get_connection() as conn:
            cur = conn.cursor()
            langs_str = json.dumps(programming_languages) if programming_languages else None
            meta_str = json.dumps(metadata) if metadata else None
            if self.db_type == "sqlite":
                cur.execute("""
                    INSERT INTO users (external_id, email, software_background, hardware_experience, programming_languages, learning_goal, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (external_id, email, software_background, hardware_experience, langs_str, learning_goal, meta_str))
                conn.commit()
                return cur.lastrowid
            else:
                cur.execute("""
                    INSERT INTO users (external_id, email, software_background, hardware_experience, programming_languages, learning_goal, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (external_id, email, software_background, hardware_experience, langs_str, learning_goal, meta_str))
                return cur.fetchone()[0]

    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cur = conn.cursor()
            if self.db_type == "sqlite":
                cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
                row = cur.fetchone()
                return dict(row) if row else None
            else:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                return cur.fetchone()

    def get_user_by_external_id(self, external_id: str) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cur = conn.cursor()
            if self.db_type == "sqlite":
                cur.execute("SELECT * FROM users WHERE external_id = ?", (external_id,))
                row = cur.fetchone()
                return dict(row) if row else None
            else:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                cur.execute("SELECT * FROM users WHERE external_id = %s", (external_id,))
                return cur.fetchone()

    def update_user_profile(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update user profile fields provided in updates dict."""
        allowed = {"software_background", "hardware_experience", "programming_languages", "learning_goal", "metadata", "email"}
        set_parts = []
        values = []
        for k, v in updates.items():
            if k not in allowed:
                continue
            if k == "programming_languages" or k == "metadata":
                set_parts.append(f"{k} = ?") if self.db_type == "sqlite" else set_parts.append(f"{k} = %s")
                values.append(json.dumps(v) if v is not None else None)
            else:
                set_parts.append(f"{k} = ?") if self.db_type == "sqlite" else set_parts.append(f"{k} = %s")
                values.append(v)

        if not set_parts:
            return False

        values.append(user_id)
        with self.get_connection() as conn:
            cur = conn.cursor()
            if self.db_type == "sqlite":
                placeholders = ", ".join(set_parts) + ", updated_at = CURRENT_TIMESTAMP WHERE id = ?"
                cur.execute(f"UPDATE users SET {placeholders}", tuple(values))
                conn.commit()
                return cur.rowcount > 0
            else:
                placeholders = ", ".join(set_parts) + ", updated_at = CURRENT_TIMESTAMP WHERE id = %s"
                cur.execute(f"UPDATE users SET {placeholders}", tuple(values))
                return cur.rowcount > 0
    
    def get_documents_by_chapter(self, chapter: str) -> List[Dict]:
        """Retrieve documents by chapter."""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM documents WHERE chapter = %s
                    ORDER BY created_at DESC
                """, (chapter,))
                return cur.fetchall()
    
    def get_interaction_history(self, limit: int = 50) -> List[Dict]:
        """Retrieve recent interactions."""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM interactions
                    ORDER BY created_at DESC
                    LIMIT %s
                """, (limit,))
                return cur.fetchall()

    def get_all_users(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.cursor()
            if self.db_type == "sqlite":
                cur.execute("SELECT * FROM users")
                rows = cur.fetchall()
                return [dict(r) for r in rows]
            else:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                cur.execute("SELECT * FROM users")
                return cur.fetchall()

    def has_awarded_bonus(self, external_id: str, chapter: str) -> bool:
        with self.get_connection() as conn:
            cur = conn.cursor()
            if self.db_type == "sqlite":
                cur.execute("SELECT id FROM bonus_awards WHERE external_id = ? AND chapter = ?", (external_id, chapter))
                row = cur.fetchone()
                return bool(row)
            else:
                cur = conn.cursor()
                cur.execute("SELECT id FROM bonus_awards WHERE external_id = %s AND chapter = %s", (external_id, chapter))
                row = cur.fetchone()
                return bool(row)

    def award_bonus(self, external_id: str, chapter: str, points: int) -> int:
        """Award bonus points to a user for a chapter. Returns awarded points (0 if already awarded or cap reached)."""
        MAX_POINTS = 50
        with self.get_connection() as conn:
            cur = conn.cursor()

            # Check existing award for this chapter
            if self.db_type == "sqlite":
                cur.execute("SELECT id FROM bonus_awards WHERE external_id = ? AND chapter = ?", (external_id, chapter))
                if cur.fetchone():
                    return 0
            else:
                cur.execute("SELECT id FROM bonus_awards WHERE external_id = %s AND chapter = %s", (external_id, chapter))
                if cur.fetchone():
                    return 0

            # Compute remaining points available for this user
            current = self.get_user_points(external_id)
            remaining = MAX_POINTS - current
            if remaining <= 0:
                return 0

            award_amount = points if points <= remaining else remaining

            # Insert award and update user's total points
            if self.db_type == "sqlite":
                cur.execute("INSERT INTO bonus_awards (external_id, chapter, points) VALUES (?, ?, ?)", (external_id, chapter, award_amount))
                cur.execute("UPDATE users SET points = COALESCE(points,0) + ?, updated_at = CURRENT_TIMESTAMP WHERE external_id = ?", (award_amount, external_id))
                conn.commit()
                return award_amount
            else:
                cur.execute("INSERT INTO bonus_awards (external_id, chapter, points) VALUES (%s, %s, %s)", (external_id, chapter, award_amount))
                cur.execute("UPDATE users SET points = COALESCE(points,0) + %s, updated_at = CURRENT_TIMESTAMP WHERE external_id = %s", (award_amount, external_id))
                return award_amount

    def get_user_points(self, external_id: str) -> int:
        with self.get_connection() as conn:
            cur = conn.cursor()
            if self.db_type == "sqlite":
                cur.execute("SELECT points FROM users WHERE external_id = ?", (external_id,))
                row = cur.fetchone()
                return int(row[0]) if row and row[0] is not None else 0
            else:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                cur.execute("SELECT points FROM users WHERE external_id = %s", (external_id,))
                row = cur.fetchone()
                return int(row["points"]) if row and row.get("points") is not None else 0


# Global database manager instance
db_manager = DatabaseManager()
