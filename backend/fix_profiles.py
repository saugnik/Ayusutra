
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Practitioner, Patient, Admin, UserRole

def fix_profiles():
    db: Session = SessionLocal()
    try:
        users = db.query(User).all()
        fixed_count = 0

        for user in users:
            role_val = user.role.value if hasattr(user.role, 'value') else str(user.role)
            
            if role_val == "practitioner":
                profile = db.query(Practitioner).filter(Practitioner.user_id == user.id).first()
                if not profile:
                    print(f"Fixing missing profile for Practitioner {user.email}...")
                    new_profile = Practitioner(
                        user_id=user.id,
                        license_number="PENDING-FIX",
                        specializations=["General Ayurveda"],
                        clinic_name="Default Clinic",
                        clinic_address="Update Address"
                    )
                    db.add(new_profile)
                    fixed_count += 1
            
            elif role_val == "patient":
                profile = db.query(Patient).filter(Patient.user_id == user.id).first()
                if not profile:
                    print(f"Fixing missing profile for Patient {user.email}...")
                    new_profile = Patient(
                        user_id=user.id,
                        gender="Other",
                        prakriti_type="Unknown"
                    )
                    db.add(new_profile)
                    fixed_count += 1

            elif role_val == "admin":
                profile = db.query(Admin).filter(Admin.user_id == user.id).first()
                if not profile:
                    print(f"Fixing missing profile for Admin {user.email}...")
                    new_profile = Admin(
                        user_id=user.id,
                        admin_level="standard",
                        permissions=["user_management"]
                    )
                    db.add(new_profile)
                    fixed_count += 1
        
        if fixed_count > 0:
            db.commit()
            print(f"Successfully created {fixed_count} missing profiles.")
        else:
            print("No missing profiles found.")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_profiles()
