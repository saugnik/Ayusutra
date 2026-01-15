
import requests
import json
import sys
import time

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
    login_data = {"email": email, "password": "password123"}
    
    try:
        r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if r.status_code == 200:
            return r.json()["access_token"], r.json()["user_id"]
    except:
        pass

    r = requests.post(url, json=data)
    if r.status_code != 200:
        r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if r.status_code == 200:
            return r.json()["access_token"], r.json()["user_id"]
        print(f"Failed to register/login {role}: {r.text}")
        sys.exit(1)
    
    r = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    return r.json()["access_token"], r.json()["user_id"]

def verify_flow():
    print("1. Setup unique users for this run...")
    timestamp = int(time.time())
    patient_email = f"p_flow_{timestamp}@test.com"
    practitioner_email = f"dr_flow_{timestamp}@test.com"
    
    patient_token, patient_id_user = register_user(patient_email, "patient")
    practitioner_token, practitioner_id = register_user(practitioner_email, "practitioner")
    
    headers_patient = {"Authorization": f"Bearer {patient_token}"}
    headers_practitioner = {"Authorization": f"Bearer {practitioner_token}"}

    print("\n2. Patient submits input (Symptom)...")
    symptom_name = f"Test Fever {timestamp}"
    symptom_data = {
        "symptom_name": symptom_name,
        "severity": "high",
        "notes": "Feeling very hot",
        "duration_days": 2
    }
    r = requests.post(f"{BASE_URL}/health/symptoms", json=symptom_data, headers=headers_patient)
    if r.status_code == 200:
        print("✅ Patient logged symptom successfully.")
        # Extract patient_id from the response which is a SymptomResponse
        p_profile_id = r.json()["patient_id"]
        print(f"   Patient Profile ID: {p_profile_id}")
    else:
        print(f"❌ Patient failed to log symptom: {r.text}")
        sys.exit(1)

    print("\n3. Practitioner checks report...")
    
    # Get report using the extracted profile ID
    r = requests.get(f"{BASE_URL}/reports/patient/{p_profile_id}", headers=headers_practitioner)
    if r.status_code == 200:
        report = r.json()
        print("✅ Practitioner got patient report.")
        
        # Check for recent_symptoms field
        if "recent_symptoms" not in report:
            print("❌ 'recent_symptoms' field MISSING in report response.")
            print(f"Keys found: {report.keys()}")
            sys.exit(1)
            
        symptoms = report["recent_symptoms"]
        found = False
        for s in symptoms:
            if s["symptom_name"] == symptom_name:
                found = True
                break
        
        if found:
            print(f"✅ SUCCESS: Verified symptom '{symptom_name}' is visible to practitioner!")
        else:
            print(f"❌ FAILURE: Symptom '{symptom_name}' NOT found in practitioner report.")
            print(f"Symptoms returned: {json.dumps(symptoms, indent=2)}")
             
    else:
        print(f"❌ Practitioner failed to get report: {r.text}")

if __name__ == "__main__":
    try:
        verify_flow()
    except Exception as e:
        print(f"Error: {e}")
