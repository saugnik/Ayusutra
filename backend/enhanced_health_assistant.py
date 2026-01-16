"""
Enhanced Health Assistant Service
Provides conversational AI, personalized diet plans, and workout recommendations
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize Gemini
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    logger.warning("Google API key not found")
    model = None


class ConversationalHealthAssistant:
    """
    Advanced health assistant that asks clarifying questions and provides
    personalized recommendations
    """
    
    def __init__(self):
        self.conversation_context = {}
    
    def needs_clarification(self, query: str, user_profile: Dict[str, Any]) -> Optional[Dict[str, List[str]]]:
        """
        Determine if clarifying questions are needed
        Returns dict with categorized questions, or None if no clarification needed
        """
        query_lower = query.lower()
        questions = {
            'basic_info': [],
            'diet_info': [],
            'fitness_info': []
        }
        
        # Check for diet-related queries
        if any(word in query_lower for word in ['diet', 'food', 'eat', 'nutrition', 'meal', 'weight']):
            # Basic info
            if not user_profile.get('weight'):
                questions['basic_info'].append("What is your current weight (in kg)?")
            if not user_profile.get('height'):
                questions['basic_info'].append("What is your height (in cm)?")
            if not user_profile.get('age'):
                questions['basic_info'].append("What is your age?")
            
            # Diet-specific info
            if not user_profile.get('activity_level'):
                questions['diet_info'].append("What is your activity level?\n   • Sedentary\n   • Lightly active\n   • Moderately active\n   • Very active\n   • Extremely active")
            if not user_profile.get('dietary_goal'):
                questions['diet_info'].append("What is your primary goal?\n   • Weight loss\n   • Weight gain\n   • Muscle building\n   • Maintenance\n   • Health improvement")
            if not user_profile.get('dietary_restrictions'):
                questions['diet_info'].append("Do you have any dietary restrictions or allergies?")
        
        # Check for workout-related queries
        if any(word in query_lower for word in ['workout', 'exercise', 'gym', 'fitness', 'yoga', 'training']):
            # Fitness-specific info
            if not user_profile.get('fitness_level'):
                questions['fitness_info'].append("What is your current fitness level?\n   • Beginner\n   • Intermediate\n   • Advanced")
            if not user_profile.get('workout_goal'):
                questions['fitness_info'].append("What is your fitness goal?\n   • Strength\n   • Endurance\n   • Flexibility\n   • Weight loss\n   • General fitness")
            if not user_profile.get('available_time'):
                questions['fitness_info'].append("How much time can you dedicate to workouts per day? (in minutes)")
            if not user_profile.get('equipment_access'):
                questions['fitness_info'].append("Do you have access to a gym or prefer home workouts?")
        
        # Check if any questions were added
        has_questions = any(questions[cat] for cat in questions)
        return questions if has_questions else None
    
    def generate_diet_plan(self, user_profile: Dict[str, Any], dosha_analysis: Dict[str, int]) -> Dict[str, Any]:
        """
        Generate personalized diet plan based on user profile and dosha
        """
        weight = user_profile.get('weight', 70)
        height = user_profile.get('height', 170)
        activity_level = user_profile.get('activity_level', 'moderately active')
        goal = user_profile.get('dietary_goal', 'maintenance')
        restrictions = user_profile.get('dietary_restrictions', [])
        
        # Calculate BMI
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        # Calculate daily calorie needs
        bmr = 10 * weight + 6.25 * height - 5 * user_profile.get('age', 30) + 5  # Mifflin-St Jeor for men
        
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly active': 1.375,
            'moderately active': 1.55,
            'very active': 1.725,
            'extremely active': 1.9
        }
        
        tdee = bmr * activity_multipliers.get(activity_level, 1.55)
        
        # Adjust for goal
        if goal == 'weight loss':
            target_calories = tdee - 500
        elif goal == 'weight gain' or goal == 'muscle building':
            target_calories = tdee + 300
        else:
            target_calories = tdee
        
        # Determine dominant dosha
        dominant_dosha = max(dosha_analysis, key=dosha_analysis.get)
        
        # Dosha-specific food recommendations
        dosha_foods = {
            'vata': {
                'favor': ['Warm cooked foods', 'Sweet fruits (bananas, berries)', 'Cooked vegetables', 'Whole grains (rice, oats)', 'Nuts and seeds', 'Ghee and oils', 'Warm milk', 'Root vegetables'],
                'avoid': ['Cold foods', 'Raw vegetables', 'Dry foods', 'Caffeine', 'Beans (except mung)'],
                'spices': ['Ginger', 'Cinnamon', 'Cardamom', 'Cumin', 'Black pepper']
            },
            'pitta': {
                'favor': ['Cool foods', 'Sweet fruits (melons, grapes)', 'Leafy greens', 'Cucumber', 'Coconut', 'Milk', 'Whole grains', 'Legumes'],
                'avoid': ['Spicy foods', 'Sour fruits', 'Tomatoes', 'Garlic', 'Onions', 'Red meat', 'Alcohol'],
                'spices': ['Coriander', 'Fennel', 'Cardamom', 'Turmeric', 'Mint']
            },
            'kapha': {
                'favor': ['Light foods', 'Pungent vegetables', 'Leafy greens', 'Apples', 'Pears', 'Legumes', 'Spices', 'Honey'],
                'avoid': ['Heavy foods', 'Dairy', 'Fried foods', 'Sweet foods', 'Cold foods', 'Excessive salt'],
                'spices': ['Ginger', 'Black pepper', 'Cayenne', 'Turmeric', 'Mustard']
            }
        }
        
        foods = dosha_foods.get(dominant_dosha, dosha_foods['vata'])
        
        # Sample meal plan
        meal_plan = {
            'breakfast': self._generate_meal('breakfast', dominant_dosha, target_calories * 0.25),
            'lunch': self._generate_meal('lunch', dominant_dosha, target_calories * 0.40),
            'dinner': self._generate_meal('dinner', dominant_dosha, target_calories * 0.30),
            'snacks': self._generate_meal('snacks', dominant_dosha, target_calories * 0.05)
        }
        
        return {
            'bmi': round(bmi, 1),
            'bmr': round(bmr),
            'tdee': round(tdee),
            'target_calories': round(target_calories),
            'dominant_dosha': dominant_dosha,
            'macros': {
                'protein': f"{round(target_calories * 0.30 / 4)}g (30%)",
                'carbs': f"{round(target_calories * 0.40 / 4)}g (40%)",
                'fats': f"{round(target_calories * 0.30 / 9)}g (30%)"
            },
            'foods_to_favor': foods['favor'],
            'foods_to_avoid': foods['avoid'],
            'recommended_spices': foods['spices'],
            'meal_plan': meal_plan,
            'hydration': f"{round(weight * 0.033, 1)}L per day",
            'meal_timing': {
                'breakfast': '7:00-8:00 AM',
                'lunch': '12:00-1:00 PM',
                'dinner': '6:00-7:00 PM'
            }
        }
    
    def _generate_meal(self, meal_type: str, dosha: str, calories: float) -> Dict[str, Any]:
        """Generate sample meal based on dosha and calorie target"""
        meals = {
            'vata': {
                'breakfast': 'Warm oatmeal with almonds, dates, and cinnamon',
                'lunch': 'Kitchari (rice and mung dal) with ghee and steamed vegetables',
                'dinner': 'Vegetable soup with whole grain bread and avocado',
                'snacks': 'Warm milk with turmeric or handful of soaked nuts'
            },
            'pitta': {
                'breakfast': 'Coconut chia pudding with sweet fruits',
                'lunch': 'Quinoa salad with cucumber, mint, and cooling herbs',
                'dinner': 'Steamed vegetables with basmati rice and coconut chutney',
                'snacks': 'Fresh fruit smoothie or coconut water'
            },
            'kapha': {
                'breakfast': 'Light vegetable poha or upma with ginger tea',
                'lunch': 'Mixed vegetable curry with millet and minimal oil',
                'dinner': 'Clear vegetable soup with quinoa',
                'snacks': 'Apple with cinnamon or herbal tea'
            }
        }
        
        return {
            'suggestion': meals.get(dosha, meals['vata']).get(meal_type, 'Balanced meal'),
            'calories': round(calories),
            'timing': self._get_meal_timing(meal_type)
        }
    
    def _get_meal_timing(self, meal_type: str) -> str:
        """Get recommended timing for meal"""
        timings = {
            'breakfast': '7:00-8:00 AM',
            'lunch': '12:00-1:00 PM',
            'dinner': '6:00-7:00 PM',
            'snacks': 'Mid-morning or evening'
        }
        return timings.get(meal_type, 'As needed')
    
    def generate_workout_plan(self, user_profile: Dict[str, Any], dosha_analysis: Dict[str, int]) -> Dict[str, Any]:
        """
        Generate personalized workout plan based on user profile and dosha
        """
        fitness_level = user_profile.get('fitness_level', 'beginner')
        goal = user_profile.get('workout_goal', 'general fitness')
        available_time = user_profile.get('available_time', 30)
        equipment = user_profile.get('equipment_access', 'home')
        
        # Determine dominant dosha
        dominant_dosha = max(dosha_analysis, key=dosha_analysis.get)
        
        # Dosha-specific workout recommendations
        dosha_workouts = {
            'vata': {
                'style': 'Gentle, grounding, and calming',
                'recommended': ['Hatha Yoga', 'Tai Chi', 'Swimming', 'Walking', 'Light strength training'],
                'avoid': ['Intense cardio', 'Excessive jumping', 'Overly competitive sports'],
                'duration': '30-45 minutes',
                'frequency': '4-5 days per week'
            },
            'pitta': {
                'style': 'Moderate intensity, cooling, and non-competitive',
                'recommended': ['Swimming', 'Cycling', 'Moderate yoga', 'Hiking', 'Team sports (non-competitive)'],
                'avoid': ['Hot yoga', 'Intense competition', 'Excessive heat'],
                'duration': '45-60 minutes',
                'frequency': '5-6 days per week'
            },
            'kapha': {
                'style': 'Vigorous, stimulating, and energizing',
                'recommended': ['Running', 'HIIT', 'Ashtanga Yoga', 'Dance', 'Martial arts', 'Weight training'],
                'avoid': ['Excessive rest', 'Slow movements', 'Water retention activities'],
                'duration': '60-90 minutes',
                'frequency': '6-7 days per week'
            }
        }
        
        workout_info = dosha_workouts.get(dominant_dosha, dosha_workouts['vata'])
        
        # Generate weekly plan
        weekly_plan = self._generate_weekly_workout(fitness_level, goal, available_time, equipment, dominant_dosha)
        
        # Yoga recommendations
        yoga_sequence = self._get_yoga_sequence(dominant_dosha, available_time)
        
        return {
            'dominant_dosha': dominant_dosha,
            'workout_style': workout_info['style'],
            'recommended_activities': workout_info['recommended'],
            'activities_to_avoid': workout_info['avoid'],
            'recommended_duration': workout_info['duration'],
            'recommended_frequency': workout_info['frequency'],
            'weekly_plan': weekly_plan,
            'yoga_sequence': yoga_sequence,
            'warm_up': 'Always start with 5-10 minutes of light cardio and dynamic stretching',
            'cool_down': 'End with 5-10 minutes of static stretching and deep breathing',
            'rest_days': 'Include 1-2 rest days per week for recovery'
        }
    
    def _generate_weekly_workout(self, level: str, goal: str, time: int, equipment: str, dosha: str) -> Dict[str, str]:
        """Generate weekly workout schedule"""
        if dosha == 'vata':
            return {
                'Monday': 'Gentle Hatha Yoga (30 min) + Walking (15 min)',
                'Tuesday': 'Light strength training - Upper body (30 min)',
                'Wednesday': 'Swimming or Water aerobics (30 min)',
                'Thursday': 'Yoga for grounding (30 min) + Meditation (10 min)',
                'Friday': 'Light strength training - Lower body (30 min)',
                'Saturday': 'Nature walk or Tai Chi (40 min)',
                'Sunday': 'Rest or gentle stretching (20 min)'
            }
        elif dosha == 'pitta':
            return {
                'Monday': 'Moderate cycling (40 min)',
                'Tuesday': 'Vinyasa Yoga (45 min)',
                'Wednesday': 'Swimming (45 min)',
                'Thursday': 'Hiking or brisk walking (50 min)',
                'Friday': 'Strength training - Full body (40 min)',
                'Saturday': 'Team sport or recreational activity (60 min)',
                'Sunday': 'Restorative yoga or rest'
            }
        else:  # kapha
            return {
                'Monday': 'HIIT workout (30 min) + Core exercises (15 min)',
                'Tuesday': 'Ashtanga Yoga or Power Yoga (60 min)',
                'Wednesday': 'Running intervals (40 min)',
                'Thursday': 'Weight training - Upper body (45 min)',
                'Friday': 'Dance or Zumba (60 min)',
                'Saturday': 'Weight training - Lower body (45 min) + Cardio (20 min)',
                'Sunday': 'Active recovery - Light jog or yoga (30 min)'
            }
    
    def _get_yoga_sequence(self, dosha: str, duration: int) -> List[str]:
        """Get dosha-specific yoga sequence"""
        sequences = {
            'vata': [
                'Mountain Pose (Tadasana) - 2 min',
                'Cat-Cow Stretch - 3 min',
                'Child\'s Pose - 3 min',
                'Seated Forward Bend - 3 min',
                'Legs Up the Wall - 5 min',
                'Corpse Pose (Savasana) - 5 min'
            ],
            'pitta': [
                'Moon Salutation - 5 min',
                'Standing Forward Bend - 3 min',
                'Seated Twist - 3 min each side',
                'Bridge Pose - 3 min',
                'Fish Pose - 2 min',
                'Corpse Pose - 5 min'
            ],
            'kapha': [
                'Sun Salutation A - 10 min',
                'Warrior Sequence - 5 min',
                'Triangle Pose - 2 min each side',
                'Boat Pose - 3 min',
                'Bow Pose - 3 min',
                'Headstand or Shoulder Stand - 3 min',
                'Corpse Pose - 3 min'
            ]
        }
        return sequences.get(dosha, sequences['vata'])
    
    async def generate_conversational_response(
        self,
        query: str,
        user_profile: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        dosha_analysis: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Generate intelligent conversational response with Actions
        """
        query_lower = query.lower()
        actions = []
        
        # 1. Intent: Water / Hydration
        if any(w in query_lower for w in ['water', 'hydrate', 'drink']):
             # Suggest setting water reminders
             actions.append({
                 "type": "create_reminder",
                 "label": "Set Water Reminders (Every 2 hours)",
                 "data": {
                     "title": "Drink Water",
                     "message": "Time to hydrate! Drink a glass of water.",
                     "frequency": "daily",
                     "time": "09:00,11:00,13:00,15:00,17:00,19:00" # Frontend handle split or backend loop
                 }
             })

        # 2. Intent: Weight Loss / Exercise
        if any(w in query_lower for w in ['weight', 'fat', 'lose', 'slim', 'exercise', 'workout']):
             # Calculate generic schedule based on profile (or default)
             actions.append({
                 "type": "create_reminder",
                 "label": "Set Daily Morning Workout (7:00 AM)",
                 "data": {
                     "title": "Morning Workout",
                     "message": "Time for your weight loss exercises!",
                     "frequency": "daily",
                     "time": "07:00"
                 }
             })
             
             # Also suggest generating a full plan (existing logic reused)
             workout_plan = self.generate_workout_plan(user_profile, dosha_analysis)
             # We could embed or just talk about it.

        # 3. Intent: Medical Help / Doctor
        if any(w in query_lower for w in ['doctor', 'pain', 'sick', 'ill', 'fever', 'appointment', 'consult']):
             # Suggest finding a doctor
             actions.append({
                 "type": "find_practitioner",
                 "label": "Find a Practitioner",
                 "data": {
                     "specialization": "General" if "pain" not in query_lower else "Specialist"
                 }
             })

        # Generate text response using Gemini or Templates
        conversation_context = f"""
        User Profile: {user_profile}
        Dosha: {dosha_analysis}
        Query: {query}
        Actions Proposed: {[a['label'] for a in actions]}
        """
        
        reply_text = ""
        if model:
            try:
                base_prompt = "You are a helpful AyurSutra Health Agent. The user asked: " + query + ". "
                if actions:
                    base_prompt += f"You have proposed these actions: {[a['label'] for a in actions]}. Explain why they are good."
                else:
                    base_prompt += "Provide helpful health advice."
                
                resp = model.generate_content(base_prompt)
                reply_text = resp.text
            except Exception as e:
                logger.error(f"Gemini Error: {e}")
                reply_text = "I can help you with that. I've also suggested some actions for you below."
        else:
             reply_text = "I've analyzed your request. Please check the suggested actions below."

        return {
            'reply': reply_text,
            'actions': actions,
            'conversation_id': "new" # Maintain ID in caller
        }


# Singleton instance
health_assistant = ConversationalHealthAssistant()
