import requests
import json
import sys

# Force UTF-8 encoding for output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

url = "http://localhost:8001/auth/register"

data = {
    "full_name": "Test User",
    "email": "testuser@example.com",
    "phone": "1234567890",
    "password": "12345",
    "role": "patient"
}

print("=" * 60)
print("Testing Registration")
print("=" * 60)
print(f"\nRequest URL: {url}")
print(f"Request Data:\n{json.dumps(data, indent=2)}")
print("\nSending request...")

try:
    response = requests.post(url, json=data)
    print(f"\nResponse Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("\nSUCCESS! Registration completed!")
        print(f"\nResponse Data:\n{json.dumps(response.json(), indent=2)}")
    else:
        print(f"\nFAILED! Status Code: {response.status_code}")
        print(f"\nResponse Text:\n{response.text}")
            
except Exception as e:
    print(f"\nException: {e}")
