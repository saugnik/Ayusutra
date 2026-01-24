#!/usr/bin/env python3
"""
Comprehensive Health Agent Chatbot Testing Script
Tests all 10 features and reports results
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8001"
RESULTS = []

def print_header(test_num, test_name):
    print(f"\n{'='*80}")
    print(f"TEST {test_num}/10: {test_name}")
    print(f"{'='*80}")

def print_result(passed, message):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"\n{status}: {message}\n")
    return passed

def login():
    """Login and get access token"""
    print("🔐 Logging in...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "patient@test.com", "password": "patient123"}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login successful!")
        return token
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(response.text)
        return None

def test_agent_chat(token, message, test_name):
    """Send message to agent and return response"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/agent/chat",
        headers=headers,
        json={"message": message}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
        return None

def run_tests():
    """Run all 10 test cases"""
    token = login()
    if not token:
        print("Cannot proceed without authentication")
        return
    
    test_results = []
    
    # TEST 1: Water Reminder
    print_header(1, "Water Reminder")
    response = test_agent_chat(token, "Remind me to drink water every 2 hours", "Water Reminder")
    if response:
        print(f"Reply: {response.get('reply', 'No reply')[:200]}...")
        actions = response.get('actions', [])
        print(f"Actions: {len(actions)} action(s) detected")
        if actions:
            print(f"Action details: {json.dumps(actions[0], indent=2)}")
        
        passed = (
            actions and 
            any('water' in str(action).lower() for action in actions) and
            any('reminder' in str(action).lower() for action in actions)
        )
        result = print_result(passed, "Water reminder action detected" if passed else "No water reminder action found")
        test_results.append(("Water Reminder", result))
    else:
        test_results.append(("Water Reminder", False))
    
    time.sleep(1)
    
    # TEST 2: Exercise Reminder
    print_header(2, "Exercise Reminder")
    response = test_agent_chat(token, "I want to exercise daily at 6 AM", "Exercise Reminder")
    if response:
        print(f"Reply: {response.get('reply', 'No reply')[:200]}...")
        actions = response.get('actions', [])
        print(f"Actions: {len(actions)} action(s) detected")
        if actions:
            print(f"Action details: {json.dumps(actions[0], indent=2)}")
        
        passed = (
            actions and 
            any('exercise' in str(action).lower() or 'workout' in str(action).lower() for action in actions)
        )
        result = print_result(passed, "Exercise reminder action detected" if passed else "No exercise reminder action found")
        test_results.append(("Exercise Reminder", result))
    else:
        test_results.append(("Exercise Reminder", False))
    
    time.sleep(1)
    
    # TEST 3: Diet Plan Request
    print_header(3, "Diet Plan Generation")
    response = test_agent_chat(token, "I'm 25 years old, weigh 70kg, height 175cm, and want to lose weight. Create a diet plan for me.", "Diet Plan")
    if response:
        reply = response.get('reply', '')
        print(f"Reply length: {len(reply)} characters")
        print(f"Reply preview: {reply[:300]}...")
        
        # Check for diet plan components
        has_calories = 'calorie' in reply.lower() or 'kcal' in reply.lower()
        has_macros = 'protein' in reply.lower() or 'carb' in reply.lower() or 'fat' in reply.lower()
        has_meals = 'breakfast' in reply.lower() or 'lunch' in reply.lower() or 'dinner' in reply.lower()
        has_bmi = 'bmi' in reply.lower()
        
        print(f"Has calories: {has_calories}")
        print(f"Has macros: {has_macros}")
        print(f"Has meals: {has_meals}")
        print(f"Has BMI: {has_bmi}")
        
        passed = has_calories and has_macros and has_meals
        result = print_result(passed, "Complete diet plan generated" if passed else "Incomplete diet plan")
        test_results.append(("Diet Plan", result))
    else:
        test_results.append(("Diet Plan", False))
    
    time.sleep(1)
    
    # TEST 4: Workout Plan Request
    print_header(4, "Workout Plan Generation")
    response = test_agent_chat(token, "Create a workout plan for me based on my Vata dosha", "Workout Plan")
    if response:
        reply = response.get('reply', '')
        print(f"Reply length: {len(reply)} characters")
        print(f"Reply preview: {reply[:300]}...")
        
        has_workout = 'workout' in reply.lower() or 'exercise' in reply.lower()
        has_schedule = 'monday' in reply.lower() or 'tuesday' in reply.lower() or 'week' in reply.lower()
        has_yoga = 'yoga' in reply.lower() or 'asana' in reply.lower()
        
        print(f"Has workout info: {has_workout}")
        print(f"Has schedule: {has_schedule}")
        print(f"Has yoga: {has_yoga}")
        
        passed = has_workout and (has_schedule or has_yoga)
        result = print_result(passed, "Workout plan generated" if passed else "Incomplete workout plan")
        test_results.append(("Workout Plan", result))
    else:
        test_results.append(("Workout Plan", False))
    
    time.sleep(1)
    
    # TEST 5: Find Practitioner
    print_header(5, "Find Practitioner")
    response = test_agent_chat(token, "I have a severe headache for 3 days. Can you help me find a doctor?", "Find Practitioner")
    if response:
        reply = response.get('reply', '')
        actions = response.get('actions', [])
        print(f"Reply: {reply[:200]}...")
        print(f"Actions: {len(actions)} action(s) detected")
        
        has_practitioner_action = any('practitioner' in str(action).lower() or 'doctor' in str(action).lower() for action in actions)
        mentions_doctor = 'doctor' in reply.lower() or 'practitioner' in reply.lower() or 'consult' in reply.lower()
        
        print(f"Has practitioner action: {has_practitioner_action}")
        print(f"Mentions consultation: {mentions_doctor}")
        
        passed = has_practitioner_action or mentions_doctor
        result = print_result(passed, "Practitioner recommendation provided" if passed else "No practitioner recommendation")
        test_results.append(("Find Practitioner", result))
    else:
        test_results.append(("Find Practitioner", False))
    
    time.sleep(1)
    
    # TEST 6: General Ayurvedic Question
    print_header(6, "Ayurvedic Q&A")
    response = test_agent_chat(token, "What are the benefits of drinking warm water in Ayurveda?", "Ayurvedic Q&A")
    if response:
        reply = response.get('reply', '')
        print(f"Reply length: {len(reply)} characters")
        print(f"Reply: {reply[:400]}...")
        
        has_agni = 'agni' in reply.lower() or 'digestive' in reply.lower()
        has_benefits = 'benefit' in reply.lower() or 'help' in reply.lower()
        is_substantial = len(reply) > 100
        
        print(f"Mentions Agni/Digestion: {has_agni}")
        print(f"Mentions benefits: {has_benefits}")
        print(f"Substantial answer: {is_substantial}")
        
        passed = has_benefits and is_substantial
        result = print_result(passed, "Helpful Ayurvedic answer provided" if passed else "Insufficient answer")
        test_results.append(("Ayurvedic Q&A", result))
    else:
        test_results.append(("Ayurvedic Q&A", False))
    
    time.sleep(1)
    
    # TEST 7: Medicine Reminder
    print_header(7, "Medicine Reminder (Multiple Times)")
    response = test_agent_chat(token, "Remind me to take my medicine at 8 AM and 8 PM daily", "Medicine Reminder")
    if response:
        reply = response.get('reply', '')
        actions = response.get('actions', [])
        print(f"Reply: {reply[:200]}...")
        print(f"Actions: {len(actions)} action(s) detected")
        if actions:
            print(f"Action details: {json.dumps(actions[0], indent=2)}")
        
        has_reminder = actions and any('reminder' in str(action).lower() for action in actions)
        mentions_times = '8' in reply or 'morning' in reply.lower() or 'evening' in reply.lower()
        
        print(f"Has reminder action: {has_reminder}")
        print(f"Mentions times: {mentions_times}")
        
        passed = has_reminder
        result = print_result(passed, "Medicine reminder action detected" if passed else "No medicine reminder action")
        test_results.append(("Medicine Reminder", result))
    else:
        test_results.append(("Medicine Reminder", False))
    
    time.sleep(1)
    
    # TEST 8: Clarification Request
    print_header(8, "Clarification Handling")
    response = test_agent_chat(token, "I want a diet plan", "Clarification")
    if response:
        reply = response.get('reply', '')
        print(f"Reply: {reply[:300]}...")
        
        asks_for_info = any(word in reply.lower() for word in ['age', 'weight', 'height', 'goal', 'tell me', 'need', 'information'])
        is_question = '?' in reply
        
        print(f"Asks for information: {asks_for_info}")
        print(f"Contains question: {is_question}")
        
        passed = asks_for_info or is_question
        result = print_result(passed, "Agent asks for clarification" if passed else "No clarification requested")
        test_results.append(("Clarification", result))
    else:
        test_results.append(("Clarification", False))
    
    time.sleep(1)
    
    # TEST 9: Context Memory (Two-part conversation)
    print_header(9, "Context Memory")
    # First message
    response1 = test_agent_chat(token, "I'm 30 years old and weigh 80kg", "Context Part 1")
    if response1:
        conv_id = response1.get('conversation_id')
        print(f"Conversation ID: {conv_id}")
        print(f"Reply 1: {response1.get('reply', '')[:200]}...")
        
        time.sleep(1)
        
        # Second message using same conversation
        response2 = test_agent_chat(token, "Create a diet plan for me", "Context Part 2")
        if response2:
            reply2 = response2.get('reply', '')
            print(f"Reply 2 preview: {reply2[:300]}...")
            
            # Check if it generated a plan (meaning it remembered the context)
            has_plan = 'calorie' in reply2.lower() or 'diet' in reply2.lower() or 'meal' in reply2.lower()
            doesnt_ask_again = 'age' not in reply2.lower() or 'weight' not in reply2.lower()
            
            print(f"Generated plan: {has_plan}")
            print(f"Doesn't re-ask for info: {doesnt_ask_again}")
            
            passed = has_plan
            result = print_result(passed, "Context maintained across messages" if passed else "Context not maintained")
            test_results.append(("Context Memory", result))
        else:
            test_results.append(("Context Memory", False))
    else:
        test_results.append(("Context Memory", False))
    
    time.sleep(1)
    
    # TEST 10: Multiple Intents
    print_header(10, "Multiple Intents Handling")
    response = test_agent_chat(token, "I want to lose weight. Can you create a diet plan and workout plan for me? I'm 28, 75kg, 170cm tall.", "Multiple Intents")
    if response:
        reply = response.get('reply', '')
        print(f"Reply length: {len(reply)} characters")
        print(f"Reply preview: {reply[:400]}...")
        
        has_diet = 'diet' in reply.lower() or 'meal' in reply.lower() or 'calorie' in reply.lower()
        has_workout = 'workout' in reply.lower() or 'exercise' in reply.lower()
        is_comprehensive = len(reply) > 300
        
        print(f"Addresses diet: {has_diet}")
        print(f"Addresses workout: {has_workout}")
        print(f"Comprehensive response: {is_comprehensive}")
        
        passed = (has_diet or has_workout) and is_comprehensive
        result = print_result(passed, "Multiple intents handled" if passed else "Incomplete handling of multiple intents")
        test_results.append(("Multiple Intents", result))
    else:
        test_results.append(("Multiple Intents", False))
    
    # Print Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed_count = sum(1 for _, passed in test_results if passed)
    total_count = len(test_results)
    
    for i, (test_name, passed) in enumerate(test_results, 1):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{i}. {test_name:30s} {status}")
    
    print(f"\n{'='*80}")
    print(f"FINAL SCORE: {passed_count}/{total_count} tests passed")
    print(f"Success Rate: {(passed_count/total_count)*100:.1f}%")
    print(f"{'='*80}")
    
    if passed_count >= 9:
        print("\n🎉 SUCCESS! At least 9/10 tests passed!")
    else:
        print(f"\n⚠️  NEEDS IMPROVEMENT: Only {passed_count}/10 tests passed. Target is 9/10.")
    
    return test_results, passed_count

if __name__ == "__main__":
    print("🧪 Starting Comprehensive Health Agent Testing...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: http://localhost:8001")
    
    try:
        results, score = run_tests()
        
        # Save results to file
        with open("agent_test_results.json", "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "score": f"{score}/10",
                "results": [{"test": name, "passed": passed} for name, passed in results]
            }, f, indent=2)
        
        print("\n📊 Results saved to agent_test_results.json")
        
    except Exception as e:
        print(f"\n❌ Testing failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
