import requests

print("Checking backend status...")
try:
    response = requests.get("http://localhost:8001/")
    print(f"✓ Backend is running on port 8001! Status: {response.status_code}")
except Exception as e:
    print(f"✗ Backend NOT accessible on port 8001: {e}")

print("\nTesting registration...")
try:
    data = {
        "full_name": "Quick Test",
        "email": "quicktest@example.com",
        "phone": "5555555555",
        "password": "12345",
        "role": "patient"
    }
    response = requests.post("http://localhost:8001/auth/register", json=data)
    if response.status_code == 200:
        print(f"✓ Registration SUCCESSFUL!")
        print(f"Response: {response.json()}")
    else:
        print(f"✗ Registration FAILED! Status: {response.status_code}")
        print(f"Error: {response.text}")
except Exception as e:
    print(f"✗ Registration request failed: {e}")
