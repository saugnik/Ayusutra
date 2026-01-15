
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Patient, PatientHealthLog, Appointment

def check_seed():
    db: Session = SessionLocal()
    try:
        email = "patient_demo@test.com"
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print("User NOT found")
            return
        
        print(f"User found: {user.email} (ID: {user.id})")
        
        patient = db.query(Patient).filter(Patient.user_id == user.id).first()
        if not patient:
            print("Patient profile NOT found")
            return
        print(f"Patient profile found (ID: {patient.id})")
        
        logs = db.query(PatientHealthLog).filter(PatientHealthLog.patient_id == patient.id).all()
        print(f"Health Logs: {len(logs)}")
        
        appts = db.query(Appointment).filter(Appointment.patient_id == patient.id).all()
        print(f"Appointments: {len(appts)}")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_seed()
