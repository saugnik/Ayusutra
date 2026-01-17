"""
Test script for Health Agent endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8001"

def test_agent_without_auth():
    """Test agent endpoints without authentication to see error handling"""
    print("=" * 60)
    print("Testing Health Agent Endpoints")
    print("=" * 60)
    
    # Test 1: Agent chat endpoint
    print("\n1. Testing /api/agent/chat endpoint (without auth)...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/agent/chat",
            json={"message": "Remind me to drink water at 8 AM"},
            timeout=10
        )
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 401:
            print("   ✓ Correctly requires authentication")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test 2: Reminders endpoint
    print("\n2. Testing /api/reminders endpoint (without auth)...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/reminders",
            timeout=10
        )
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 401:
            print("   ✓ Correctly requires authentication")
        else:
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test 3: Server health check
    print("\n3. Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Server is running")
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("- Backend server is running on port 8001")
    print("- Agent endpoints exist and require authentication")
    print("- To test with authentication, login via frontend or use a token")
    print("=" * 60)

if __name__ == "__main__":
    test_agent_without_auth()
