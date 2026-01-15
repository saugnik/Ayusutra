import requests
import sys

BASE_URL = "http://localhost:8001"

def test_login(email, password):
    print(f"Attempting login for {email}...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Login SUCCESS!")
            print(response.json())
        else:
            print("Login FAILED!")
            print(response.text)
    except Exception as e:
        print(f"Request Error: {e}")

if __name__ == "__main__":
    # detailed usage
    if len(sys.argv) > 2:
        test_login(sys.argv[1], sys.argv[2])
    else:
        # Default test user - assume one exists or create one
        print("Usage: python backend/test_login_debug.py <email> <password>")
        print("Using default 'patient@example.com' / 'password123'")
        test_login("patient@example.com", "password123")
