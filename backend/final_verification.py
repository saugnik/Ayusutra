import requests
import json
import random

# Generate unique email
unique_id = random.randint(10000, 99999)
email = f"test.user.{unique_id}@example.com"

print("=" * 70)
print("FINAL VERIFICATION TEST")
print("=" * 70)

registration_data = {
    "full_name": f"Test User {unique_id}",
    "email": email,
    "phone": f"555{unique_id}",
    "password": "12345",
    "role": "patient"
}

print(f"\n[1] Testing Registration with NEW user...")
print(f"    Email: {email}")

try:
    response = requests.post(
        "http://localhost:8001/auth/register",
        json=registration_data
    )
    
    if response.status_code == 200:
        print(f"\n    ✓ REGISTRATION SUCCESSFUL!")
        user_data = response.json()
        print(f"    - User ID: {user_data.get('id')}")
        print(f"    - Email: {user_data.get('email')}")
        print(f"    - Role: {user_data.get('role')}")
        
        # Test login
        print(f"\n[2] Testing Login...")
        login_response = requests.post(
            "http://localhost:8001/auth/login",
            json={"email": email, "password": "12345"}
        )
        
        if login_response.status_code == 200:
            print(f"    ✓ LOGIN SUCCESSFUL!")
            token_data = login_response.json()
            print(f"    - Token received: {token_data.get('access_token')[:30]}...")
            
            print("\n" + "=" * 70)
            print("✓✓✓ ALL TESTS PASSED! AUTHENTICATION IS WORKING! ✓✓✓")
            print("=" * 70)
        else:
            print(f"    ✗ Login failed: {login_response.status_code}")
            print(f"    Error: {login_response.text}")
    else:
        print(f"\n    ✗ Registration failed: {response.status_code}")
        print(f"    Error: {response.text}")
        
except Exception as e:
    print(f"\n    ✗ Error: {e}")
