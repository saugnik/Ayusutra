
from database import SessionLocal
from models import Practitioner, User

def get_practitioner_email():
    db = SessionLocal()
    try:
        practitioner = db.query(Practitioner).first()
        if practitioner:
            user = db.query(User).filter(User.id == practitioner.user_id).first()
            if user:
                print(f"FOUND_EMAIL: {user.email}")
                return
        print("NO_PRACTITIONER_FOUND")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    get_practitioner_email()
