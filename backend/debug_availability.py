
import requests
import json
import sys

BASE_URL = "http://localhost:8001"

def login(email, password):
    print(f"Logging in as {email}...")
    # Use the custom /auth/login endpoint with JSON
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return None
    return response.json()["access_token"]

def get_profile(token):
    print("Fetching profile...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/practitioner/profile", headers=headers)
    if response.status_code != 200:
        print(f"Get profile failed: {response.text}")
        return None
    return response.json()

def update_profile(token, schedule):
    print("Updating profile with new schedule...")
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"availability_schedule": schedule}
    response = requests.patch(f"{BASE_URL}/practitioner/profile", json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Update profile failed: {response.text}")
        with open("last_error.txt", "w") as f:
            f.write(response.text)
        return None
    return response.json()

def main():
    # 1. Login
    # Using a known practitioner user or creating one. 
    # I'll rely on one existing from previous context or generic one.
    # Assuming 'practitioner@example.com' / 'password123' if it exists, 
    # OR better, use the one from users_export.txt if I viewed it, or just try generic.
    # Actually, I'll try to find a valid user.
    # Let's try 'dr.priya@example.com' or similar if I saw it.
    # If not, I can register one, but I'll try a common test user first.
    
    # Wait, I can assume the user I created in previous steps might exist? 
    # Let's try to register a temp one to be safe.
    
    # Register temp practitioner
    reg_email = f"debug_avail_{json.dumps(sys.argv)}@example.com"
    reg_pass = "password123"
    
    # Actually, let's just use the login credentials if I know them. 
    # Since I don't want to blindly guess, I will try to create a *new* one to be clean.
    
    # Use Dr. Sharma credentials
    email = "dr.sharma@ayursutra.com"
    password = "password123"
    
    # Skip registration, just login
    token = login(email, password)
    if not token:
        print("Login failed for Dr. Sharma.")
        return

    # 2. Get initial profile
    profile = get_profile(token)
    print(f"Initial Schedule: {json.dumps(profile.get('availability_schedule'), indent=2)}")

    # 3. Update schedule
    new_schedule = {
        "monday": [
            {"start_time": "09:00", "end_time": "12:00", "location": "Debug Clinic"}
        ],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": [],
        "saturday": [],
        "sunday": []
    }
    
    updated_profile = update_profile(token, new_schedule)
    if not updated_profile:
        print("Update failed.")
        return

    print("Update call returned success.")

    # 4. Verify persistence
    print("Verifying persistence by fetching profile again...")
    final_profile = get_profile(token)
    
    saved_schedule = final_profile.get('availability_schedule')
    print(f"Saved Schedule: {json.dumps(saved_schedule, indent=2)}")
    
    # Check
    if saved_schedule and len(saved_schedule.get("monday", [])) == 1:
        print("SUCCESS: Schedule saved correctly.")
        if saved_schedule["monday"][0]["location"] == "Debug Clinic":
             print("SUCCESS: Location saved correctly.")
        else:
             print("FAILURE: Location mismatch.")
    else:
        print("FAILURE: Schedule NOT saved.")

if __name__ == "__main__":
    main()
