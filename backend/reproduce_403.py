
import requests
import sys

BASE_URL = "http://localhost:8001"

def login(email, password):
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if r.status_code == 200:
        return r.json()["access_token"]
    return None

def test_endpoint(token, role_name):
    print(f"\nTesting /reports/treatments with {role_name} token...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/reports/treatments", headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:100]}")

if __name__ == "__main__":
    # 1. Login as Practitioner (created previously)
    token_prac = login("practitioner_flow_1736913456@test.com", "password123")
    if token_prac:
        test_endpoint(token_prac, "PRACTITIONER")
    else:
        print("Could not login as practitioner")

    # 2. Login as Patient
    # We need a patient. Let's try to register one or use known one.
    # The previous flow verified a patient.
    token_pat = login("p_flow_1736913456@test.com", "password123") # Assuming timestamp matched
    # If not, let's register a new one to be sure
    if not token_pat:
        email = "patient_403_test@test.com"
        requests.post(f"{BASE_URL}/auth/register", json={
            "email": email, "password": "password123", "full_name": "Test Pat", "role": "patient", "phone": "123"
        })
        token_pat = login(email, "password123")
    
    if token_pat:
        test_endpoint(token_pat, "PATIENT")
    else:
        print("Could not login as patient")
