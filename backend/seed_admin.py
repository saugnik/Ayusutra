import os
import sys
from datetime import datetime
from sqlalchemy.orm import Session

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, User, Admin, UserRole
from auth import get_password_hash

def seed_admin():
    db = SessionLocal()
    try:
        email = "admin@ayursutra.com"
        password = "Admin@123" 
        full_name = "System Super Admin"
        
        # Check if exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"Admin user {email} already exists.")
            # Ensure it has admin profile
            admin_profile = db.query(Admin).filter(Admin.user_id == existing_user.id).first()
            if not admin_profile:
                print("Creating missing Admin profile...")
                admin_profile = Admin(
                    user_id=existing_user.id,
                    admin_level="super",
                    permissions=["all"],
                    department="IT"
                )
                db.add(admin_profile)
                db.commit()
                print("Admin profile created.")
            return

        print(f"Creating Super Admin: {email}")
        
        # Create User
        new_user = User(
            email=email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
            created_at=datetime.utcnow()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create Admin Profile
        admin_profile = Admin(
            user_id=new_user.id,
            admin_level="super",
            permissions=["all"],
            department="IT"
        )
        db.add(admin_profile)
        db.commit()
        
        print("Super Admin created successfully!")
        
    except Exception as e:
        print(f"Error seeding admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
