from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Admin, UserRole
from auth import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        email = "admin_demo@test.com"
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"Creating admin user: {email}")
            user = User(
                email=email,
                hashed_password=get_password_hash("admin123"),
                full_name="System Admin",
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Create Admin Profile
            admin_profile = Admin(
                user_id=user.id,
                admin_level="super",
                permissions=["all"],
                department="IT"
            )
            db.add(admin_profile)
            db.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")
            
        print(f"Admin Credentials: {email} / admin123")
        
    except Exception as e:
        print(f"Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
