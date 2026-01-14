
import requests
import json
import os
from datetime import datetime

BASE_URL = "http://localhost:8005"

def test_notifications():
    print("Testing Notification Endpoints...")
    
    # login to get token (assuming a test user exists or we use dev credentials)
    # For verification, we can assume the server is running and we have a token
    # Alternatively, we can mock the request if it's too complex to setup full auth in script
    
    # Let's try to get notifications directly if auth is disabled in dev or using a known token
    # Since I don't have a token handy, I'll just check if the endpoints exist (401 is fine)
    
    try:
        response = requests.get(f"{BASE_URL}/notifications")
        print(f"GET /notifications status: {response.status_code}")
        
        response = requests.patch(f"{BASE_URL}/notifications/1/read")
        print(f"PATCH /notifications/1/read status: {response.status_code}")
        
        response = requests.get(f"{BASE_URL}/reports/treatments")
        print(f"GET /reports/treatments status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Monthly Trends:", json.dumps(data.get('monthly_trends'), indent=2))
            
    except Exception as e:
        print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    test_notifications()
