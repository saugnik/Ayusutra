
import sqlite3
import bcrypt  # You might need passlib/bcrypt installed, assuming backend environment has it
from datetime import datetime

# Mimic backend hashing if possible, or insert via API?
# API is safer. Let's use requests to register.

import requests

BASE_URL = "http://localhost:8002"

def create_patient():
    print("Creating test patient via API...")
    
    user_data = {
        "email": "test_patient_gpu@ayursutra.com",
        "password": "password123",
        "full_name": "Test GPU Patient",
        "confirm_password": "password123",
         "role": "patient" # API might infer this or require it
    }
    
    # Register endpoint? Usually /auth/register or similar.
    # Let's check main.py for verify.
    
    try:
        # Try /auth/register
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        
        if response.status_code in [200, 201]:
            print("✓ User created successfully!")
            return True
        elif response.status_code == 400 and "Email already registered" in response.text:
             print("User already exists. Proceeding.")
             return True
        else:
            print(f"Failed to create user: {response.status_code} {response.text}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    create_patient()
