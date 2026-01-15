from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base
from database import DATABASE_URL, engine
import requests

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def list_users():
    print("--- Listing Users ---")
    users = db.query(User).all()
    for u in users:
        print(f"ID: {u.id}, Email: {u.email}, Role: {u.role.value}, Active: {u.is_active}")
    print("---------------------")

def test_register_and_login():
    email = "debug_patient@example.com"
    password = "DebugPassword123!"
    
    # Check if exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print(f"User {email} already exists. Deleting for clean test...")
        db.delete(existing)
        db.commit()

    print(f"Registering {email}...")
    reg_response = requests.post("http://localhost:8001/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Debug Patient",
        "role": "patient",
        "phone": "555-0000"
    })
    
    if reg_response.status_code == 200:
        print("Registration SUCCESS")
        print("Attempting to Login...")
        login_response = requests.post("http://localhost:8001/auth/login", json={
            "email": email,
            "password": password
        })
        if login_response.status_code == 200:
            print("Login SUCCESS!")
            print(login_response.json())
        else:
            print(f"Login FAILED: {login_response.status_code}")
            print(login_response.text)
    else:
        print(f"Registration FAILED: {reg_response.status_code}")
        print(reg_response.text)

if __name__ == "__main__":
    list_users()
    test_register_and_login()
