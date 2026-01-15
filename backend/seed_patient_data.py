
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Patient, PatientHealthLog, Appointment, UserRole
from datetime import datetime, timedelta
import random

def seed_patient_data():
    db: Session = SessionLocal()
    try:
        # 1. Get or Create a Test Patient User
        email = "patient_demo@test.com"
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"Creating demo patient: {email}")
            from auth import get_password_hash
            user = User(
                email=email,
                hashed_password=get_password_hash("password123"),
                full_name="Demo Patient",
                role=UserRole.PATIENT,
                is_active=True,
                is_verified=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Create Patient Profile
            patient = Patient(
                user_id=user.id,
                gender="Female",
                date_of_birth=datetime(1990, 1, 1),
                prakriti_type="Vata-Pitta"
            )
            db.add(patient)
            db.commit()
            db.refresh(patient)
        else:
            patient = db.query(Patient).filter(Patient.user_id == user.id).first()
            if not patient:
                print("Fixing missing profile for demo patient...")
                patient = Patient(user_id=user.id, gender="Female", prakriti_type="Vata-Pitta")
                db.add(patient)
                db.commit()
                db.refresh(patient)
            print(f"Found existing patient: {email} (ID: {patient.id})")

        # 1.5 Ensure Practitioner Exists
        from models import Practitioner
        practitioner = db.query(Practitioner).first()
        if not practitioner:
             print("Creating dummy practitioner...")
             p_user = db.query(User).filter(User.email == "doc_demo@test.com").first()
             if not p_user:
                 from auth import get_password_hash
                 p_user = User(email="doc_demo@test.com", hashed_password=get_password_hash("pass"), full_name="Dr. Demo", role=UserRole.PRACTITIONER, is_active=True)
                 db.add(p_user)
                 db.commit()
             
             practitioner = Practitioner(user_id=p_user.id, license_number="DOC123")
             db.add(practitioner)
             db.commit()
             db.refresh(practitioner)

        # 2. Check/Add Health Logs (Fake Data)
        logs = db.query(PatientHealthLog).filter(PatientHealthLog.patient_id == patient.id).all()
        if not logs:
            print(f"Seeding Health Logs with Practitioner ID {practitioner.id}...")
            log = PatientHealthLog(
                patient_id=patient.id,
                practitioner_id=practitioner.id,
                date=datetime.now().date(),
                sleep_score=85,
                stress_level="Medium",
                hydration=2.0,
                dosha_vata=60,
                dosha_pitta=30,
                dosha_kapha=10,
                notes="Feeling better after yoga.",
                recommendations="Continue Vata-pacifying diet. Warm oil massage recommended."
            )
            db.add(log)
            db.commit()
            print("Health Log added.")
        else:
            print("Health Logs already exist.")

        # 3. Check/Add Appointments (Fake Data)
        from models import Practitioner
        practitioner = db.query(Practitioner).first()
        if not practitioner:
             print("Creating dummy practitioner for appointments...")
             # Need a user first
             p_user = db.query(User).filter(User.email == "doc_demo@test.com").first()
             if not p_user:
                 from auth import get_password_hash
                 p_user = User(email="doc_demo@test.com", hashed_password=get_password_hash("pass"), full_name="Dr. Demo", role=UserRole.PRACTITIONER, is_active=True)
                 db.add(p_user)
                 db.commit()
             
             practitioner = Practitioner(user_id=p_user.id, license_number="DOC123")
             db.add(practitioner)
             db.commit()
             db.refresh(practitioner)
        
        appts = db.query(Appointment).filter(Appointment.patient_id == patient.id).all()
        if not appts:
            print(f"Seeding Appointments with Practitioner ID {practitioner.id}...")
            # Pending
            a1 = Appointment(
                patient_id=patient.id,
                practitioner_id=practitioner.id, 
                therapy_type="Shirodhara",
                scheduled_datetime=datetime.now() + timedelta(days=2),
                duration_minutes=60,
                status="scheduled",
                notes="Pre-treatment consultation done."
            )
            db.add(a1)
            db.commit()
            print("Appointment added.")
        else:
            print("Appointments already exist.")

        print("\nSEEDING COMPLETE.")
        print(f"Login Credentials: {email} / password123")

    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_patient_data()
