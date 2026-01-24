"""Reset test user password"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from auth import get_password_hash

DATABASE_URL = "sqlite:///./ayursutra.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

user = db.query(User).filter(User.email == "patient@test.com").first()

if user:
    print(f"Found user: {user.email}")
    print(f"Current active status: {user.is_active}")
    
    # Reset password
    user.hashed_password = get_password_hash("patient123")
    user.is_active = True
    db.commit()
    
    print("✅ Password reset to 'patient123'")
    print("✅ User activated")
else:
    print("❌ User not found!")

db.close()
