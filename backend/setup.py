#!/usr/bin/env python3
"""
Setup script for the Robotics Book RAG Chatbot backend.
This script initializes all necessary components.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import psycopg2
        import qdrant_client
        import openai
        import fastapi
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def create_env_file():
    """Create .env file from example"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ .env.example not found")
        return False
    
    with open(env_example) as f:
        content = f.read()
    
    with open(env_file, "w") as f:
        f.write(content)
    
    print("✅ Created .env file (update with your API keys)")
    return True

def setup_database():
    """Initialize database"""
    try:
        from database import db_manager
        print("🔄 Initializing database...")
        db_manager.init_db()
        print("✅ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def index_documents(docs_path="../docs"):
    """Index all documents"""
    try:
        from document_indexer import index_robotics_book
        print("🔄 Indexing documents (this may take several minutes)...")
        stats = index_robotics_book(docs_path)
        print(f"✅ Indexing complete:")
        print(f"   - Total files: {stats['total_files']}")
        print(f"   - Indexed: {stats['indexed_files']}")
        print(f"   - Chunks: {stats['total_chunks']}")
        if stats['errors']:
            print(f"   - Errors: {len(stats['errors'])}")
        return True
    except Exception as e:
        print(f"❌ Indexing failed: {e}")
        return False

def main():
    """Run setup process"""
    print("\n" + "="*50)
    print("Robotics Book RAG Chatbot - Backend Setup")
    print("="*50 + "\n")
    
    # Check Python version
    print("1. Checking Python version...")
    check_python_version()
    
    # Check dependencies
    print("\n2. Checking dependencies...")
    if not check_dependencies():
        print("   Install with: pip install -r requirements.txt")
        return
    
    # Create .env file
    print("\n3. Setting up environment variables...")
    if not create_env_file():
        print("   Please copy .env.example to .env and configure it")
        return
    
    # Initialize database
    print("\n4. Initializing database...")
    if not setup_database():
        print("   Make sure DATABASE_URL is correctly configured in .env")
        return
    
    # Index documents
    print("\n5. Indexing documents...")
    index_docs = input("   Index documents now? (y/n): ").lower() == 'y'
    if index_docs:
        if not index_documents():
            print("   You can run indexing later with: python -c \"from document_indexer import index_robotics_book; index_robotics_book()\"")
    
    print("\n" + "="*50)
    print("Setup complete! ✅")
    print("="*50)
    print("\nNext steps:")
    print("1. Update .env with your API keys:")
    print("   - OPENAI_API_KEY (from https://platform.openai.com/api-keys)")
    print("   - DATABASE_URL (from Neon)")
    print("   - QDRANT_URL and QDRANT_API_KEY (from Qdrant Cloud)")
    print("\n2. Start the server:")
    print("   python -m uvicorn main:app --reload")
    print("\n3. Open browser:")
    print("   http://localhost:8000/docs")
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
