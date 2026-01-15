
import requests
import sys

BASE_URL = "http://localhost:8001"

def test_login():
    email = "practitioner_flow_1736913456@test.com" # Use a known email
    # Or try to register a new one to be sure
    reg_email = "login_test_user@test.com"
    
    print(f"1. Registering {reg_email}...")
    r = requests.post(f"{BASE_URL}/auth/register", json={
        "email": reg_email, "password": "password123", "full_name": "Login Test", "role": "practitioner", "phone": "555"
    })
    print(f"Register status: {r.status_code}")
    
    print("2. Logging in...")
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": reg_email, "password": "password123"})
    print(f"Login status: {r.status_code}")
    if r.status_code == 200:
        print("Login SUCCESS")
        print(r.json().keys())
    else:
        print(f"Login FAILED: {r.text}")

if __name__ == "__main__":
    try:
        test_login()
    except Exception as e:
        print(f"Exception: {e}")
