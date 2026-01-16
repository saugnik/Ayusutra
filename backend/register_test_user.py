
import requests

BASE_URL = "http://localhost:8001"

def register_user():
    user_data = {
        "email": "testagent1@example.com",
        "full_name": "Test Agent User",
        "password": "password123",
        "role": "patient",
        "date_of_birth": "1990-01-01T00:00:00",
        "gender": "Male"
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"Register Status: {resp.status_code}")
        print(f"Register Response: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_user()
