#!/usr/bin/env python
"""
Startup script for the minimal robotics chatbot
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from app_minimal import app

if __name__ == "__main__":
    print("🚀 Starting Robotics Chatbot Backend...")
    print("📍 Listening on http://0.0.0.0:8000")
    print("✅ Health check: http://localhost:8000/health")
    print("-" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
