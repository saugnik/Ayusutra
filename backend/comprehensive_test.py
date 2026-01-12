import requests
import json

print("=" * 70)
print("COMPREHENSIVE REGISTRATION TEST")
print("=" * 70)

# Test 1: Check backend health
print("\n[1] Checking Backend Health...")
try:
    response = requests.get("http://localhost:8001/")
    print(f"   ✓ Backend is running! Status: {response.status_code}")
except Exception as e:
    print(f"   ✗ Backend check failed: {e}")
    exit(1)

# Test 2: Register a new user
print("\n[2] Testing User Registration...")
registration_data = {
    "full_name": "Comprehensive Test User",
    "email": "comprehensive.test@example.com",
    "phone": "5554443333",
    "password": "12345",
    "role": "patient"
}

print(f"   Request Data:")
print(f"   {json.dumps(registration_data, indent=6)}")

try:
    response = requests.post(
        "http://localhost:8001/auth/register",
        json=registration_data
    )
    
    if response.status_code == 200:
        print(f"\n   ✓ REGISTRATION SUCCESSFUL!")
        user_data = response.json()
        print(f"\n   Response Data:")
        print(f"   - User ID: {user_data.get('id')}")
        print(f"   - Email: {user_data.get('email')}")
        print(f"   - Full Name: {user_data.get('full_name')}")
        print(f"   - Role: {user_data.get('role')}")
        print(f"   - Created At: {user_data.get('created_at')}")
        
        # Test 3: Login with the new user
        print("\n[3] Testing Login with New User...")
        login_data = {
            "email": registration_data["email"],
            "password": registration_data["password"]
        }
        
        login_response = requests.post(
            "http://localhost:8001/auth/login",
            json=login_data
        )
        
        if login_response.status_code == 200:
            print(f"   ✓ LOGIN SUCCESSFUL!")
            token_data = login_response.json()
            print(f"\n   Token Data:")
            print(f"   - Access Token: {token_data.get('access_token')[:50]}...")
            print(f"   - Token Type: {token_data.get('token_type')}")
            print(f"   - User ID: {token_data.get('user_id')}")
            print(f"   - Role: {token_data.get('role')}")
            
            print("\n" + "=" * 70)
            print("ALL TESTS PASSED! ✓")
            print("=" * 70)
            print("\nSUMMARY:")
            print("  ✓ Backend is running on port 8001")
            print("  ✓ User registration is working")
            print("  ✓ User login is working")
            print("  ✓ JWT token generation is working")
            print("\nThe authentication system is FULLY FUNCTIONAL!")
            print("=" * 70)
        else:
            print(f"   ✗ LOGIN FAILED! Status: {login_response.status_code}")
            print(f"   Error: {login_response.text}")
    else:
        print(f"\n   ✗ REGISTRATION FAILED! Status: {response.status_code}")
        print(f"   Error: {response.text}")
        
except Exception as e:
    print(f"\n   ✗ Request failed: {e}")
    import traceback
    traceback.print_exc()
