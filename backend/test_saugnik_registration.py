import requests
import json

url = "http://localhost:8001/auth/register"

data = {
    "full_name": "Saugnik Aich",
    "email": "saugnikaich123@gmail.com",
    "phone": "6290716143",
    "password": "12345",
    "role": "patient"
}

print("Testing registration for Saugnik Aich...")
print(f"Request data: {json.dumps(data, indent=2)}")
print(f"\nSending POST to {url}...")

try:
    response = requests.post(url, json=data)
    print(f"\n✓ Status Code: {response.status_code}")
    print(f"✓ Response: {json.dumps(response.json(), indent=2)}")
except requests.exceptions.RequestException as e:
    print(f"\n✗ Request failed: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"✗ Status Code: {e.response.status_code}")
        print(f"✗ Response: {e.response.text}")
