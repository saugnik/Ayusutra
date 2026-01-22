
import requests
import json
import time
import sys

# Configuration
BACKEND_URL = "http://localhost:8002"
LOGIN_EMAIL = "test_patient_gpu@ayursutra.com"
LOGIN_PASSWORD = "password123"

def login():
    """Login and return access token"""
    print(f"Logging in as {LOGIN_EMAIL}...")
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json={"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
        )
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("[PASS] Login successful")
            return token
        else:
            print(f"[FAIL] Login failed: {response.status_code} - {response.text}")
            sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Connection error: {e}")
        sys.exit(1)

def test_agent_capability(token, category, prompt, expected_intents):
    """
    Test a specific agent capability.
    expected_intents: list of action types expected (e.g., ['create_reminder', 'find_practitioner'])
    """
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"message": prompt}
    
    print(f"\n--- Testing Category: {category} ---")
    print(f"Prompt: '{prompt}'")
    
    start_time = time.time()
    try:
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
            
            print(f"[PASS] Response received in {duration:.2f}s")
            print(f"Actions Returned: {len(actions)}")
            
            # Verify Actions
            found_intents = [action.get('type') for action in actions]
            print(f"Action Types Found: {found_intents}")
            
            all_intents_matched = True
            for expected in expected_intents:
                if expected not in found_intents:
                    print(f"[FAIL] Missing expected action: {expected}")
                    all_intents_matched = False
            
            if all_intents_matched and expected_intents:
                print("[PASS] All expected actions present")
            elif not expected_intents and not actions:
                 print("[PASS] Correctly returned no actions for general query")

            # Check for content snippets (heuristic)
            print("\nResponse Preview:")
            try:
                preview = reply[:200] + "..." if len(reply) > 200 else reply
                print(f"  {preview.encode('ascii', 'replace').decode()}")
            except:
                print("  [Content could not be printed due to encoding]")
            
            # Detail the actions
            if actions:
                print("\nDetailed Actions:")
                for i, ax in enumerate(actions, 1):
                    try:
                        label = ax.get('label', '').encode('ascii', 'replace').decode()
                        print(f"  {i}. {label} ({ax.get('type')})")
                        if ax.get('data'):
                            print(f"     Data: {json.dumps(ax.get('data'))}")
                    except:
                         print(f"  {i}. [Action label encoding error]")

            return all_intents_matched
            
        else:
            print(f"[FAIL] Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"[FAIL] Exception: {e}")
        return False

def main():
    token = login()
    
    tests = [
        {
            "category": "Hydration Agent",
            "prompt": "I barely drank any water today, maybe just one glass.",
            "expected_intents": ["create_reminder"] 
        },
        {
            "category": "Weight Loss Agent (Timeline)",
            "prompt": "I am a 30 year old male, 180cm tall. I weigh 95kg and want to lose weight to reach 85kg.",
            "expected_intents": ["create_reminder", "find_practitioner"] # Expect workout/meal reminders + doctor fallback
        },
        {
            "category": "Medical Specialist Agent",
            "prompt": "I have been diagnosed with high blood pressure and need help.",
            "expected_intents": ["find_practitioner", "create_reminder"] # Cardiologist + Med reminder
        },
        {
             "category": "General Query (No Actions)",
             "prompt": "What are the benefits of Ashwagandha?",
             "expected_intents": []
        }
    ]
    
    passed = 0
    for t in tests:
        if test_agent_capability(token, t['category'], t['prompt'], t['expected_intents']):
            passed += 1
            
    print(f"\n\nTotal Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {len(tests) - passed}")

if __name__ == "__main__":
    main()
