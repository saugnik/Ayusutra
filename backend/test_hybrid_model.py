"""
Test Suite for Hybrid Med-Gemma + Gemini Pro Integration
Tests query classification, hybrid routing, and fallback scenarios
"""

import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from query_classifier import QueryClassifier, get_query_classifier
from med_gemma_service import MedGemmaService, get_med_gemma_service


class TestQueryClassifier:
    """Test query classification logic"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.classifier = QueryClassifier()
    
    def test_medical_query_classification(self):
        """Test that medical queries are correctly classified"""
        test_cases = [
            ("I have diabetes, what should I eat?", "medical"),
            ("My blood pressure is high", "medical"),
            ("I have thyroid problems", "medical"),
            ("What medication should I take for headache?", "medical"),
            ("I'm experiencing fever and cough", "medical"),
        ]
        
        for query, expected_type in test_cases:
            model_type, confidence, metadata = self.classifier.classify(query)
            assert model_type == expected_type, f"Query '{query}' should be classified as {expected_type}, got {model_type}"
            assert confidence > 0.6, f"Confidence should be > 0.6, got {confidence}"
    
    def test_ayurvedic_query_classification(self):
        """Test that Ayurvedic queries are correctly classified"""
        test_cases = [
            ("What is my dosha type?", "ayurvedic"),
            ("I want a diet plan for vata", "ayurvedic"),
            ("Can you suggest a workout routine?", "ayurvedic"),
            ("Tell me about panchakarma treatment", "ayurvedic"),
            ("I need yoga exercises for stress", "ayurvedic"),
        ]
        
        for query, expected_type in test_cases:
            model_type, confidence, metadata = self.classifier.classify(query)
            assert model_type == expected_type, f"Query '{query}' should be classified as {expected_type}, got {model_type}"
            assert confidence > 0.6, f"Confidence should be > 0.6, got {confidence}"
    
    def test_hybrid_query_classification(self):
        """Test that hybrid queries are detected"""
        query = "I have diabetes and want an Ayurvedic diet plan for my pitta dosha"
        model_type, confidence, metadata = self.classifier.classify(query)
        
        assert model_type == "hybrid", f"Query should be classified as hybrid, got {model_type}"
        assert metadata['medical_score'] > 0, "Should have medical keywords"
        assert metadata['ayurvedic_score'] > 0, "Should have Ayurvedic keywords"
    
    def test_general_query_classification(self):
        """Test that general queries are classified correctly"""
        test_cases = [
            "Hello, how are you?",
            "What is the weather today?",
            "Tell me a joke",
        ]
        
        for query in test_cases:
            model_type, confidence, metadata = self.classifier.classify(query)
            assert model_type == "general", f"Query '{query}' should be classified as general, got {model_type}"
    
    def test_should_use_med_gemma(self):
        """Test Med-Gemma usage decision"""
        # Should use Med-Gemma
        assert self.classifier.should_use_med_gemma("I have diabetes") == True
        assert self.classifier.should_use_med_gemma("My blood pressure is high") == True
        
        # Should NOT use Med-Gemma
        assert self.classifier.should_use_med_gemma("What is my dosha?") == False
        assert self.classifier.should_use_med_gemma("I want a diet plan") == False
    
    def test_classification_report(self):
        """Test detailed classification report"""
        query = "I have diabetes"
        report = self.classifier.get_classification_report(query)
        
        assert 'query' in report
        assert 'recommended_model' in report
        assert 'confidence' in report
        assert 'use_med_gemma' in report
        assert 'metadata' in report
        assert 'explanation' in report
        
        assert report['recommended_model'] == 'medical'
        assert report['use_med_gemma'] == True


class TestMedGemmaService:
    """Test Med-Gemma service wrapper"""
    
    def setup_method(self):
        """Setup test fixtures"""
        # Use mock deployment for testing
        self.service = MedGemmaService(deployment_type="mock")
    
    def test_service_initialization(self):
        """Test that service initializes correctly"""
        assert self.service is not None
        assert self.service.deployment_type == "mock"
        assert self.service.is_available() == True
    
    def test_medical_response_generation(self):
        """Test medical response generation"""
        query = "I have diabetes, what should I eat?"
        response = self.service.generate_medical_response(query)
        
        assert 'response' in response
        assert 'confidence' in response
        assert 'source' in response
        
        assert response['response'] is not None
        assert len(response['response']) > 0
        assert 'diabetes' in response['response'].lower()
    
    def test_medical_response_with_context(self):
        """Test medical response with patient context"""
        query = "What diet should I follow?"
        context = "Patient has diabetes and hypertension"
        
        response = self.service.generate_medical_response(query, context=context)
        
        assert response['response'] is not None
        assert len(response['response']) > 0
    
    def test_medical_response_with_history(self):
        """Test medical response with conversation history"""
        query = "What else should I do?"
        history = [
            {"role": "user", "content": "I have diabetes"},
            {"role": "assistant", "content": "I recommend a low-glycemic diet"}
        ]
        
        response = self.service.generate_medical_response(query, conversation_history=history)
        
        assert response['response'] is not None
    
    def test_model_availability_check(self):
        """Test model availability check"""
        availability = self.service.check_model_availability()
        
        assert 'available' in availability
        assert 'deployment' in availability
        assert availability['deployment'] == 'mock'


class TestHybridIntegration:
    """Test hybrid AI integration end-to-end"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.classifier = get_query_classifier()
        self.med_gemma = get_med_gemma_service("mock")
    
    def test_medical_query_flow(self):
        """Test complete flow for medical query"""
        query = "I have diabetes and high blood pressure"
        
        # Step 1: Classify
        model_type, confidence, metadata = self.classifier.classify(query)
        assert model_type == "medical"
        
        # Step 2: Route to Med-Gemma
        should_use_med_gemma = self.classifier.should_use_med_gemma(query)
        assert should_use_med_gemma == True
        
        # Step 3: Generate response
        if should_use_med_gemma and self.med_gemma.is_available():
            response = self.med_gemma.generate_medical_response(query)
            assert response['response'] is not None
            assert response['source'] == 'med-gemma-mock'
    
    def test_ayurvedic_query_flow(self):
        """Test complete flow for Ayurvedic query"""
        query = "What is my dosha type and what diet should I follow?"
        
        # Step 1: Classify
        model_type, confidence, metadata = self.classifier.classify(query)
        assert model_type == "ayurvedic"
        
        # Step 2: Should NOT use Med-Gemma
        should_use_med_gemma = self.classifier.should_use_med_gemma(query)
        assert should_use_med_gemma == False
    
    def test_hybrid_query_flow(self):
        """Test complete flow for hybrid query"""
        query = "I have diabetes and want an Ayurvedic diet plan for my pitta dosha"
        
        # Step 1: Classify
        model_type, confidence, metadata = self.classifier.classify(query)
        assert model_type == "hybrid"
        
        # Step 2: May use Med-Gemma depending on confidence
        should_use_med_gemma = self.classifier.should_use_med_gemma(query)
        # Hybrid queries with high confidence may use Med-Gemma
        assert isinstance(should_use_med_gemma, bool)


def test_singleton_instances():
    """Test that singleton instances work correctly"""
    classifier1 = get_query_classifier()
    classifier2 = get_query_classifier()
    assert classifier1 is classifier2, "Query classifier should be singleton"
    
    service1 = get_med_gemma_service("mock")
    service2 = get_med_gemma_service()
    assert service1 is service2, "Med-Gemma service should be singleton"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
