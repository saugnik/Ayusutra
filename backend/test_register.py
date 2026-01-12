import requests
import json

print("Testing Registration Endpoint...")
print("=" * 60)

url = "http://localhost:8001/auth/register"
data = {
    "email": "pythontest@example.com",
    "full_name": "Python Test User",
    "password": "test123",
    "role": "patient"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ SUCCESS!")
        print(json.dumps(response.json(), indent=2))
    else:
        print("✗ FAILED!")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"✗ ERROR: {e}")

print("=" * 60)
print("\nNow check the backend terminal for the Python error traceback!")
