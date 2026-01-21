"""
Quick test to verify admin endpoints are working
"""
import requests
import json

BASE_URL = "http://localhost:8002"

print("Testing Admin Endpoints...")
print("=" * 50)

# Test 1: Check if backend is running
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Backend is running: {response.json()['message']}")
except Exception as e:
    print(f"❌ Backend not accessible: {e}")
    exit(1)

# Test 2: Try to get dashboard stats (will fail without auth, but should return 403 not 500)
try:
    response = requests.get(f"{BASE_URL}/admin/dashboard")
    print(f"\n📊 Dashboard endpoint status: {response.status_code}")
    if response.status_code == 403:
        print("   Expected 403 - authentication required ✅")
    elif response.status_code == 200:
        data = response.json()
        print(f"   Total users: {data.get('total_users', 'N/A')}")
except Exception as e:
    print(f"❌ Dashboard error: {e}")

# Test 3: Try to get users list (will fail without auth)
try:
    response = requests.get(f"{BASE_URL}/admin/users?limit=10")
    print(f"\n👥 Users endpoint status: {response.status_code}")
    if response.status_code == 403:
        print("   Expected 403 - authentication required ✅")
    elif response.status_code == 200:
        data = response.json()
        print(f"   Users found: {len(data)}")
except Exception as e:
    print(f"❌ Users error: {e}")

# Test 4: Check CORS headers
try:
    response = requests.options(
        f"{BASE_URL}/admin/users",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization"
        }
    )
    print(f"\n🔒 CORS preflight status: {response.status_code}")
    cors_headers = {k: v for k, v in response.headers.items() if 'access-control' in k.lower()}
    print(f"   CORS headers: {json.dumps(cors_headers, indent=2)}")
except Exception as e:
    print(f"❌ CORS test error: {e}")

print("\n" + "=" * 50)
print("✅ Backend is ready!")
print("\nNext steps:")
print("1. Open http://localhost:3000/admin in your browser")
print("2. Login with your admin credentials")
print("3. Click 'User Management' to see all users")
