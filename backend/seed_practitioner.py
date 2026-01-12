
import requests

# 1. Register a Practitioner
url = "http://localhost:8001/auth/register"
data = {
    "email": "dr.sharma@ayursutra.com",
    "password": "password123",
    "full_name": "Dr. Priya Sharma",
    "role": "PRACTITIONER",
    "license_number": "AYU-2024-001",
    "specializations": ["Panchakarma", "Vata Disorders"],
    "clinic_name": "AyurHealth Clinic"
}

try:
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("✅ Practitioner Created: Dr. Priya Sharma")
    elif response.status_code == 400 and "already registered" in response.text:
         print("ℹ️ Practitioner already exists.")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")

    # 2. Verify List
    list_resp = requests.get("http://localhost:8001/practitioners")
    print("\nExample from GET /practitioners:")
    print(list_resp.json())

except Exception as e:
    print(f"Error: {e}")
