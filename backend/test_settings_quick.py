import requests

def test_settings_api():
    # 1. Login as Admin
    login_url = "http://localhost:8001/auth/login"
    login_data = {"email": "admin@ayursutra.com", "password": "Admin@123"}
    
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code != 200:
            print(f"Login failed: {response.status_code} {response.text}")
            return
            
        token = response.json().get("access_token")
        print("Login successful.")
        
        # 2. Fetch Settings
        settings_url = "http://localhost:8001/admin/settings"
        headers = {"Authorization": f"Bearer {token}"}
        
        print(f"Fetching settings from {settings_url}...")
        resp = requests.get(settings_url, headers=headers)
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"Success! Retrieved {len(data)} settings.")
            for s in data:
                print(f"- {s.get('key')}: {s.get('value')}")
        else:
            print(f"Failed to fetch settings: {resp.status_code} {resp.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_settings_api()
