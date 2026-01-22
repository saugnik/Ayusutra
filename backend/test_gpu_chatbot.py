"""
Test Med-Gemma with NVIDIA GPU
"""
import os
os.environ["MED_GEMMA_DEPLOYMENT"] = "ollama"

from med_gemma_service import get_med_gemma_service

print("=" * 60)
print("TESTING MED-GEMMA WITH NVIDIA GPU")
print("=" * 60)

# Get service
service = get_med_gemma_service(deployment_type="ollama")

print(f"\n✓ Service Available: {service.is_available()}")
print(f"✓ Model: {service.model_name}")
print(f"✓ Endpoint: {service.endpoint}")

# Check model availability
availability = service.check_model_availability()
print(f"\n✓ Model Check: {availability}")

# Test medical query
print("\n" + "=" * 60)
print("TEST 1: Medical Query (Diabetes)")
print("=" * 60)

response1 = service.generate_medical_response(
    query="What is diabetes and how is it managed?",
    context=None
)

print(f"\nSource: {response1.get('source')}")
print(f"Confidence: {response1.get('confidence')}")
print(f"Response:\n{response1.get('response')}")

# Test another query
print("\n" + "=" * 60)
print("TEST 2: Medical Query (Hypertension)")
print("=" * 60)

response2 = service.generate_medical_response(
    query="What causes high blood pressure?",
    context=None
)

print(f"\nSource: {response2.get('source')}")
print(f"Confidence: {response2.get('confidence')}")
print(f"Response:\n{response2.get('response')}")

print("\n" + "=" * 60)
print("✅ ALL TESTS COMPLETED!")
print("=" * 60)
print("\nNow check nvidia-smi to verify GPU was used!")
