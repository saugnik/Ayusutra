"""Simple Health Agent Test - 10 Test Cases"""
import requests
import json

BASE = "http://localhost:8001"

print("="*60)
print("HEALTH AGENT - 10 TEST CASES")
print("="*60)

# Login
print("\n🔐 Logging in...")
r = requests.post(f"{BASE}/auth/login", json={"email":"patient@test.com","password":"patient123"})
if r.status_code != 200:
    print(f"❌ Login failed: {r.status_code} - {r.text}")
    exit(1)

token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("✅ Login successful\n")

results = []

# Test 1: Water Reminder
print("TEST 1: Water Reminder")
r = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"Remind me to drink water every 2 hours"})
if r.status_code == 200:
    data = r.json()
    has_action = len(data.get("actions", [])) > 0
    print(f"✅ PASS" if has_action else "❌ FAIL")
    results.append(("Water Reminder", has_action))
else:
    print(f"❌ FAIL - {r.status_code}")
    results.append(("Water Reminder", False))

# Test 2: Exercise Reminder  
print("\nTEST 2: Exercise Reminder")
r = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"I want to exercise daily at 6 AM"})
if r.status_code == 200:
    data = r.json()
    has_action = len(data.get("actions", [])) > 0
    print(f"✅ PASS" if has_action else "❌ FAIL")
    results.append(("Exercise Reminder", has_action))
else:
    print(f"❌ FAIL - {r.status_code}")
    results.append(("Exercise Reminder", False))

# Test 3: Diet Plan
print("\nTEST 3: Diet Plan")
r = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"I'm 25 years old, weigh 70kg, height 175cm. Create a diet plan for weight loss."})
if r.status_code == 200:
    reply = r.json().get("reply", "")
    has_diet = "calorie" in reply.lower() and "meal" in reply.lower()
    print(f"✅ PASS" if has_diet else "❌ FAIL")
    results.append(("Diet Plan", has_diet))
else:
    print(f"❌ FAIL - {r.status_code}")
    results.append(("Diet Plan", False))

# Test 4: Workout Plan
print("\nTEST 4: Workout Plan")
r = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"Create a workout plan for me"})
if r.status_code == 200:
    reply = r.json().get("reply", "")
    has_workout = "workout" in reply.lower() or "exercise" in reply.lower()
    print(f"✅ PASS" if has_workout else "❌ FAIL")
    results.append(("Workout Plan", has_workout))
else:
    print(f"❌ FAIL - {r.status_code}")
    results.append(("Workout Plan", False))

# Test 5: Find Practitioner
print("\nTEST 5: Find Practitioner")
r = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"I have a severe headache. Help me find a doctor."})
if r.status_code == 200:
    data = r.json()
    reply = data.get("reply", "")
    has_rec = "doctor" in reply.lower() or "practitioner" in reply.lower() or len(data.get("actions", [])) > 0
    print(f"✅ PASS" if has_rec else "❌ FAIL")
    results.append(("Find Practitioner", has_rec))
else:
    print(f"❌ FAIL - {r.status_code}")
    results.append(("Find Practitioner", False))

# Test 6: Ayurvedic Q&A
print("\nTEST 6: Ayurvedic Q&A")
r = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"What are the benefits of drinking warm water in Ayurveda?"})
if r.status_code == 200:
    reply = r.json().get("reply", "")
    has_answer = len(reply) > 100 and "benefit" in reply.lower()
    print(f"✅ PASS" if has_answer else "❌ FAIL")
    results.append(("Ayurvedic Q&A", has_answer))
else:
    print(f"❌ FAIL - {r.status_code}")
    results.append(("Ayurvedic Q&A", False))

# Test 7: Medicine Reminder
print("\nTEST 7: Medicine Reminder")
r = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"Remind me to take medicine at 8 AM and 8 PM"})
if r.status_code == 200:
    data = r.json()
    has_action = len(data.get("actions", [])) > 0
    print(f"✅ PASS" if has_action else "❌ FAIL")
    results.append(("Medicine Reminder", has_action))
else:
    print(f"❌ FAIL - {r.status_code}")
    results.append(("Medicine Reminder", False))

# Test 8: Clarification
print("\nTEST 8: Clarification")
r = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"I want a diet plan"})
if r.status_code == 200:
    reply = r.json().get("reply", "")
    asks_info = "age" in reply.lower() or "weight" in reply.lower() or "?" in reply
    print(f"✅ PASS" if asks_info else "❌ FAIL")
    results.append(("Clarification", asks_info))
else:
    print(f"❌ FAIL - {r.status_code}")
    results.append(("Clarification", False))

# Test 9: Context Memory
print("\nTEST 9: Context Memory")
r1 = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"I'm 30 years old and weigh 80kg"})
if r1.status_code == 200:
    r2 = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"Create a diet plan"})
    if r2.status_code == 200:
        reply = r2.json().get("reply", "")
        has_plan = "calorie" in reply.lower() or "diet" in reply.lower()
        print(f"✅ PASS" if has_plan else "❌ FAIL")
        results.append(("Context Memory", has_plan))
    else:
        print(f"❌ FAIL - {r2.status_code}")
        results.append(("Context Memory", False))
else:
    print(f"❌ FAIL - {r1.status_code}")
    results.append(("Context Memory", False))

# Test 10: Multiple Intents
print("\nTEST 10: Multiple Intents")
r = requests.post(f"{BASE}/api/agent/chat", headers=headers, json={"message":"I want to lose weight. Create a diet and workout plan. I'm 28, 75kg, 170cm."})
if r.status_code == 200:
    reply = r.json().get("reply", "")
    has_both = ("diet" in reply.lower() or "meal" in reply.lower()) and ("workout" in reply.lower() or "exercise" in reply.lower())
    print(f"✅ PASS" if has_both else "❌ FAIL")
    results.append(("Multiple Intents", has_both))
else:
    print(f"❌ FAIL - {r.status_code}")
    results.append(("Multiple Intents", False))

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
passed = sum(1 for _, p in results if p)
for i, (name, p) in enumerate(results, 1):
    print(f"{i}. {name:25s} {'✅ PASS' if p else '❌ FAIL'}")
print(f"\nFINAL SCORE: {passed}/10")
print(f"Success Rate: {(passed/10)*100:.0f}%")
print("="*60)

if passed >= 9:
    print("\n🎉 SUCCESS! At least 9/10 tests passed!")
else:
    print(f"\n⚠️  Only {passed}/10 passed. Target: 9/10")
