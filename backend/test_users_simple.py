import requests

# Test users endpoint
response = requests.post(
    "http://localhost:8002/auth/login",
    json={"email": "admin_new@ayursutra.com", "password": "password123"}
)

print(f"Login status: {response.status_code}")

if response.status_code == 200:
    token = response.json()['access_token']
    
    # Test users endpoint
    users = requests.get(
        "http://localhost:8002/admin/users?limit=100",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Users endpoint status: {users.status_code}")
    print(f"Response: {users.text[:500]}")
else:
    print(f"Login failed: {response.text}")
