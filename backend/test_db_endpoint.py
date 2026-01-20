
import requests
import json

try:
    print("Testing connection to http://localhost:8002/debug/db-data...")
    response = requests.get("http://localhost:8002/debug/db-data", timeout=5)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Success! Data received:")
        print(json.dumps(data, indent=2)[:500] + "...")
    else:
        print("Failed!")
        with open("backend/debug_output.txt", "w") as f:
            f.write(response.text)
        print("Error details saved to backend/debug_output.txt")

except Exception as e:
    print(f"Connection Error: {e}")
