import requests
import json
import random

BASE_URL = "http://localhost:8001"

def register_and_login(role, user_details):
    print(f"\n[{role.upper()} TEST]")
    print("-" * 40)
    
    # Register
    print(f"1. Registering {role}...")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_details)
        if response.status_code == 200:
            user_data = response.json()
            print(f"   ✓ Success! ID: {user_data['id']}, Role: {user_data['role']}")
        else:
            print(f"   ✗ Registration Failed: {response.status_code}")
            print(f"   {response.text}")
            return
    except Exception as e:
        print(f"   ✗ Connection Error: {e}")
        return

    # Login
    print(f"2. Logging in as {role}...")
    try:
        login_data = {
            "email": user_details["email"],
            "password": user_details["password"]
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"   ✓ Login Success!")
            print(f"   ✓ Token Role in Response: {token_data.get('role')}")
            print(f"   ✓ User ID: {token_data.get('user_id')}")
        else:
            print(f"   ✗ Login Failed: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"   ✗ Connection Error: {e}")

# --- Test Data ---
suffix = random.randint(1000, 9999)

# 1. Practitioner
practitioner_data = {
    "full_name": f"Dr. Test Practitioner {suffix}",
    "email": f"practitioner.{suffix}@hospital.com",
    "password": "securepassword",
    "phone": "9876543210",
    "role": "practitioner",
    # Optional profile fields
    "license_number": f"LIC-{suffix}",
    "clinic_name": "AyurSutra Wellness Center",
    "specializations": ["Ayurveda", "Panchakarma"]
}

# 2. Admin
admin_data = {
    "full_name": f"Admin User {suffix}",
    "email": f"admin.{suffix}@ayursutra.com",
    "password": "adminpassword",
    "phone": "1231231234",
    "role": "admin"
}

if __name__ == "__main__":
    print("=== TESTING ROLE-BASED AUTHENTICATION ===\n")
    register_and_login("practitioner", practitioner_data)
    register_and_login("admin", admin_data)
    print("\n" + "="*40)
