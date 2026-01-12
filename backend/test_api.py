import requests
import json

# Test backend health
print("Testing Backend Connection...")
print("=" * 50)

try:
    response = requests.get("http://localhost:8001/health")
    print(f"✓ Backend Health Check: {response.status_code}")
    print(f"  Response: {response.json()}")
except Exception as e:
    print(f"✗ Backend Health Check Failed: {e}")

print("\n" + "=" * 50)
print("Testing User Registration...")
print("=" * 50)

# Test registration
try:
    register_data = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "password123",
        "role": "patient",
        "phone": "+1234567890"
    }
    
    response = requests.post(
        "http://localhost:8001/auth/register",
        json=register_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✓ Registration Successful!")
        print(f"  User: {response.json()}")
    else:
        print(f"✗ Registration Failed: {response.json()}")
        
except Exception as e:
    print(f"✗ Registration Error: {e}")

print("\n" + "=" * 50)
print("Testing User Login...")
print("=" * 50)

# Test login
try:
    login_data = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    response = requests.post(
        "http://localhost:8001/auth/login",
        json=login_data
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✓ Login Successful!")
        result = response.json()
        print(f"  Token: {result['access_token'][:50]}...")
        print(f"  Role: {result['role']}")
        print(f"  User ID: {result['user_id']}")
    else:
        print(f"✗ Login Failed: {response.json()}")
        
except Exception as e:
    print(f"✗ Login Error: {e}")

print("\n" + "=" * 50)
print("Test Complete!")
print("=" * 50)
