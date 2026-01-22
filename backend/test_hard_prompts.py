"""
Comprehensive Test Suite for GPU-Powered Med-Gemma Chatbot
Tests with challenging medical prompts
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8002"
LOGIN_EMAIL = "test_patient_gpu@ayursutra.com"
LOGIN_PASSWORD = "password123"

# Hard medical prompts to test
HARD_PROMPTS = [
    {
        "category": "Complex Diagnosis",
        "prompt": "A 45-year-old patient presents with polyuria, polydipsia, unexplained weight loss, and HbA1c of 8.5%. What is the likely diagnosis and what are the differential diagnoses to consider?"
    },
    {
        "category": "Drug Interactions",
        "prompt": "What are the potential drug interactions between metformin, lisinopril, and atorvastatin in a patient with type 2 diabetes and hypertension?"
    },
    {
        "category": "Emergency Medicine",
        "prompt": "A patient arrives with severe chest pain radiating to the left arm, diaphoresis, and shortness of breath. What immediate steps should be taken and what tests should be ordered?"
    },
    {
        "category": "Rare Disease",
        "prompt": "Explain the pathophysiology of Addison's disease and how it differs from Cushing's syndrome in terms of cortisol levels and clinical presentation."
    },
    {
        "category": "Treatment Protocol",
        "prompt": "What is the step-by-step treatment protocol for a patient diagnosed with acute bacterial meningitis, including antibiotic choices and supportive care?"
    },
    {
        "category": "Pediatric Case",
        "prompt": "A 6-year-old child has recurrent respiratory infections, failure to thrive, and salty-tasting skin. What genetic disorder should be suspected and what diagnostic tests are needed?"
    },
    {
        "category": "Pharmacology",
        "prompt": "Compare and contrast the mechanisms of action, efficacy, and side effects of ACE inhibitors versus ARBs in treating hypertension."
    },
    {
        "category": "Multi-System Disease",
        "prompt": "Describe the systemic effects of uncontrolled diabetes mellitus on the cardiovascular, renal, neurological, and ophthalmologic systems."
    }
]

def login():
    """Login and get access token"""
    print("=" * 80)
    print("LOGGING IN...")
    print("=" * 80)
    
    response = requests.post(
        f"{BACKEND_URL}/auth/login",
        json={"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    )
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print(f"✓ Login successful! Token: {token[:30]}...")
        return token
    else:
        print(f"✗ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def test_chatbot(token, prompt_data):
    """Test chatbot with a specific prompt"""
    category = prompt_data['category']
    prompt = prompt_data['prompt']
    
    print("\n" + "=" * 80)
    print(f"TEST: {category}")
    print("=" * 80)
    print(f"Prompt: {prompt}")
    print("-" * 80)
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat/ai-assistant",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "message": prompt
            },
            timeout=60  # 60 second timeout for complex queries
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✓ Response received in {response_time:.2f} seconds")
            # API doesn't return model metadata in response model currently
            print(f"\nResponse:\n{data.get('reply', 'No reply content')}")
            
            return {
                "success": True,
                "category": category,
                "response_time": response_time,
                "model": "gemma2:2b", # Assumed based on server config
                "answer_length": len(data.get('reply', '')),
                "response_text": data.get('reply', 'No reply content')
            }
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return {
                "success": False,
                "category": category,
                "error": response.text
            }
            
    except requests.exceptions.Timeout:
        print("✗ Request timed out (>60 seconds)")
        return {
            "success": False,
            "category": category,
            "error": "Timeout"
        }
    except Exception as e:
        print(f"✗ Exception: {str(e)}")
        return {
            "success": False,
            "category": category,
            "error": str(e)
        }

def main():
    print("\n" + "=" * 80)
    print("GPU-POWERED MED-GEMMA CHATBOT - HARD PROMPT TEST SUITE")
    print("=" * 80)
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Prompts: {len(HARD_PROMPTS)}")
    print("=" * 80)
    
    # Login
    token = login()
    if not token:
        print("\n✗ Cannot proceed without authentication")
        return
    
    # Run tests
    results = []
    for i, prompt_data in enumerate(HARD_PROMPTS, 1):
        print(f"\n\n{'#' * 80}")
        print(f"TEST {i}/{len(HARD_PROMPTS)}")
        print(f"{'#' * 80}")
        
        result = test_chatbot(token, prompt_data)
        results.append(result)
        
        # Wait between requests to avoid overloading
        if i < len(HARD_PROMPTS):
            print("\nWaiting 2 seconds before next test...")
            time.sleep(2)
    
    # Summary
    print("\n\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"✓ Successful: {len(successful)}")
    print(f"✗ Failed: {len(failed)}")
    
    if successful:
        avg_time = sum(r['response_time'] for r in successful) / len(successful)
        avg_length = sum(r['answer_length'] for r in successful) / len(successful)
        
        print(f"\nPerformance Metrics:")
        print(f"  Average Response Time: {avg_time:.2f} seconds")
        print(f"  Average Answer Length: {avg_length:.0f} characters")
        
        models_used = set(str(r.get('model', 'Unknown')) for r in successful)
        print(f"  Models Used: {', '.join(models_used)}")
    
    if failed:
        print(f"\nFailed Tests:")
        for r in failed:
            print(f"  - {r['category']}: {r.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 80)
    print(f"Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Save results to file
    with open("chatbot_test_results.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_tests": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results
        }, f, indent=2)
    
    print("\n✓ Results saved to chatbot_test_results.json")

if __name__ == "__main__":
    main()
