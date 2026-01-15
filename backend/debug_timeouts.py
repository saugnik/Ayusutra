
import requests
import time

BASE_URL = "http://localhost:8001"
TIMEOUT = 5

def test_endpoint(name, url, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    print(f"\nTesting {name} ({url})...")
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}{url}", headers=headers, timeout=TIMEOUT)
        elapsed = time.time() - start
        print(f"Status: {response.status_code}")
        print(f"Time: {elapsed:.2f}s")
        if response.status_code == 200:
            print("✅ Success")
        else:
            print(f"❌ Failed: {response.text[:200]}")
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT (Backend not responding in time)")
    except Exception as e:
        print(f"❌ ERROR: {e}")

# Login as practitioner to get token
def get_practitioner_token():
    print("Logging in as practitioner...")
    try:
        # Try a known practitioner or create one
        # Let's try to register/login a temporary one to be safe
        email = f"debug_timeout_{int(time.time())}@test.com"
        data = {
            "email": email,
            "password": "password123",
            "full_name": "Debug Practitioner",
            "role": "practitioner",
            "phone": "1234567890"
        }
        r = requests.post(f"{BASE_URL}/auth/register", json=data)
        if r.status_code != 200:
             r = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": "password123"})
        
        return r.json().get("access_token")
    except Exception as e:
        print(f"Login failed: {e}")
        try:
             # Fallback to hardcoded known user if registration fails
             r = requests.post(f"{BASE_URL}/auth/login", json={"email": "practitioner_flow_1736913456@test.com", "password": "password123"})
             if r.status_code == 200:
                 return r.json().get("access_token")
        except:
             pass
        return None

if __name__ == "__main__":
    # 1. Check Root
    test_endpoint("Root", "")
    
    # 2. Get Token
    token = get_practitioner_token()
    
    if token:
        # 3. Test the failing endpoints
        test_endpoint("Treatment Analytics", "/reports/treatments", token)
        test_endpoint("Monthly Summary", "/reports/monthly-summary", token)
        test_endpoint("Feedback Report", "/reports/feedback", token)
    else:
        print("Skipping authenticated tests due to login failure.")
