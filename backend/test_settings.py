
import requests
import sys

BASE_URL = "http://localhost:8001"

def login(email, password):
    r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if r.status_code == 200:
        return r.json()["access_token"]
    return None

def test_settings_flow():
    # 1. Register a test user
    email = "settings_test_v2@test.com"
    password = "password123"
    try:
        requests.post(f"{BASE_URL}/auth/register", json={
            "email": email, "password": password, "full_name": "Settings Tester", "role": "patient", "phone": "1234567890"
        })
    except:
        pass

    print(f"Logging in as {email}...")
    token = login(email, password)
    if not token:
        print("Login failed")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Test GET /users/me
    print("\nTesting GET /users/me...")
    r = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print(f"Current Name: {r.json()['full_name']}")
    
    # 3. Test UPDATE Profile
    print("\nTesting PUT /users/me (Update Name)...")
    r = requests.put(f"{BASE_URL}/users/me", headers=headers, json={"full_name": "Updated Name"})
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print(f"New Name: {r.json()['full_name']}")
        if r.json()['full_name'] != "Updated Name":
            print("FAILURE: Name not updated")
    
    # 4. Test Password Update
    print("\nTesting Password Update...")
    new_password = "newpassword456"
    r = requests.put(f"{BASE_URL}/users/me", headers=headers, json={"password": new_password})
    print(f"Status: {r.status_code}")
    
    # 5. Verify Login with New Password
    print("\nVerifying Login with New Password...")
    token_new = login(email, new_password)
    if token_new:
        print("SUCCESS: Login with new password works!")
    else:
        print("FAILURE: Login with new password failed")

if __name__ == "__main__":
    test_settings_flow()
