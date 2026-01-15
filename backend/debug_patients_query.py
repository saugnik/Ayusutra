from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, User, Patient, Practitioner, Appointment
from backend.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def debug_queries():
    print("--- Debugging Patient Queries ---")
    
    # Mock current practitioner - find the one with appointments or just the first one
    practitioner = db.query(Practitioner).first()
    if not practitioner:
        print("No practitioner found.")
        return
        
    print(f"Practitioner ID: {practitioner.id}")
    
    # 1. Dashboard Query Logic
    total_patients_dash = db.query(Appointment).filter(
        Appointment.practitioner_id == practitioner.id
    ).distinct(Appointment.patient_id).count()
    print(f"Dashboard Count (Appointment Distinct): {total_patients_dash}")
    
    # 2. Get My Patients Query Logic
    patients_list = db.query(Patient).join(Appointment).filter(
        Appointment.practitioner_id == practitioner.id
    ).distinct().all()
    print(f"GetMyPatients Count (Patient Join): {len(patients_list)}")
    
    # Detail
    if len(patients_list) == 0 and total_patients_dash > 0:
        print("MISMATCH DETECTED!")
        print("Checking Appointments for this practitioner:")
        appts = db.query(Appointment).filter(Appointment.practitioner_id == practitioner.id).all()
        for appt in appts:
            print(f"  Appt ID: {appt.id}, Patient ID: {appt.patient_id}")
            # Check if patient exists
            pat = db.query(Patient).filter(Patient.id == appt.patient_id).first()
            print(f"    -> Patient Record? {pat is not None}")
            if pat:
                print(f"    -> Patient User ID: {pat.user_id}")
                usr = db.query(User).filter(User.id == pat.user_id).first()
                print(f"    -> User Record? {usr is not None}")

if __name__ == "__main__":
    debug_queries()
