
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Practitioner, Patient, Admin, UserRole

def audit_users():
    db: Session = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"Total Users: {len(users)}")
        print("-" * 60)
        print(f"{'ID':<5} | {'Email':<30} | {'Role':<15} | {'Profile Status'}")
        print("-" * 60)
        
        issues_found = []

        for user in users:
            role_val = user.role.value if hasattr(user.role, 'value') else str(user.role)
            status = "OK"
            
            if role_val == "practitioner":
                profile = db.query(Practitioner).filter(Practitioner.user_id == user.id).first()
                if not profile:
                    status = "MISSING PROFILE"
                    issues_found.append(user)
            elif role_val == "patient":
                profile = db.query(Patient).filter(Patient.user_id == user.id).first()
                if not profile:
                    status = "MISSING PROFILE"
                    issues_found.append(user)
            elif role_val == "admin":
                profile = db.query(Admin).filter(Admin.user_id == user.id).first()
                if not profile:
                    status = "MISSING PROFILE"
                    issues_found.append(user)
            
            print(f"{user.id:<5} | {user.email:<30} | {role_val:<15} | {status}")

        print("-" * 60)
        if issues_found:
            print(f"\nFOUND {len(issues_found)} USERS WITH MISSING PROFILES!")
            for u in issues_found:
                print(f" - Fix needed for User ID {u.id} ({u.email})")
        else:
            print("\nAll users have consistent profiles.")

    finally:
        db.close()

if __name__ == "__main__":
    audit_users()
