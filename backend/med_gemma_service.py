"""
Med-Gemma Service Layer
Provides medical AI capabilities using Med-Gemma 2B via Ollama
"""

import os
import logging
from typing import Dict, Any, Optional, List
import json

logger = logging.getLogger(__name__)

class MedGemmaService:
    """
    Service wrapper for Med-Gemma medical AI model
    Supports Ollama local deployment with fallback options
    """
    
    def __init__(self, deployment_type: str = "ollama"):
        """
        Initialize Med-Gemma service
        
        Args:
            deployment_type: 'ollama', 'huggingface', or 'mock'
        """
        self.deployment_type = deployment_type
        self.model_name = os.getenv("MED_GEMMA_MODEL", "gemma2:2b")
        self.endpoint = os.getenv("MED_GEMMA_ENDPOINT", "http://localhost:11434")
        self.available = False
        
        # Try to initialize based on deployment type
        if deployment_type == "ollama":
            self._init_ollama()
        elif deployment_type == "huggingface":
            self._init_huggingface()
        else:
            logger.warning("Using mock Med-Gemma service")
            self.available = True  # Mock is always available
    
    def _init_ollama(self):
        """Initialize Ollama client"""
        try:
            import ollama
            self.client = ollama.Client(host=self.endpoint)
            
            # Test connection
            try:
                self.client.list()
                self.available = True
                logger.info(f"Med-Gemma service initialized via Ollama at {self.endpoint}")
            except Exception as e:
                logger.warning(f"Ollama server not available: {e}")
                self.available = False
        except ImportError:
            logger.error("Ollama package not installed. Run: pip install ollama")
            self.available = False
    
    def _init_huggingface(self):
        """Initialize Hugging Face Inference API client"""
        try:
            from huggingface_hub import InferenceClient
            api_key = os.getenv("HUGGINGFACE_API_KEY")
            
            if not api_key:
                logger.warning("HUGGINGFACE_API_KEY not found")
                self.available = False
                return
            
            self.client = InferenceClient(token=api_key)
            self.available = True
            logger.info("Med-Gemma service initialized via Hugging Face")
        except ImportError:
            logger.error("huggingface_hub package not installed")
            self.available = False
    
    def is_available(self) -> bool:
        """Check if Med-Gemma service is available"""
        return self.available
    
    def generate_medical_response(
        self,
        query: str,
        context: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate medical response using Med-Gemma
        
        Args:
            query: User's medical query
            context: Additional context (patient history, symptoms, etc.)
            conversation_history: Previous conversation messages
            
        Returns:
            Dict with 'response', 'confidence', and 'source' keys
        """
        if not self.available:
            return {
                "response": None,
                "confidence": 0.0,
                "source": "med-gemma",
                "error": "Med-Gemma service not available"
            }
        
        # Build prompt for medical query
        prompt = self._build_medical_prompt(query, context, conversation_history)
        
        try:
            if self.deployment_type == "ollama":
                return self._generate_ollama(prompt)
            elif self.deployment_type == "huggingface":
                return self._generate_huggingface(prompt)
            else:
                return self._generate_mock(prompt, query)
        except Exception as e:
            logger.error(f"Med-Gemma generation error: {e}")
            return {
                "response": None,
                "confidence": 0.0,
                "source": "med-gemma",
                "error": str(e)
            }
    
    def _build_medical_prompt(
        self,
        query: str,
        context: Optional[str],
        conversation_history: Optional[List[Dict[str, str]]]
    ) -> str:
        """Build optimized prompt for Med-Gemma"""
        
        # Medical system prompt
        system_prompt = """You are a medical AI assistant trained on clinical literature and medical knowledge. 
Provide accurate, evidence-based medical information. Always recommend consulting healthcare professionals for diagnosis and treatment.
Be clear, concise, and use appropriate medical terminology when necessary.
If you're unsure, acknowledge limitations and suggest professional consultation."""
        
        # Build conversation context
        prompt_parts = [system_prompt, "\n"]
        
        if conversation_history:
            prompt_parts.append("Previous conversation:\n")
            for msg in conversation_history[-3:]:  # Last 3 messages
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                prompt_parts.append(f"{role}: {content}\n")
        
        if context:
            prompt_parts.append(f"\nPatient Context: {context}\n")
        
        prompt_parts.append(f"\nUser Query: {query}\n\nMedical Assistant Response:")
        
        return "".join(prompt_parts)
    
    def _generate_ollama(self, prompt: str) -> Dict[str, Any]:
        """Generate response using Ollama"""
        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.3,  # Lower temperature for medical accuracy
                    "top_p": 0.9,
                    "num_predict": 512  # Max tokens
                }
            )
            
            return {
                "response": response['response'].strip(),
                "confidence": 0.85,  # Med-Gemma is generally confident
                "source": "med-gemma-ollama",
                "model": self.model_name
            }
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            raise
    
    def _generate_huggingface(self, prompt: str) -> Dict[str, Any]:
        """Generate response using Hugging Face Inference API"""
        try:
            response = self.client.text_generation(
                prompt,
                model="google/medgemma-2b",
                max_new_tokens=512,
                temperature=0.3
            )
            
            return {
                "response": response.strip(),
                "confidence": 0.85,
                "source": "med-gemma-huggingface",
                "model": "medgemma-2b"
            }
        except Exception as e:
            logger.error(f"Hugging Face generation error: {e}")
            raise
    
    def _generate_mock(self, prompt: str, query: str) -> Dict[str, Any]:
        """Generate mock response for testing"""
        query_lower = query.lower()
        
        # Simple keyword-based mock responses
        if "diabetes" in query_lower:
            response = """For diabetes management, I recommend:
1. Monitor blood glucose regularly
2. Follow a low-glycemic diet (avoid refined sugars, white bread)
3. Include fiber-rich foods, whole grains, and lean proteins
4. Stay hydrated and exercise regularly
5. **Important**: Consult an endocrinologist for personalized treatment plan"""
        
        elif "blood pressure" in query_lower or "hypertension" in query_lower:
            response = """For blood pressure management:
1. Reduce sodium intake (limit salt, processed foods)
2. Eat potassium-rich foods (bananas, spinach, sweet potatoes)
3. Maintain healthy weight and exercise regularly
4. Limit alcohol and avoid smoking
5. **Important**: Consult a cardiologist for proper diagnosis and medication"""
        
        elif "thyroid" in query_lower:
            response = """For thyroid health:
1. Ensure adequate iodine intake (if hypothyroid)
2. Include selenium-rich foods (brazil nuts, fish)
3. Avoid excessive raw cruciferous vegetables if hypothyroid
4. Manage stress and get adequate sleep
5. **Important**: Consult an endocrinologist for thyroid function tests and treatment"""
        
        else:
            response = f"""Based on your medical query about '{query}', I recommend:
1. Maintain a balanced, nutritious diet
2. Stay physically active
3. Monitor your symptoms carefully
4. Keep a health journal
5. **Important**: Please consult a healthcare professional for proper diagnosis and treatment.

This is general medical information and not a substitute for professional medical advice."""
        
        return {
            "response": response,
            "confidence": 0.75,
            "source": "med-gemma-mock",
            "model": "mock"
        }
    
    def check_model_availability(self) -> Dict[str, Any]:
        """Check if Med-Gemma model is available and ready"""
        if self.deployment_type == "ollama" and self.available:
            try:
                models = self.client.list()
                model_names = [m['name'] for m in models.get('models', [])]
                
                return {
                    "available": self.model_name in model_names,
                    "installed_models": model_names,
                    "deployment": "ollama",
                    "endpoint": self.endpoint
                }
            except Exception as e:
                return {
                    "available": False,
                    "error": str(e),
                    "deployment": "ollama"
                }
        
        return {
            "available": self.available,
            "deployment": self.deployment_type
        }


# Singleton instance
_med_gemma_service = None

def get_med_gemma_service(deployment_type: str = None) -> MedGemmaService:
    """Get or create Med-Gemma service singleton"""
    global _med_gemma_service
    
    if _med_gemma_service is None:
        if deployment_type is None:
            deployment_type = os.getenv("MED_GEMMA_DEPLOYMENT", "mock")
        
        _med_gemma_service = MedGemmaService(deployment_type=deployment_type)
    
    return _med_gemma_service
