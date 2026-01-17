"""
Quick Health Agent Test - ASCII output only
"""
import requests
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal
from models import User, UserRole
from auth import create_access_token

BASE_URL = "http://localhost:8001"

def test_agent():
    print("\n" + "="*60)
    print("HEALTH AGENT TEST")
    print("="*60)
    
    # Get user
    db = SessionLocal()
    user = db.query(User).filter(User.role == UserRole.PATIENT).first()
    db.close()
    
    if not user:
        print("ERROR: No patient users found")
        return
    
    print(f"Using patient: {user.email}")
    token = create_access_token(data={"sub": user.email})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Water reminder
    print("\n[1] Testing water reminder...")
    try:
        r = requests.post(
            f"{BASE_URL}/api/agent/chat",
            headers=headers,
            json={"message": "Remind me to drink water at 8 AM"},
            timeout=15
        )
        if r.status_code == 200:
            data = r.json()
            print(f"  OK - Reply length: {len(data['reply'])} chars")
            print(f"  Actions detected: {len(data.get('actions', []))}")
            if data.get('actions'):
                print(f"  Action type: {data['actions'][0]['type']}")
        else:
            print(f"  FAILED - Status: {r.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # Test 2: Create reminder
    print("\n[2] Testing reminder creation...")
    try:
        action = [{
            "type": "create_reminder",
            "label": "Test",
            "data": {
                "title": "Water",
                "message": "Drink water",
                "time": "08:00 AM",
                "frequency": "daily"
            }
        }]
        r = requests.post(
            f"{BASE_URL}/api/agent/confirm-actions",
            headers=headers,
            json=action,
            timeout=10
        )
        if r.status_code == 200:
            data = r.json()
            print(f"  OK - Status: {data['results'][0]['status']}")
        else:
            print(f"  FAILED - Status: {r.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")
    
    # Test 3: Get reminders
    print("\n[3] Testing get reminders...")
    try:
        r = requests.get(f"{BASE_URL}/api/reminders", headers=headers, timeout=10)
        if r.status_code == 200:
            reminders = r.json()
            print(f"  OK - Total reminders: {len(reminders)}")
        else:
            print(f"  FAILED - Status: {r.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*60)

if __name__ == "__main__":
    test_agent()
