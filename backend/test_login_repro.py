
import sys
import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# Add current directory to path to allow imports
sys.path.append(os.getcwd())

from models import User, UserRole
from database import Base, get_db
from auth import verify_password, create_access_token, get_password_hash

# Setup DB connection (using the sqlite file in current dir)
SQLALCHEMY_DATABASE_URL = "sqlite:///./ayursutra.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_login_logic(email, password):
    db = SessionLocal()
    try:
        print(f"Testing login for {email}...")
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print("User not found!")
            return

        print(f"User found: {user.id}, Role type: {type(user.role)}, Role value: {user.role}")
        
        # Simulate checks in login endpoint
        if not verify_password(password, user.hashed_password):
            print("Password mismatch")
            return
            
        if not user.is_active:
            print("User inactive")
            return
            
        # Simulate last login update
        from datetime import datetime
        user.last_login = datetime.utcnow()
        # db.commit() # Skip commit to avoid modifying real data during test if possible, but the error might be IN commit
        
        # Simulate token creation (suspected area)
        print("Attempting to access user.role.value...")
        try:
            role_val = user.role.value
            print(f"Role value accessed: {role_val}")
        except AttributeError as e:
            print(f"CRITICAL ERROR accessing user.role.value: {e}")
            print(f"user.role is actually: {user.role!r} (type: {type(user.role)})")
            raise

        access_token = create_access_token(data={"sub": user.email, "role": role_val})
        print(f"Token created: {access_token[:20]}...")
        
        print("Login logic finished successfully.")

    except Exception as e:
        print(f"\nCAUGHT EXCEPTION: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    # Test with the user mentioned in previous conversations or a known one
    # I saw 'saugnikaich123@gmail.com' in conversation history
    test_login_logic("saugnikaich123@gmail.com", "password123") # Assuming a password or just testing retrieval
    
    # Also list all users to see if any have weird roles
    db = SessionLocal()
    users = db.query(User).all()
    print("\nChecking all users roles:")
    for u in users:
        print(f"ID: {u.id}, Email: {u.email}, Role Type: {type(u.role)}, Role: {u.role}")
    db.close()
