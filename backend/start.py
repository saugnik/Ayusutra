#!/usr/bin/env python3
"""
AyurSutra Backend Startup Script
Run this to start the backend server.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        import passlib
        import jwt
        import requests
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return False

def setup_environment():
    """Set up environment variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating default .env file...")
        env_content = """# AyurSutra Backend Environment Variables
SECRET_KEY=ayursutra-secret-key-change-in-production-please
DATABASE_URL=sqlite:///./ayursutra.db
RAG_SERVICE_URL=http://localhost:8000

# For PostgreSQL (uncomment and modify if needed):
# DATABASE_URL=postgresql://username:password@localhost/ayursutra

# CORS Origins (frontend URLs)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# API Configuration
API_PORT=8001
API_HOST=0.0.0.0
DEBUG=true
"""
        env_file.write_text(env_content)
        print("✅ Created .env file with default settings")

def create_database():
    """Initialize database tables"""
    try:
        from database import engine
        from models import Base
        
        print("📊 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False
    return True

def start_server():
    """Start the FastAPI server"""
    try:
        port = os.getenv("API_PORT", "8001")
        host = os.getenv("API_HOST", "0.0.0.0")
        
        print(f"🚀 Starting AyurSutra Backend server...")
        print(f"   Server: http://{host}:{port}")
        print(f"   API Docs: http://{host}:{port}/docs")
        print(f"   ReDoc: http://{host}:{port}/redoc")
        print()
        print("Press CTRL+C to stop the server")
        
        import uvicorn
        uvicorn.run(
            "main:app",
            host=host,
            port=int(port),
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("🌿 AyurSutra Backend Startup")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found. Please run this script from the backend directory.")
        sys.exit(1)
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  Warning: python-dotenv not installed, using system environment variables only")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
