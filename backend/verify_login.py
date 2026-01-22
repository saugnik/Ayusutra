
import requests

BASE_URL = "http://localhost:8002"
EMAIL = "test_patient_gpu@ayursutra.com"
PASSWORD = "password123"

def test_login():
    print(f"Attempting login for {EMAIL}...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": EMAIL, "password": PASSWORD}
        )
        
        if response.status_code == 200:
            print("✓ Login successful!")
            token = response.json().get('access_token')
            print(f"Token received: {token[:20]}...")
            return token
        else:
            print(f"✗ Login failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    test_login()
