import requests
import sys

URL = "http://localhost:8001/debug/db-data"

try:
    print(f"Testing GET {URL}...")
    response = requests.get(URL)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Success!")
        print(response.json())
    else:
        print("Failed!")
        print(response.text)
except Exception as e:
    print(f"Connection Error: {e}")
