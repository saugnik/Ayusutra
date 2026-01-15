
import requests
import sys

BASE_URL = "http://localhost:8001"

def test_practitioner_access():
    # 1. Register new practitioner
    email = "prac_test_role@test.com"
    print(f"Registering {email}...")
    try:
        r = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email, "password": "password123", "full_name": "Role Test", "role": "practitioner", "phone": "999"
        })
    except:
        pass # maybe exists

    # 2. Login
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": "password123"})
    if r.status_code != 200:
        print(f"Login failed: {r.text}")
        return
    
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Test Endpoint
    print("Testing /reports/treatments...")
    r = requests.get(f"{BASE_URL}/reports/treatments", headers=headers)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("SUCCESS")
    else:
        print(f"FAILED: {r.text}")

if __name__ == "__main__":
    test_practitioner_access()
