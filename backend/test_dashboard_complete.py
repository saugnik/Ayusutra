"""
Direct test to see what the frontend would receive from the dashboard endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8002"

print("=" * 70)
print("TESTING ADMIN DASHBOARD ENDPOINT")
print("=" * 70)

# Step 1: Login to get a valid token
print("\n1. Logging in as admin...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "admin_new@ayursutra.com", "password": "password123"}
)

if login_response.status_code != 200:
    print(f"   ❌ Login failed: {login_response.status_code}")
    print(f"   Response: {login_response.text}")
    print("\n   Trying to register first...")
    
    register_response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "full_name": "Admin User",
            "email": "admin_new@ayursutra.com",
            "password": "password123",
            "phone": "9876543210",
            "role": "admin"
        }
    )
    
    if register_response.status_code == 200:
        print("   ✅ Registration successful, logging in again...")
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": "admin_new@ayursutra.com", "password": "password123"}
        )
    else:
        print(f"   ❌ Registration failed: {register_response.text}")
        exit(1)

if login_response.status_code == 200:
    token_data = login_response.json()
    access_token = token_data['access_token']
    print(f"   ✅ Login successful!")
    print(f"   User ID: {token_data.get('user_id')}")
    print(f"   Role: {token_data.get('role')}")
    print(f"   Token: {access_token[:30]}...")
else:
    print(f"   ❌ Login failed: {login_response.text}")
    exit(1)

# Step 2: Call dashboard endpoint
print("\n2. Calling /admin/dashboard endpoint...")
dashboard_response = requests.get(
    f"{BASE_URL}/admin/dashboard",
    headers={"Authorization": f"Bearer {access_token}"}
)

print(f"   Status Code: {dashboard_response.status_code}")

if dashboard_response.status_code == 200:
    data = dashboard_response.json()
    print(f"\n   ✅ SUCCESS! Dashboard data received:")
    print(f"   " + "-" * 60)
    print(json.dumps(data, indent=6))
    print(f"   " + "-" * 60)
    
    # Highlight the key fields
    print(f"\n   📊 KEY STATS:")
    print(f"   - Total Users: {data.get('total_users', 'MISSING')}")
    print(f"   - Total Practitioners: {data.get('total_practitioners', 'MISSING')}")
    print(f"   - Total Patients: {data.get('total_patients', 'MISSING')}")
    print(f"   - Total Appointments: {data.get('total_appointments', 'MISSING')}")
    print(f"   - Recent Registrations: {data.get('recent_registrations', 'MISSING')}")
    
    if data.get('total_users', 0) == 0:
        print(f"\n   ⚠️  WARNING: Backend is returning 0 users!")
        print(f"   This means the database queries in the backend are failing.")
    else:
        print(f"\n   ✅ Backend is returning correct data!")
        print(f"   The issue must be in the frontend display logic.")
        
elif dashboard_response.status_code == 403:
    print(f"   ❌ 403 Forbidden - Authentication issue")
    print(f"   Response: {dashboard_response.text}")
    print(f"\n   The token might not have admin privileges.")
else:
    print(f"   ❌ Error: {dashboard_response.status_code}")
    print(f"   Response: {dashboard_response.text}")

print("\n" + "=" * 70)
print("FRONTEND DEBUGGING STEPS:")
print("=" * 70)
print("""
If backend returns correct data but frontend shows 0:

1. Open browser console (F12) and look for:
   - [DEBUG] messages showing the fetch request
   - Any CORS errors
   - Any JavaScript errors

2. Check localStorage in browser console:
   localStorage.getItem('token')
   localStorage.getItem('access_token')

3. Manually test the API in browser console:
   fetch('http://localhost:8002/admin/dashboard', {
     headers: {'Authorization': 'Bearer ' + localStorage.getItem('token')}
   }).then(r => r.json()).then(console.log)

4. If data is received but not displayed, the issue is in React state management.
""")
print("=" * 70)
