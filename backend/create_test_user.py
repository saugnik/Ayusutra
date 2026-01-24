"""Create test patient user for testing"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Patient, UserRole
from auth import get_password_hash
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///./ayursutra.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Check if user exists
existing_user = db.query(User).filter(User.email == "patient@test.com").first()

if existing_user:
    print(f"✅ User already exists: {existing_user.email}")
    print(f"   Role: {existing_user.role.value}")
    print(f"   Active: {existing_user.is_active}")
else:
    print("Creating new test patient user...")
    
    # Create user
    new_user = User(
        email="patient@test.com",
        hashed_password=get_password_hash("patient123"),
        full_name="Test Patient",
        role=UserRole.PATIENT,
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.flush()
    
    # Create patient profile
    new_patient = Patient(
        user_id=new_user.id,
        date_of_birth=datetime(1995, 1, 1),
        gender="male",
        prakriti_type="vata-pitta",
        medical_history="None",
        allergies="None",
        current_medications="None"
    )
    db.add(new_patient)
    db.commit()
    
    print(f"✅ Created user: {new_user.email}")
    print(f"   User ID: {new_user.id}")
    print(f"   Patient ID: {new_patient.id}")

db.close()
print("\n✅ Test user is ready!")
