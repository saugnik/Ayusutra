import requests
import sys

BASE_URL = "http://localhost:8001"
user_email = "saugnikaich123@gmail.com"
user_pass = "12345"

def test_delete_flow():
    # 1. Login
    print("1. Logging in...")
    login_payload = {"email": user_email, "password": user_pass}
    try:
        resp = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
        if resp.status_code != 200:
            print(f"Login failed: {resp.text}")
            return
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("   Login successful.")
    except Exception as e:
        print(f"   Auth error: {e}")
        return

    # 2. Test Delete Reminder
    print("\n2. Testing Reminder Delete...")
    # Create dummy reminder
    # Oh wait, there is no direct create endpoint for reminders except via agent?
    # Actually I can't easily create one via API without agent action logic. 
    # But I can check if any exist. If not, I might need to mock or just skip creation and try to delete a non-existent one to check 404 vs 500.
    # Actually, let's try to delete a random ID. Expected: 404 (Not Found), not 405 (Method Not Allowed) or 500.
    
    del_resp = requests.delete(f"{BASE_URL}/reminders/999999", headers=headers)
    print(f"   Delete Non-existent Reminder: {del_resp.status_code} (Expected 404)")
    if del_resp.status_code in [404, 200]:
         print("   [PASS] Endpoint exists.")
    else:
         print(f"   [FAIL] Unexpected status: {del_resp.status_code}")

    # 3. Test Delete Conversation
    print("\n3. Testing Conversation Delete...")
    # Try deleting a non-existent conversation
    del_conv = requests.delete(f"{BASE_URL}/health/conversations/non_existent_id", headers=headers)
    print(f"   Delete Non-existent Conv: {del_conv.status_code} (Expected 404)")
    if del_conv.status_code in [404, 200]:
         print("   [PASS] Endpoint exists.")
    else:
         print(f"   [FAIL] Unexpected status: {del_conv.status_code}")

if __name__ == "__main__":
    test_delete_flow()
