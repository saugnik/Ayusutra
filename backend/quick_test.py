import requests

print("Quick Backend Test")
print("=" * 50)

# Test if backend is running
try:
    response = requests.get("http://localhost:8001/")
    print(f"✓ Backend is running!")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
except Exception as e:
    print(f"✗ Backend is NOT running!")
    print(f"  Error: {e}")
    print("\nPlease start the backend with: python main.py")
