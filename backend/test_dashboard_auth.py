"""
Test the actual dashboard endpoint with authentication
"""
import requests
import json

BASE_URL = "http://localhost:8002"

print("Testing Dashboard Endpoint with Authentication")
print("=" * 60)

# Step 1: Login as admin
print("\n1. Logging in as admin...")
login_data = {
    "email": "admin_new@ayursutra.com",
    "password": "password123"
}

try:
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        print(f"   Login successful! Token: {access_token[:20]}...")
    else:
        print(f"   Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        # Try creating admin account first
        print("\n   Trying to register admin account...")
        register_data = {
            "full_name": "Admin User",
            "email": "admin_new@ayursutra.com",
            "password": "password123",
            "phone": "9876543210",
            "role": "admin"
        }
        reg_response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"   Registration: {reg_response.status_code}")
        if reg_response.status_code == 200:
            # Try login again
            response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                print(f"   Login successful after registration!")
            else:
                print(f"   Login still failed: {response.text}")
                exit(1)
        else:
            print(f"   Registration failed: {reg_response.text}")
            exit(1)
except Exception as e:
    print(f"   Error: {e}")
    exit(1)

# Step 2: Call dashboard endpoint with token
print("\n2. Calling dashboard endpoint...")
headers = {"Authorization": f"Bearer {access_token}"}

try:
    response = requests.get(f"{BASE_URL}/admin/dashboard", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n   Dashboard Data:")
        print(f"   - Total Users: {data.get('total_users', 'N/A')}")
        print(f"   - Total Practitioners: {data.get('total_practitioners', 'N/A')}")
        print(f"   - Total Patients: {data.get('total_patients', 'N/A')}")
        print(f"   - Total Appointments: {data.get('total_appointments', 'N/A')}")
        print(f"   - Recent Registrations: {data.get('recent_registrations', 'N/A')}")
        
        if data.get('total_users', 0) == 0:
            print("\n   WARNING: Dashboard shows 0 users!")
            print("   This means the ORM queries are failing.")
        else:
            print("\n   SUCCESS: Dashboard is working correctly!")
    else:
        print(f"   Error: {response.text}")
        
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
