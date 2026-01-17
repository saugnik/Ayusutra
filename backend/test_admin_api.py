
import requests
import json

BASE_URL = "http://localhost:8001"
ADMIN_EMAIL = "admin@ayursutra.com"
ADMIN_PASSWORD = "Admin@123"

def test_admin_flow():
    print(f"Testing Admin Flow at {BASE_URL}...")
    
    # 1. Login as Admin
    print("\n1. Logging in as Admin...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        if response.status_code != 200:
            print(f"Failed to login: {response.text}")
            return
            
        data = response.json()
        token = data["access_token"]
        print(f"Login successful! Token: {token[:10]}...")
        headers = {"Authorization": f"Bearer {token}"}
    except Exception as e:
        print(f"Connection error: {e}")
        return

    # 2. Get Dashboard
    print("\n2. Fetching Admin Dashboard...")
    response = requests.get(f"{BASE_URL}/admin/dashboard", headers=headers)
    if response.status_code == 200:
        print("Dashboard stats:", json.dumps(response.json(), indent=2))
    else:
        print("Failed to get dashboard:", response.text)

    # 3. Get Users
    print("\n3. Fetching Users...")
    response = requests.get(f"{BASE_URL}/admin/users?limit=5", headers=headers)
    if response.status_code == 200:
        users = response.json()
        print(f"Found {len(users)} users.")
        if users:
            target_user = users[0]
            print(f"Target User for Impersonation: {target_user['email']} (ID: {target_user['id']})")
            
            # 4. Impersonate User
            print("\n4. Testing Impersonation...")
            imp_resp = requests.post(f"{BASE_URL}/admin/impersonate/{target_user['id']}", headers=headers)
            if imp_resp.status_code == 200:
                imp_data = imp_resp.json()
                print("Impersonation successful!")
                print("Impersonation Token:", imp_data["access_token"][:10] + "...")
            else:
                print("Impersonation failed:", imp_resp.text)
    else:
        print("Failed to get users:", response.text)

    # 5. Get Audit Logs
    print("\n5. Fetching Audit Logs...")
    response = requests.get(f"{BASE_URL}/admin/audit-logs", headers=headers)
    if response.status_code == 200:
        logs = response.json()
        print(f"Found {len(logs)} audit logs.")
        print(json.dumps(logs[:2], indent=2))
    else:
        print("Failed to get logs:", response.text)

if __name__ == "__main__":
    test_admin_flow()
