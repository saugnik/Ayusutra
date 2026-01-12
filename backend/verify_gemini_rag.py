import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    print("Checking health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"✅ Service is healthy: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to service: {e}")
        return False

def test_ask(question):
    print(f"\nAsking question: '{question}'")
    payload = {
        "query": question,
        "top_k": 3
    }
    try:
        response = requests.post(f"{BASE_URL}/ask", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Response received!")
            print(f"Answer: {data['answer']['text'][:150]}...")
            print(f"Confidence: {data['answer']['confidence']}")
            print(f"Evidence: {data['answer']['evidence']}")
        else:
            print(f"❌ Request failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error during request: {e}")

if __name__ == "__main__":
    # Wait for service to start if running immediately after launch
    print("Waiting for service to be ready...")
    for i in range(5):
        if test_health():
            break
        time.sleep(2)
    else:
        print("Service did not start in time.")
        exit(1)
        
    test_ask("What are the benefits of Abhyanga?")
