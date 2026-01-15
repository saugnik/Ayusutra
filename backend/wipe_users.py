from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base, Appointment, TherapySession, Feedback, Notification, PatientHealthLog, Symptom, ChatMessage, AuditLog
from database import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def wipe_users():
    db = SessionLocal()
    try:
        print("Cleaning up child tables...")
        # Delete data that references users/patients/practitioners
        db.query(ChatMessage).delete()
        db.query(Notification).delete()
        db.query(Feedback).delete()
        db.query(PatientHealthLog).delete()
        db.query(Symptom).delete()
        db.query(TherapySession).delete()
        db.query(Appointment).delete()
        db.query(AuditLog).delete()
        db.commit()
        print("Child tables cleaned.")

        users = db.query(User).all()
        count = len(users)
        print(f"Found {count} users.")
        
        if count > 0:
            print("Deleting all users (and cascading to profiles)...")
            for user in users:
                db.delete(user)
            db.commit()
            print("All users deleted successfully.")
        else:
            print("No users found to delete.")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        db.rollback()
    finally:
        db.close()

import sys

if __name__ == "__main__":
    if "--force" in sys.argv:
        print("Force flag detected. Proceeding without confirmation.")
        wipe_users()
    else:
        confirm = input("Are you sure you want to delete ALL users? Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            wipe_users()
        else:
            print("Operation cancelled.")
