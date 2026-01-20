"""
Database Configuration
SQLAlchemy setup and database connection management.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL - defaults to SQLite for development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./ayursutra.db"
)

# For PostgreSQL in production, use:
# DATABASE_URL = "postgresql://username:password@localhost/ayursutra"

# Create SQLAlchemy engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}  # Only needed for SQLite
    )
else:
    engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        import traceback
        from datetime import datetime
        with open("backend_error.log", "a") as f:
            f.write(f"DB CRASH AT {datetime.utcnow()}:\n")
            f.write(traceback.format_exc())
            f.write("\n")
        db.rollback()
        raise
    finally:
        db.close()
