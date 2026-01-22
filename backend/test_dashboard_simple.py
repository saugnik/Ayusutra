import requests
import json

# Test dashboard endpoint
response = requests.post(
    "http://localhost:8002/auth/login",
    json={"email": "admin_new@ayursutra.com", "password": "password123"}
)

if response.status_code == 200:
    token = response.json()['access_token']
    
    dashboard = requests.get(
        "http://localhost:8002/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    with open("dashboard_response.json", "w") as f:
        if dashboard.status_code == 200:
            json.dump(dashboard.json(), f, indent=2)
            print("SUCCESS! Dashboard data saved to dashboard_response.json")
            print(f"Total Users: {dashboard.json().get('total_users')}")
            print(f"Total Practitioners: {dashboard.json().get('total_practitioners')}")
            print(f"Total Patients: {dashboard.json().get('total_patients')}")
        else:
            f.write(f"Error: {dashboard.status_code}\n{dashboard.text}")
            print(f"ERROR: {dashboard.status_code}")
else:
    print(f"Login failed: {response.status_code}")
