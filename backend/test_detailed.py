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

print("="*60)
print("Testing Registration for Saugnik Aich")
print("="*60)
print(f"\nRequest URL: {url}")
print(f"Request Data:\n{json.dumps(data, indent=2)}")
print("\nSending request...")

try:
    response = requests.post(url, json=data)
    print(f"\n{'='*60}")
    print(f"Response Status Code: {response.status_code}")
    print(f"{'='*60}")
    
    if response.status_code == 200:
        print("\n✓ SUCCESS! Registration completed!")
        print(f"\nResponse Data:\n{json.dumps(response.json(), indent=2)}")
    else:
        print(f"\n✗ FAILED! Status Code: {response.status_code}")
        print(f"\nFull Response Text:\n{response.text}")
        try:
            error_data = response.json()
            print(f"\nError JSON:\n{json.dumps(error_data, indent=2)}")
        except:
            print("\nCould not parse error as JSON")
            
except requests.exceptions.RequestException as e:
    print(f"\n✗ Request Exception: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"\nResponse Text: {e.response.text}")
