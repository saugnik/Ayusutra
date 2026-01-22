import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8002"
LOGIN_EMAIL = "test_patient_gpu@ayursutra.com"
LOGIN_PASSWORD = "password123"

def login():
    """Login and return access token"""
    print(f"Logging in as {LOGIN_EMAIL}...")
    response = requests.post(
        f"{BACKEND_URL}/auth/login",
        json={"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    )
    if response.status_code == 200:
        token = response.json().get('access_token')
        print("[PASS] Login successful\n")
        return token
    else:
        print(f"[FAIL] Login failed: {response.status_code}")
        return None

def test_chatbot(token, test_name, message, expected_features):
    """Test chatbot with specific message and verify expected features"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    print(f"Message: '{message}'")
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": message}
    
    start_time = time.time()
    response = requests.post(
        f"{BACKEND_URL}/chat/ai-assistant",
        json=payload,
        headers=headers
    )
    duration = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        reply = data.get('reply', '')
        actions = data.get('actions', [])
        
        print(f"\n[PASS] Response received in {duration:.2f}s")
        print(f"\nReply Preview (first 300 chars):")
        print("-" * 60)
        print(reply[:300] + ("..." if len(reply) > 300 else ""))
        print("-" * 60)
        
        print(f"\nActions Returned: {len(actions)}")
        for i, action in enumerate(actions, 1):
            print(f"  {i}. {action.get('label')} ({action.get('type')})")
        
        # Verify expected features
        print(f"\nVerification:")
        passed = 0
        for feature, check in expected_features.items():
            if check(reply, actions):
                print(f"  [PASS] {feature}")
                passed += 1
            else:
                print(f"  [FAIL] {feature}")
        
        print(f"\nResult: {passed}/{len(expected_features)} checks passed")
        return passed == len(expected_features)
    else:
        print(f"[FAIL] Error: {response.status_code} - {response.text}")
        return False

def main():
    token = login()
    if not token:
        return
    
    tests = [
        {
            "name": "No Clarification on General Query",
            "message": "What are the benefits of yoga?",
            "expected": {
                "No clarification questions": lambda r, a: "What is your" not in r and "age" not in r.lower(),
                "Has meaningful response": lambda r, a: len(r) > 50
            }
        },
        {
            "name": "Disease Detection - Fever",
            "message": "I have a fever and feeling very hot",
            "expected": {
                "Immediate action mentioned": lambda r, a: "immediate" in r.lower() or "rest" in r.lower(),
                "Ayurvedic remedy mentioned": lambda r, a: "tulsi" in r.lower() or "ginger" in r.lower(),
                "Doctor action suggested": lambda r, a: any(a.get('type') == 'find_practitioner' for a in a)
            }
        },
        {
            "name": "Disease Detection - Chest Pain (Emergency)",
            "message": "I'm experiencing severe chest pain",
            "expected": {
                "Emergency warning": lambda r, a: "emergency" in r.lower() or "urgent" in r.lower(),
                "Cardiologist recommended": lambda r, a: "cardiologist" in r.lower(),
                "Urgent action": lambda r, a: any(a.get('data', {}).get('urgent') for a in a)
            }
        },
        {
            "name": "Diet Plan with Full Content",
            "message": "Give me a diet plan",
            "expected": {
                "Shows calories": lambda r, a: "calor" in r.lower() and "kcal" in r.lower(),
                "Shows meal plan": lambda r, a: "breakfast" in r.lower() and "lunch" in r.lower(),
                "Has meal reminders": lambda r, a: any("meal" in a.get('label', '').lower() for a in a)
            }
        },
        {
            "name": "Workout Plan with Full Content",
            "message": "Create a workout plan for me",
            "expected": {
                "Shows weekly schedule": lambda r, a: "monday" in r.lower() or "weekly" in r.lower(),
                "Shows exercises": lambda r, a: len(r) > 200,  # Should have substantial content
                "Has workout reminders": lambda r, a: any("workout" in a.get('label', '').lower() for a in a)
            }
        },
        {
            "name": "Diabetes Management",
            "message": "I have diabetes and need help managing it",
            "expected": {
                "Immediate advice": lambda r, a: "blood sugar" in r.lower() or "monitor" in r.lower(),
                "Ayurvedic remedy": lambda r, a: "bitter gourd" in r.lower() or "fenugreek" in r.lower(),
                "Endocrinologist suggested": lambda r, a: "endocrinologist" in r.lower(),
                "Medication reminder": lambda r, a: any("medication" in a.get('label', '').lower() for a in a)
            }
        }
    ]
    
    print("\n" + "="*60)
    print("CHATBOT AGENT BEHAVIOR VERIFICATION")
    print("="*60)
    
    passed_tests = 0
    for test in tests:
        if test_chatbot(token, test['name'], test['message'], test['expected']):
            passed_tests += 1
        time.sleep(2)  # Brief pause between tests
    
    print("\n" + "="*60)
    print(f"FINAL RESULTS: {passed_tests}/{len(tests)} tests passed")
    print("="*60)

if __name__ == "__main__":
    main()
