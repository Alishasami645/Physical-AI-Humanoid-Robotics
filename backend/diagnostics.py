"""
Health check and diagnostics script.
Run this to verify all components are working correctly.
"""

import sys
from pathlib import Path
import json

def check_imports():
    """Check if all required modules can be imported"""
    print("Checking imports...")
    modules = {
        'fastapi': 'FastAPI',
        'psycopg2': 'Postgres driver',
        'qdrant_client': 'Qdrant client',
        'openai': 'OpenAI SDK',
        'dotenv': 'Environment variables',
    }
    
    failed = []
    for module, description in modules.items():
        try:
            __import__(module)
            print(f"  ✅ {description} ({module})")
        except ImportError:
            print(f"  ❌ {description} ({module})")
            failed.append(module)
    
    return len(failed) == 0

def check_env_file():
    """Check if .env file exists and has required keys"""
    print("\nChecking environment variables...")
    
    env_path = Path('.env')
    if not env_path.exists():
        print("  ❌ .env file not found")
        return False
    
    required_keys = [
        'OPENAI_API_KEY',
        'DATABASE_URL',
        'QDRANT_URL',
        'QDRANT_API_KEY',
    ]
    
    with open(env_path) as f:
        env_content = f.read()
    
    missing = []
    for key in required_keys:
        if key in env_content:
            # Check if it has a value (not just the key)
            for line in env_content.split('\n'):
                if line.startswith(f'{key}=') and '=' in line:
                    value = line.split('=', 1)[1].strip()
                    if value and not value.startswith('your_'):
                        print(f"  ✅ {key}")
                        break
            else:
                print(f"  ⚠️  {key} (not configured)")
                missing.append(key)
        else:
            print(f"  ❌ {key} (not found)")
            missing.append(key)
    
    return len(missing) == 0

def check_openai_connection():
    """Test OpenAI API connection"""
    print("\nChecking OpenAI connection...")
    try:
        from config import settings
        from openai import OpenAI
        
        if not settings.openai_api_key or settings.openai_api_key.startswith('your_'):
            print("  ⚠️  OpenAI API key not configured")
            return False
        
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(
            input="test",
            model=settings.embedding_model
        )
        print(f"  ✅ OpenAI connection successful")
        return True
    except Exception as e:
        print(f"  ❌ OpenAI connection failed: {e}")
        return False

def check_database_connection():
    """Test database connection"""
    print("\nChecking database connection...")
    try:
        from config import settings
        import psycopg2
        
        if not settings.database_url or settings.database_url.startswith('postgresql://user'):
            print("  ⚠️  Database URL not configured")
            return False
        
        conn = psycopg2.connect(settings.database_url)
        conn.close()
        print(f"  ✅ Database connection successful")
        return True
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        return False

def check_qdrant_connection():
    """Test Qdrant connection"""
    print("\nChecking Qdrant connection...")
    try:
        from config import settings
        from qdrant_client import QdrantClient
        
        if not settings.qdrant_url or settings.qdrant_url.startswith('https://your'):
            print("  ⚠️  Qdrant URL not configured")
            return False
        
        client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        collections = client.get_collections()
        print(f"  ✅ Qdrant connection successful")
        print(f"     Collections: {len(collections.collections)}")
        return True
    except Exception as e:
        print(f"  ❌ Qdrant connection failed: {e}")
        return False

def check_tables():
    """Check if database tables exist"""
    print("\nChecking database tables...")
    try:
        from database import db_manager
        
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                # Check for documents table
                cur.execute("""
                    SELECT EXISTS(
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'documents'
                    )
                """)
                has_docs = cur.fetchone()[0]
                
                # Check for interactions table
                cur.execute("""
                    SELECT EXISTS(
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'interactions'
                    )
                """)
                has_interactions = cur.fetchone()[0]
        
        if has_docs:
            print("  ✅ documents table exists")
        else:
            print("  ❌ documents table not found")
        
        if has_interactions:
            print("  ✅ interactions table exists")
        else:
            print("  ❌ interactions table not found")
        
        return has_docs and has_interactions
    except Exception as e:
        print(f"  ❌ Table check failed: {e}")
        return False

def check_documents():
    """Check if documents are indexed"""
    print("\nChecking indexed documents...")
    try:
        from database import db_manager
        
        with db_manager.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM documents")
                count = cur.fetchone()[0]
        
        if count > 0:
            print(f"  ✅ {count} documents indexed")
            return True
        else:
            print("  ⚠️  No documents indexed yet")
            print("     Run: python -c \"from document_indexer import index_robotics_book; index_robotics_book()\"")
            return False
    except Exception as e:
        print(f"  ❌ Document check failed: {e}")
        return False

def main():
    """Run all diagnostics"""
    print("\n" + "="*60)
    print("Robotics Book RAG Chatbot - Diagnostics")
    print("="*60 + "\n")
    
    results = []
    
    # Check imports
    results.append(("Imports", check_imports()))
    
    # Check environment
    results.append(("Environment", check_env_file()))
    
    # Check connections
    results.append(("OpenAI", check_openai_connection()))
    results.append(("Database", check_database_connection()))
    results.append(("Qdrant", check_qdrant_connection()))
    
    # Check database state
    results.append(("Tables", check_tables()))
    results.append(("Documents", check_documents()))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name:20s}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n✅ All checks passed! Ready to start the server.")
        print("   Run: python -m uvicorn main:app --reload")
    else:
        print("\n⚠️  Some checks failed. Review configuration and dependencies.")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
