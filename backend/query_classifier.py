"""
Query Classifier
Intelligently routes queries between Med-Gemma (medical) and Gemini Pro (Ayurvedic/wellness)
"""

import logging
from typing import Dict, Any, Tuple
import re

logger = logging.getLogger(__name__)

class QueryClassifier:
    """
    Classifies user queries to determine appropriate AI model
    """
    
    # Medical keywords that indicate Med-Gemma should be used
    MEDICAL_KEYWORDS = {
        # Diseases and conditions
        'diabetes', 'diabetic', 'blood sugar', 'glucose', 'insulin',
        'hypertension', 'blood pressure', 'bp', 'high bp', 'low bp',
        'thyroid', 'hypothyroid', 'hyperthyroid', 'tsh',
        'pcos', 'pcod', 'polycystic',
        'cholesterol', 'lipid', 'triglyceride',
        'arthritis', 'joint pain', 'inflammation',
        'asthma', 'breathing', 'respiratory',
        'heart disease', 'cardiac', 'cardiovascular',
        'kidney', 'renal', 'liver', 'hepatic',
        'cancer', 'tumor', 'malignant',
        'infection', 'bacterial', 'viral', 'fungal',
        
        # Symptoms
        'fever', 'temperature', 'cough', 'cold', 'flu',
        'headache', 'migraine', 'pain', 'ache',
        'nausea', 'vomiting', 'diarrhea', 'constipation',
        'rash', 'itching', 'swelling', 'bruise',
        'bleeding', 'discharge', 'wound',
        'fatigue', 'weakness', 'dizziness', 'vertigo',
        
        # Medical terms
        'diagnosis', 'treatment', 'medication', 'medicine', 'drug',
        'prescription', 'dosage', 'side effect',
        'surgery', 'operation', 'procedure',
        'test', 'lab', 'scan', 'x-ray', 'mri', 'ct scan',
        'doctor', 'physician', 'specialist', 'hospital', 'clinic',
        'emergency', 'urgent', 'acute', 'chronic',
        
        # Body systems
        'cardiovascular', 'respiratory', 'digestive', 'nervous',
        'endocrine', 'immune', 'lymphatic', 'urinary'
    }
    
    # Ayurvedic/Wellness keywords that indicate Gemini Pro should be used
    AYURVEDIC_KEYWORDS = {
        # Ayurvedic concepts
        'dosha', 'vata', 'pitta', 'kapha', 'prakriti', 'vikriti',
        'panchakarma', 'abhyanga', 'shirodhara', 'nasya', 'basti',
        'ayurveda', 'ayurvedic', 'ayurved',
        'tridosha', 'agni', 'ama', 'ojas', 'prana',
        
        # Wellness and lifestyle
        'diet plan', 'meal plan', 'nutrition', 'healthy eating',
        'workout', 'exercise', 'fitness', 'yoga', 'asana',
        'meditation', 'pranayama', 'breathing exercise',
        'wellness', 'wellbeing', 'lifestyle', 'routine',
        'sleep', 'rest', 'relaxation', 'stress management',
        
        # Ayurvedic treatments
        'herbal', 'herbs', 'spices', 'turmeric', 'ginger',
        'ashwagandha', 'triphala', 'brahmi', 'tulsi',
        'ghee', 'oil massage', 'detox', 'cleanse',
        
        # General health
        'weight loss', 'weight gain', 'body type',
        'energy', 'vitality', 'balance', 'harmony'
    }
    
    def __init__(self):
        """Initialize query classifier"""
        self.medical_pattern = self._compile_pattern(self.MEDICAL_KEYWORDS)
        self.ayurvedic_pattern = self._compile_pattern(self.AYURVEDIC_KEYWORDS)
    
    def _compile_pattern(self, keywords: set) -> re.Pattern:
        """Compile regex pattern from keywords"""
        # Sort by length (longest first) to match longer phrases first
        sorted_keywords = sorted(keywords, key=len, reverse=True)
        # Escape special regex characters and join with |
        pattern = '|'.join(re.escape(kw) for kw in sorted_keywords)
        return re.compile(r'\b(' + pattern + r')\b', re.IGNORECASE)
    
    def classify(self, query: str) -> Tuple[str, float, Dict[str, Any]]:
        """
        Classify query to determine which model to use
        
        Args:
            query: User's query text
            
        Returns:
            Tuple of (model_type, confidence, metadata)
            - model_type: 'medical', 'ayurvedic', or 'general'
            - confidence: 0.0 to 1.0
            - metadata: Additional classification info
        """
        query_lower = query.lower()
        
        # Count keyword matches
        medical_matches = self.medical_pattern.findall(query_lower)
        ayurvedic_matches = self.ayurvedic_pattern.findall(query_lower)
        
        medical_score = len(medical_matches)
        ayurvedic_score = len(ayurvedic_matches)
        
        # Determine classification
        if medical_score > ayurvedic_score:
            confidence = min(0.95, 0.6 + (medical_score * 0.1))
            return 'medical', confidence, {
                'matched_keywords': medical_matches[:5],  # Top 5 matches
                'medical_score': medical_score,
                'ayurvedic_score': ayurvedic_score
            }
        
        elif ayurvedic_score > medical_score:
            confidence = min(0.95, 0.6 + (ayurvedic_score * 0.1))
            return 'ayurvedic', confidence, {
                'matched_keywords': ayurvedic_matches[:5],
                'medical_score': medical_score,
                'ayurvedic_score': ayurvedic_score
            }
        
        elif medical_score == ayurvedic_score and medical_score > 0:
            # Both have matches - this is a hybrid query
            return 'hybrid', 0.8, {
                'matched_keywords': {
                    'medical': medical_matches[:3],
                    'ayurvedic': ayurvedic_matches[:3]
                },
                'medical_score': medical_score,
                'ayurvedic_score': ayurvedic_score
            }
        
        else:
            # No clear matches - general query
            return 'general', 0.5, {
                'matched_keywords': [],
                'medical_score': 0,
                'ayurvedic_score': 0
            }
    
    def should_use_med_gemma(self, query: str, threshold: float = 0.6) -> bool:
        """
        Determine if Med-Gemma should be used for this query
        
        Args:
            query: User's query
            threshold: Confidence threshold (default 0.6)
            
        Returns:
            True if Med-Gemma should be used
        """
        model_type, confidence, _ = self.classify(query)
        
        if model_type == 'medical' and confidence >= threshold:
            return True
        
        if model_type == 'hybrid':
            # For hybrid queries, use Med-Gemma if confidence is high
            return confidence >= 0.75
        
        return False
    
    def get_classification_report(self, query: str) -> Dict[str, Any]:
        """
        Get detailed classification report for debugging
        
        Args:
            query: User's query
            
        Returns:
            Detailed classification information
        """
        model_type, confidence, metadata = self.classify(query)
        
        return {
            'query': query,
            'recommended_model': model_type,
            'confidence': confidence,
            'use_med_gemma': self.should_use_med_gemma(query),
            'metadata': metadata,
            'explanation': self._get_explanation(model_type, confidence, metadata)
        }
    
    def _get_explanation(self, model_type: str, confidence: float, metadata: Dict) -> str:
        """Generate human-readable explanation of classification"""
        if model_type == 'medical':
            keywords = ', '.join(metadata['matched_keywords'][:3])
            return f"Medical query detected (confidence: {confidence:.2f}). Matched keywords: {keywords}"
        
        elif model_type == 'ayurvedic':
            keywords = ', '.join(metadata['matched_keywords'][:3])
            return f"Ayurvedic/wellness query detected (confidence: {confidence:.2f}). Matched keywords: {keywords}"
        
        elif model_type == 'hybrid':
            return f"Hybrid query with both medical and Ayurvedic elements (confidence: {confidence:.2f})"
        
        else:
            return f"General query - no strong medical or Ayurvedic indicators (confidence: {confidence:.2f})"


# Singleton instance
_query_classifier = None

def get_query_classifier() -> QueryClassifier:
    """Get or create query classifier singleton"""
    global _query_classifier
    
    if _query_classifier is None:
        _query_classifier = QueryClassifier()
    
    return _query_classifier
