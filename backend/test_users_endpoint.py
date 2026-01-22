import requests
import json

# Test users endpoint
response = requests.post(
    "http://localhost:8002/auth/login",
    json={"email": "admin_new@ayursutra.com", "password": "password123"}
)

if response.status_code == 200:
    token = response.json()['access_token']
    print(f"Login successful! Token: {token[:30]}...")
    
    # Test users endpoint
    users = requests.get(
        "http://localhost:8002/admin/users?limit=100",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"\nUsers endpoint status: {users.status_code}")
    
    if users.status_code == 200:
        users_data = users.json()
        print(f"SUCCESS! Found {len(users_data)} users")
        print(f"\nFirst 5 users:")
        for user in users_data[:5]:
            print(f"  - {user.get('full_name')} ({user.get('email')}) - Role: {user.get('role')}")
        
        # Save to file
        with open("users_response.json", "w") as f:
            json.dump(users_data, f, indent=2)
        print(f"\nFull user list saved to users_response.json")
    else:
        print(f"ERROR: {users.status_code}")
        print(f"Response: {users.text}")
else:
    print(f"Login failed: {response.status_code}")
    print(f"Response: {response.text}")
