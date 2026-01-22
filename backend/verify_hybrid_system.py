"""
Quick verification script for hybrid AI system
Tests query classification and Med-Gemma service without full backend
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from query_classifier import get_query_classifier
from med_gemma_service import get_med_gemma_service

def test_query_classification():
    """Test query classification with sample queries"""
    print("=" * 60)
    print("TESTING QUERY CLASSIFICATION")
    print("=" * 60)
    
    classifier = get_query_classifier()
    
    test_queries = [
        "I have diabetes, what should I eat?",
        "My blood pressure is high",
        "What is my dosha type?",
        "I want a diet plan for weight loss",
        "I have diabetes and want an Ayurvedic diet for my pitta dosha",
        "Can you help me with yoga exercises?",
        "I'm experiencing fever and headache",
    ]
    
    for query in test_queries:
        report = classifier.get_classification_report(query)
        print(f"\nQuery: {query}")
        print(f"  → Model: {report['recommended_model']}")
        print(f"  → Confidence: {report['confidence']:.2f}")
        print(f"  → Use Med-Gemma: {report['use_med_gemma']}")
        print(f"  → Explanation: {report['explanation']}")

def test_med_gemma_service():
    """Test Med-Gemma service (mock mode)"""
    print("\n" + "=" * 60)
    print("TESTING MED-GEMMA SERVICE (MOCK MODE)")
    print("=" * 60)
    
    service = get_med_gemma_service("mock")
    
    print(f"\nMed-Gemma Available: {service.is_available()}")
    print(f"Deployment Type: {service.deployment_type}")
    
    # Test medical queries
    test_queries = [
        "I have diabetes, what should I eat?",
        "My blood pressure is high, what should I avoid?",
        "I have thyroid problems, what diet should I follow?",
    ]
    
    for query in test_queries:
        print(f"\n{'─' * 60}")
        print(f"Query: {query}")
        response = service.generate_medical_response(query)
        
        if response.get('response'):
            print(f"\nResponse:")
            print(response['response'][:300] + "..." if len(response['response']) > 300 else response['response'])
            print(f"\nSource: {response['source']}")
            print(f"Confidence: {response['confidence']}")
        else:
            print(f"Error: {response.get('error')}")

def test_hybrid_flow():
    """Test complete hybrid flow"""
    print("\n" + "=" * 60)
    print("TESTING HYBRID FLOW")
    print("=" * 60)
    
    classifier = get_query_classifier()
    med_gemma = get_med_gemma_service("mock")
    
    test_cases = [
        {
            "query": "I have diabetes and high blood pressure",
            "expected_model": "medical"
        },
        {
            "query": "What is my dosha type and what diet should I follow?",
            "expected_model": "ayurvedic"
        }
    ]
    
    for case in test_cases:
        query = case['query']
        expected = case['expected_model']
        
        print(f"\n{'─' * 60}")
        print(f"Query: {query}")
        print(f"Expected Model: {expected}")
        
        # Step 1: Classify
        model_type, confidence, metadata = classifier.classify(query)
        print(f"\n✓ Classification: {model_type} (confidence: {confidence:.2f})")
        
        # Step 2: Route
        should_use_med_gemma = classifier.should_use_med_gemma(query)
        print(f"✓ Use Med-Gemma: {should_use_med_gemma}")
        
        # Step 3: Generate (if medical)
        if should_use_med_gemma and med_gemma.is_available():
            response = med_gemma.generate_medical_response(query)
            if response.get('response'):
                print(f"✓ Med-Gemma Response Generated")
                print(f"  Preview: {response['response'][:150]}...")
        
        # Verify
        if model_type == expected:
            print(f"✅ PASS: Correctly classified as {expected}")
        else:
            print(f"❌ FAIL: Expected {expected}, got {model_type}")

if __name__ == "__main__":
    print("\n🚀 HYBRID AI SYSTEM VERIFICATION")
    print("=" * 60)
    
    try:
        test_query_classification()
        test_med_gemma_service()
        test_hybrid_flow()
        
        print("\n" + "=" * 60)
        print("✅ ALL VERIFICATION TESTS COMPLETED")
        print("=" * 60)
        print("\nNext Steps:")
        print("1. Install Ollama: https://ollama.ai/download/windows")
        print("2. Pull Med-Gemma: ollama pull medgemma:2b")
        print("3. Update .env: MED_GEMMA_DEPLOYMENT=ollama")
        print("4. Start backend: uvicorn main:app --reload --port 8001")
        print("5. Test in browser at http://localhost:3000")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
