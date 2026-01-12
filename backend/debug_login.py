
import requests

BASE_URL = "http://localhost:8001"

def test_login(email, password):
    print(f"Testing login for {email}...")
    url = f"{BASE_URL}/auth/login"
    # Endpoints expects JSON
    data = {
        "email": email,
        "password": password
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("✅ Login Successful")
            print(response.json())
            return True
        else:
            print(f"❌ Login Failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

# Test Practitioner Login
print("--- Practitioner Login ---")
test_login("dr.sharma@ayursutra.com", "password123")

# Test Patient Login (if one exists, otherwise we'll see failure or need to create one)
# I'll try to register one first to be sure
print("\n--- Registering & Logging in Patient ---")
reg_data = {
    "email": "patient@test.com",
    "password": "password123",
    "full_name": "Test Patient",
    "role": "patient",
    "date_of_birth": "1990-01-01",
    "gender": "Male",
    "address": "123 Test St",
    "emergency_contact": "9999999999"
}
requests.post(f"{BASE_URL}/auth/register", json=reg_data) # Ignore result if already exists
test_login("patient@test.com", "password123")
