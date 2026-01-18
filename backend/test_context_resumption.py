import requests
import json
import sys

BASE_URL = "http://localhost:8001"

def test_flow():
    # 1. Register and Login to get token
    print("1. Registering/Logging in...")
    reg_data = {
        "email": "saugnikaich123@gmail.com",
        "full_name": "Saugnik Aich",
        "password": "12345",
        "role": "patient"
    }
    requests.post(f"{BASE_URL}/auth/register", json=reg_data) # Ignore error if exists
    
    login_payload = {
        "email": "saugnikaich123@gmail.com",
        "password": "12345"
    }
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

    # 2. Trigger Diet Plan (Expect Clarification)
    print("\n2. Requesting 'Give me a diet plan'...")
    payload1 = {
        "question": "Give me a diet plan",
        "context": {}
    }
    resp1 = requests.post(f"{BASE_URL}/health/ask-ai", json=payload1, headers=headers)
    data1 = resp1.json()
    conv_id = data1.get("conversation_id")
    answer1 = data1.get("answer", "")
    print(f"   Response: {answer1[:100]}...")
    
    if "age" not in answer1.lower() and "activity" not in answer1.lower():
        print("   [WARNING] Response did not ask for details. Logic might be already knowing the info?")
    else:
        print("   [SUCCESS] AI asked for clarification.")

    # 3. Provide Details (Expect Context Resumption -> Diet Plan)
    print("\n3. Providing 'My weight is 70kg, height is 170cm, age is 20, highly active'...")
    payload2 = {
        "question": "My weight is 70kg, height is 170cm, age is 20, and I am highly active",
        "context": {"conversation_id": conv_id}
    }
    resp2 = requests.post(f"{BASE_URL}/health/ask-ai", json=payload2, headers=headers)
    data2 = resp2.json()
    answer2 = data2.get("answer", "")
    
    print("\n------------------------------------------------")
    print("FINAL RESPONSE:")
    print(answer2) 
    print("------------------------------------------------")
    
    with open("test_result.txt", "w", encoding="utf-8") as f:
        f.write(f"--- RESPONSE 1 (Clarification) ---\n{answer1}\n\n")
        f.write(f"--- RESPONSE 2 (Plan) ---\n{answer2}\n")

    # Verification Logic
    if "BMI" in answer2 and "Macros" in answer2:
        print("\n[TEST PASSED] Diet Plan Generated Successfully! ✅")
    else:
        print("\n[TEST FAILED] Diet Plan NOT generated. ❌")
        # specific check
        if "suggested some actions" in answer2:
             print("   Reason: Fallback generic message received.")
        else:
             print("   Reason: Unknown response format.")

if __name__ == "__main__":
    test_flow()
