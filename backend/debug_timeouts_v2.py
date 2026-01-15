
import requests
import time
import sys

BASE_URL = "http://localhost:8001"
TIMEOUT = 10

def get_token():
    email = f"debug_timeout_{int(time.time())}@test.com"
    password = "password123"
    
    # 1. Register
    print(f"Registering {email}...")
    r = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email, "password": password, "full_name": "Debug Doc", "role": "practitioner", "phone": "123"
    })
    
    # 2. Login
    print("Logging in...")
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if r.status_code == 200:
        return r.json()["access_token"]
    
    print(f"Login failed: {r.text}")
    return None

def check_endpoints():
    token = get_token()
    if not token:
        print("FAIL: No token")
        return

    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints = [
        "/reports/treatments",
        "/reports/monthly-summary",
        "/reports/feedback"
    ]
    
    for ep in endpoints:
        print(f"\nTesting {ep}...")
        try:
            r = requests.get(f"{BASE_URL}{ep}", headers=headers, timeout=TIMEOUT)
            print(f"Status: {r.status_code}")
            if r.status_code == 200:
                print("Response OK")
            else:
                print(f"Error: {r.text}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    check_endpoints()
