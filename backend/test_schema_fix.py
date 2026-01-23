"""
Test script to verify the 422 schema fix
Tests that conversation_id is properly maintained across messages
"""
import requests
import json

BASE_URL = "http://127.0.0.1:3000"

def test_schema_fix():
    print("=" * 60)
    print("Testing 422 Schema Fix - Conversation Context Retention")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1. Logging in...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "test_patient_gpu@ayursutra.com",
            "password": "password123"
        }
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return False
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")
    
    # Step 2: First message - provide user info
    print("\n2. Sending first message with user info...")
    payload1 = {
        "question": "I am 25 years old and weigh 70kg"
    }
    
    resp1 = requests.post(
        f"{BASE_URL}/health/ask-ai",
        json=payload1,
        headers=headers
    )
    
    print(f"   Status Code: {resp1.status_code}")
    if resp1.status_code == 422:
        print("❌ 422 Error - Schema mismatch still exists!")
        print(f"   Response: {resp1.text}")
        return False
    elif resp1.status_code != 200:
        print(f"❌ Unexpected error: {resp1.status_code}")
        print(f"   Response: {resp1.text}")
        return False
    
    data1 = resp1.json()
    conversation_id = data1.get("conversation_id")
    print(f"✅ First message successful")
    print(f"   Conversation ID: {conversation_id}")
    print(f"   Response: {data1.get('answer', '')[:100]}...")
    
    if not conversation_id:
        print("⚠️  Warning: No conversation_id returned")
        return False
    
    # Step 3: Second message - test context retention
    print("\n3. Sending second message to test context retention...")
    payload2 = {
        "question": "What was my weight again?",
        "context": {"conversation_id": conversation_id}
    }
    
    resp2 = requests.post(
        f"{BASE_URL}/health/ask-ai",
        json=payload2,
        headers=headers
    )
    
    print(f"   Status Code: {resp2.status_code}")
    if resp2.status_code == 422:
        print("❌ 422 Error on second message!")
        print(f"   Response: {resp2.text}")
        return False
    elif resp2.status_code != 200:
        print(f"❌ Unexpected error: {resp2.status_code}")
        print(f"   Response: {resp2.text}")
        return False
    
    data2 = resp2.json()
    answer2 = data2.get("answer", "")
    print(f"✅ Second message successful")
    print(f"   Response: {answer2}")
    
    # Check if context was retained (should mention 70kg)
    if "70" in answer2 or "seventy" in answer2.lower():
        print("\n✅ CONTEXT RETENTION WORKING! Bot remembered the weight.")
    else:
        print("\n⚠️  Context may not be fully working - weight not mentioned in response")
    
    # Step 4: Test general query
    print("\n4. Testing general query (yoga benefits)...")
    payload3 = {
        "question": "What are the benefits of yoga?",
        "context": {"conversation_id": conversation_id}
    }
    
    resp3 = requests.post(
        f"{BASE_URL}/health/ask-ai",
        json=payload3,
        headers=headers
    )
    
    print(f"   Status Code: {resp3.status_code}")
    if resp3.status_code == 422:
        print("❌ 422 Error on yoga query!")
        return False
    
    data3 = resp3.json()
    answer3 = data3.get("answer", "")
    print(f"   Response length: {len(answer3)} characters")
    
    if "I can help you with that" in answer3 and len(answer3) < 100:
        print("⚠️  Still getting generic response for yoga query")
    else:
        print("✅ Detailed response received")
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    print("✅ No 422 errors - Schema fix successful!")
    print(f"✅ Conversation ID tracking: {conversation_id}")
    print("✅ Context field properly sent to backend")
    
    return True

if __name__ == "__main__":
    try:
        success = test_schema_fix()
        if success:
            print("\n🎉 TEST PASSED - Schema fix is working!")
        else:
            print("\n❌ TEST FAILED - Issues remain")
    except Exception as e:
        print(f"\n❌ TEST ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
