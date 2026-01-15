
import requests
import json
import sys

BASE_URL = "http://localhost:8001"

def register_user(email, role):
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": email,
        "password": "password123",
        "full_name": f"Test {role.capitalize()}",
        "role": role,
        "phone": "1234567890"
    }
    # Try login first to get token if exists
    login_data = {"email": email, "password": "password123"}
    try:
        r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if r.status_code == 200:
            return r.json()["access_token"], r.json()["user_id"]
    except:
        pass

    # Register
    r = requests.post(url, json=data)
    if r.status_code != 200:
        # If already exists (400), try login again
        r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if r.status_code == 200:
            return r.json()["access_token"], r.json()["user_id"]
        print(f"Failed to register/login {role}: {r.text}")
        sys.exit(1)
    
    # Login to get token
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    return r.json()["access_token"], r.json()["user_id"]

def test_flow():
    print("1. Setup Users...")
    patient_token, patient_id = register_user("patient_flow@test.com", "patient")
    practitioner_token, practitioner_id = register_user("practitioner_flow@test.com", "practitioner")
    
    headers_patient = {"Authorization": f"Bearer {patient_token}"}
    headers_practitioner = {"Authorization": f"Bearer {practitioner_token}"}

    print("\n2. Patient submits input (Symptom)...")
    symptom_data = {
        "symptom_name": "High Fever",
        "severity": "high",
        "notes": "Feeling very hot and shivering",
        "duration_days": 2
    }
    r = requests.post(f"{BASE_URL}/health/symptoms", json=symptom_data, headers=headers_patient)
    if r.status_code == 200:
        print("✅ Patient logged symptom successfully.")
    else:
        print(f"❌ Patient failed to log symptom: {r.text}")

    print("\n3. Check if Practitioner can see this input...")
    # Try to get patient report
    # First we need the patient's ID (the generic ID, not User ID). 
    # The registration returns User object. We need to find the Patient ID.
    # We can get it from /users/me for the patient
    r = requests.get(f"{BASE_URL}/users/me", headers=headers_patient)
    p_profile_id = r.json()["patient_profile"]["id"]
    
    print(f"   Patient Profile ID: {p_profile_id}")

    # Practitioner attempts to get report
    r = requests.get(f"{BASE_URL}/reports/patient/{p_profile_id}", headers=headers_practitioner)
    if r.status_code == 200:
        report = r.json()
        print("✅ Practitioner got patient report.")
        
        # Check if symptom is in the report
        # Based on my code reading, it is NOT in the report structure yet.
        # ReportHealthStats has avg_sleep, etc. but not symptoms list. 
        # Wait, get_patient_report line 703 returns ReportHealthStats.
        # Line 710 return recent_health_logs.
        # It does NOT verify symptoms.
        
        print(f"   Report Keys: {report.keys()}")
        # We manually check if our symptom is there (it shouldn't be)
        if "symptoms" in str(report).lower():
             print("❓ Symptoms found in report (Unexpected based on code reading)")
        else:
             print("❌ Symptoms NOT found in report (Expected)")
             
    else:
        print(f"❌ Practitioner failed to get report: {r.text}")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"Error: {e}")
