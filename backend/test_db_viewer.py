import requests
import sys

URL = "http://localhost:8001/db-view"

try:
    print(f"Testing GET {URL}...")
    response = requests.get(URL)
    print(f"Status Code: {response.status_code}")
    print("Response Body:", response.text)
except Exception as e:
    print(f"Connection Error: {e}")

# print("-" * 20)
# try:
#     print("Testing GET http://localhost:8001/health ...")
#     r = requests.get("http://localhost:8001/health")
#     print(f"Status: {r.status_code}")
#     print("Response:", r.text[:100])
# except Exception as e:
#     print(f"Health Check Failed: {e}")
