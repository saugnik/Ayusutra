"""
Enhanced Health Assistant Service
Provides conversational AI, personalized diet plans, and workout recommendations
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import google.generativeai as genai

# Import Med-Gemma and Query Classifier
from med_gemma_service import get_med_gemma_service
from query_classifier import get_query_classifier

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

class FoodDatabase:
    """
    Comprehensive Database of Foods with Metabolic & Ayurvedic Properties.
    Acts as the 'Knowledge Graph' for the Nutritional Engine.
    """
    def __init__(self):
        # Format: Item: {Calories/100g, Protein, Carbs, Fats, GI, Dosha_Impact, Tags}
        self.db = {
            # --- PROTEIN SOURCES ---
            'Chicken Breast': {'cal': 165, 'p': 31, 'c': 0, 'f': 3.6, 'gi': 0, 'dosha': {'vata': 'neutral', 'pitta': 'neutral', 'kapha': 'good'}, 'tags': ['meat', 'lean']},
            'Chicken Thigh': {'cal': 209, 'p': 26, 'c': 0, 'f': 10.9, 'gi': 0, 'dosha': {'vata': 'good', 'pitta': 'bad', 'kapha': 'bad'}, 'tags': ['meat']},
            'Salmon': {'cal': 208, 'p': 20, 'c': 0, 'f': 13, 'gi': 0, 'dosha': {'vata': 'good', 'pitta': 'bad', 'kapha': 'good'}, 'tags': ['fish', 'fatty_fish', 'omega3']},
            'Tuna': {'cal': 132, 'p': 28, 'c': 0, 'f': 1, 'gi': 0, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['fish', 'lean']},
            'Eggs': {'cal': 155, 'p': 13, 'c': 1.1, 'f': 11, 'gi': 0, 'dosha': {'vata': 'good', 'pitta': 'neutral', 'kapha': 'bad'}, 'tags': ['vegetarian', 'eggs']},
            'Egg Whites': {'cal': 52, 'p': 11, 'c': 0.7, 'f': 0.2, 'gi': 0, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegetarian', 'lean']},
            'Tofu': {'cal': 76, 'p': 8, 'c': 1.9, 'f': 4.8, 'gi': 15, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'plant_protein', 'soy']},
            'Tempeh': {'cal': 192, 'p': 20.3, 'c': 7.6, 'f': 10.8, 'gi': 15, 'dosha': {'vata': 'neutral', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'plant_protein', 'fermented']},
            'Lentils (Cooked)': {'cal': 116, 'p': 9, 'c': 20, 'f': 0.4, 'gi': 29, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'legume']},
            'Chickpeas (Cooked)': {'cal': 164, 'p': 8.9, 'c': 27.4, 'f': 2.6, 'gi': 28, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'legume']},
            'Moong Dal': {'cal': 105, 'p': 7, 'c': 18, 'f': 0.3, 'gi': 25, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'legume', 'tridoshic']},
            'Paneer': {'cal': 265, 'p': 18, 'c': 1.2, 'f': 20.8, 'gi': 20, 'dosha': {'vata': 'good', 'pitta': 'bad', 'kapha': 'bad'}, 'tags': ['vegetarian', 'dairy']},
            'Greek Yogurt': {'cal': 59, 'p': 10, 'c': 3.6, 'f': 0.4, 'gi': 12, 'dosha': {'vata': 'good', 'pitta': 'neutral', 'kapha': 'bad'}, 'tags': ['vegetarian', 'dairy', 'probiotic']},

            # --- GRAINS & CARBS ---
            'Basmati Rice': {'cal': 130, 'p': 2.7, 'c': 28, 'f': 0.3, 'gi': 60, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'bad'}, 'tags': ['vegan', 'grain']},
            'Brown Rice': {'cal': 111, 'p': 2.6, 'c': 23, 'f': 0.9, 'gi': 50, 'dosha': {'vata': 'neutral', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'grain', 'fiber']},
            'Quinoa': {'cal': 120, 'p': 4.4, 'c': 21.3, 'f': 1.9, 'gi': 53, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'grain', 'high_protein']},
            'Oats': {'cal': 68, 'p': 2.4, 'c': 12, 'f': 1.4, 'gi': 55, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'bad'}, 'tags': ['vegan', 'grain']},
            'Sweet Potato': {'cal': 86, 'p': 1.6, 'c': 20.1, 'f': 0.1, 'gi': 61, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'bad'}, 'tags': ['vegan', 'vegetable', 'starchy']},
            'Potato': {'cal': 77, 'p': 2, 'c': 17, 'f': 0.1, 'gi': 80, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'bad'}, 'tags': ['vegan', 'vegetable', 'starchy']},
            'Barley': {'cal': 123, 'p': 2.3, 'c': 28, 'f': 0.4, 'gi': 28, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'grain']},
            'Millet': {'cal': 119, 'p': 3.5, 'c': 23.7, 'f': 1, 'gi': 71, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'grain', 'drying']},

            # --- VEGETABLES ---
            'Spinach': {'cal': 23, 'p': 2.9, 'c': 3.6, 'f': 0.4, 'gi': 15, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'vegetable', 'leafy']},
            'Kale': {'cal': 49, 'p': 4.3, 'c': 8.8, 'f': 0.9, 'gi': 5, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'vegetable', 'leafy']},
            'Broccoli': {'cal': 34, 'p': 2.8, 'c': 6.6, 'f': 0.4, 'gi': 15, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'vegetable', 'cruciferous']},
            'Carrots': {'cal': 41, 'p': 0.9, 'c': 9.6, 'f': 0.2, 'gi': 39, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'bad'}, 'tags': ['vegan', 'vegetable']},
            'Cucumber': {'cal': 15, 'p': 0.7, 'c': 3.6, 'f': 0.1, 'gi': 15, 'dosha': {'vata': 'neutral', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'vegetable', 'cooling']},
            'Bitter Gourd': {'cal': 17, 'p': 1, 'c': 3.7, 'f': 0.2, 'gi': 10, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'vegetable', 'bitter', 'diabetes_friendly']},
            'Okra': {'cal': 33, 'p': 1.9, 'c': 7.5, 'f': 0.2, 'gi': 20, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'vegetable']},
            'Zucchini': {'cal': 17, 'p': 1.2, 'c': 3.1, 'f': 0.3, 'gi': 15, 'dosha': {'vata': 'neutral', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'vegetable']},

            # --- FRUITS ---
            'Apple': {'cal': 52, 'p': 0.3, 'c': 14, 'f': 0.2, 'gi': 36, 'dosha': {'vata': 'bad', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'fruit']},
            'Banana': {'cal': 89, 'p': 1.1, 'c': 22.8, 'f': 0.3, 'gi': 51, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'bad'}, 'tags': ['vegan', 'fruit', 'sweet']},
            'Berries': {'cal': 57, 'p': 0.7, 'c': 14, 'f': 0.3, 'gi': 25, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'good'}, 'tags': ['vegan', 'fruit', 'antioxidant']},
            'Mango': {'cal': 60, 'p': 0.8, 'c': 15, 'f': 0.4, 'gi': 51, 'dosha': {'vata': 'good', 'pitta': 'bad', 'kapha': 'bad'}, 'tags': ['vegan', 'fruit', 'sweet']},

            # --- FATS & OILS ---
            'Almonds': {'cal': 579, 'p': 21, 'c': 22, 'f': 50, 'gi': 0, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'bad'}, 'tags': ['vegan', 'nut']},
            'Walnuts': {'cal': 654, 'p': 15, 'c': 14, 'f': 65, 'gi': 0, 'dosha': {'vata': 'good', 'pitta': 'neutral', 'kapha': 'bad'}, 'tags': ['vegan', 'nut', 'omega3']},
            'Ghee': {'cal': 900, 'p': 0, 'c': 0, 'f': 100, 'gi': 0, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'neutral'}, 'tags': ['vegetarian', 'fat']},
            'Coconut Oil': {'cal': 862, 'p': 0, 'c': 0, 'f': 100, 'gi': 0, 'dosha': {'vata': 'good', 'pitta': 'good', 'kapha': 'bad'}, 'tags': ['vegan', 'fat', 'cooling']},
            'Olive Oil': {'cal': 884, 'p': 0, 'c': 0, 'f': 100, 'gi': 0, 'dosha': {'vata': 'good', 'pitta': 'neutral', 'kapha': 'neutral'}, 'tags': ['vegan', 'fat']},
        }
    
    def get_foods_by_macro(self, macro_type: str, limit: int = 100) -> List[Dict]:
        """Filter foods primarily rich in protein, carbs, or fats"""
        if macro_type == 'protein':
            return [k for k, v in self.db.items() if v['p'] > 10]
        elif macro_type == 'carbs':
            return [k for k, v in self.db.items() if v['c'] > 15]
        elif macro_type == 'fats':
            return [k for k, v in self.db.items() if v['f'] > 10]
        return []

    def filter_foods(self, dosha: str, restrictions: List[str], conditions: List[str]) -> Dict[str, List[str]]:
        """Comprehensive filtering logic"""
        allowed = {'protein': [], 'carbs': [], 'veggies': [], 'fats': [], 'fruits': []}
        
        for food, data in self.db.items():
            # 1. Restriction Check
            if 'vegetarian' in restrictions and 'meat' in data['tags']: continue
            if 'vegetarian' in restrictions and 'fish' in data['tags']: continue
            if 'vegan' in restrictions and ('meat' in data['tags'] or 'dairy' in data['tags'] or 'eggs' in data['tags']): continue
            if 'keto' in restrictions and data['c'] > 10: continue # Strict Keto
            if 'gluten-free' in restrictions and food in ['Barley', 'Wheat', 'Rye']: continue # Simple list for now
            
            # 2. Condition Check
            if 'diabetes' in conditions and (data['gi'] > 55 or 'sweet' in data['tags']): continue
            if 'hypertension' in conditions and 'processed' in data['tags']: continue # Assuming DB updated with processed tag
            if 'thyroid' in conditions and 'cruciferous' in data['tags']: continue # Raw concern, but filtering for safety
            
            # 3. Dosha Check (Soft Filter - prioritize 'good' or 'neutral')
            if data['dosha'][dosha] == 'bad': continue 

            # 4. Categorize
            if 'meat' in data['tags'] or 'fish' in data['tags'] or data['p'] > 15: allowed['protein'].append(food)
            elif 'vegetable' in data['tags']: allowed['veggies'].append(food)
            elif 'fruit' in data['tags']: allowed['fruits'].append(food)
            elif 'fat' in data['tags'] or 'nut' in data['tags']: allowed['fats'].append(food)
            elif 'grain' in data['tags'] or data['c'] > 15: allowed['carbs'].append(food)
            
        return allowed

# Initialize Gemini

class NutritionalEngine:
    """
    Advanced Logic for calculating precise nutrition and constructing meals
    """
    def __init__(self):
        self.food_db = FoodDatabase()
        
    def calculate_needs(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate TDEE, BMR, and Macro split based on advanced formulas"""
        weight = profile.get('weight', 70)
        height = profile.get('height', 170)
        age = profile.get('age', 30)
        gender = profile.get('gender', 'female')
        activity = profile.get('activity_level', 'moderately active')
        goal = profile.get('dietary_goal', 'maintenance')
        
        # Harris-Benedict Refined
        if gender == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
        # Activity Multipliers
        multipliers = {
            'sedentary': 1.2,
            'lightly active': 1.375,
            'moderately active': 1.55,
            'very active': 1.725,
            'extremely active': 1.9
        }
        tdee = bmr * multipliers.get(activity, 1.55)
        
        # Goal Calculus
        if goal == 'weight loss':
            target = tdee * 0.80 # 20% deficit
            macros = {'p': 0.40, 'c': 0.30, 'f': 0.30}
        elif goal == 'muscle building':
            target = tdee * 1.10 # 10% surplus
            macros = {'p': 0.30, 'c': 0.45, 'f': 0.25}
        else:
            target = tdee
            macros = {'p': 0.30, 'c': 0.40, 'f': 0.30}
            
        return {
            'target_calories': int(target),
            'bmr': int(bmr),
            'tdee': int(tdee),
            'macros_grams': {
                'protein': int((target * macros['p']) / 4),
                'carbs': int((target * macros['c']) / 4),
                'fat': int((target * macros['f']) / 9)
            }
        }

    def generate_day_plan(self, profile: Dict[str, Any], dosha: str) -> Dict[str, Any]:
        """Construct a full day of eating using component-based logic"""
        needs = self.calculate_needs(profile)
        restrictions = profile.get('dietary_restrictions', [])
        conditions = profile.get('medical_conditions', [])
        
        # Get allowed foods
        allowed_foods = self.food_db.filter_foods(dosha, restrictions, conditions)
        
        # Check if lists are empty (fallback to generic if strict filters remove everything)
        import random
        def pick(category):
            if allowed_foods[category]: 
                return random.choice(allowed_foods[category])
            return f"Generic {category} (Database Empty)"

        # Meal Construction Logic
        # Breakfast: Protein + Carb + Fruit/Veg
        breakfast = f"{pick('protein')} with {pick('carbs')} and {pick('fruits')}"
        
        # Lunch: Protein + Carb + Veg + Fat
        lunch = f"{pick('protein')} bowl with {pick('carbs')}, steamed {pick('veggies')}, dressed with {pick('fats')}"
        
        # Dinner: Protein + Veg + Fat (Low Carb typically)
        dinner = f"Grilled/Baked {pick('protein')} with a large serving of {pick('veggies')} cooked in {pick('fats')}"
        
        # Snack: Fruit + Fat or Protein
        snack = f"{pick('fruits')} with {pick('fats')}"

        return {
            'metrics': needs,
            'meals': {
                'breakfast': {'item': breakfast, 'cal': int(needs['target_calories'] * 0.25)},
                'lunch': {'item': lunch, 'cal': int(needs['target_calories'] * 0.35)},
                'dinner': {'item': dinner, 'cal': int(needs['target_calories'] * 0.30)},
                'snacks': {'item': snack, 'cal': int(needs['target_calories'] * 0.10)}
            }
        }



class ExerciseDatabase:
    """Comprehensive Exercise Library with biomechanical metadata"""
    def __init__(self):
        self.db = {
            # --- CHEST ---
            'Pushups': {'type': 'push', 'target': 'chest', 'level': 'beginner', 'equip': 'bodyweight', 'impact': 'low'},
            'Bench Press': {'type': 'push', 'target': 'chest', 'level': 'intermediate', 'equip': 'gym', 'impact': 'medium'},
            'Dumbbell Flys': {'type': 'push', 'target': 'chest', 'level': 'beginner', 'equip': 'dumbbell', 'impact': 'low'},
            
            # --- BACK ---
            'Pullups': {'type': 'pull', 'target': 'back', 'level': 'advanced', 'equip': 'bar', 'impact': 'medium'},
            'Dumbbell Rows': {'type': 'pull', 'target': 'back', 'level': 'beginner', 'equip': 'dumbbell', 'impact': 'low'},
            'Lat Pulldowns': {'type': 'pull', 'target': 'back', 'level': 'beginner', 'equip': 'gym', 'impact': 'low'},
            
            # --- LEGS ---
            'Squats': {'type': 'legs', 'target': 'quads', 'level': 'intermediate', 'equip': 'bodyweight', 'impact': 'medium'},
            'Lunges': {'type': 'legs', 'target': 'quads', 'level': 'beginner', 'equip': 'bodyweight', 'impact': 'medium'},
            'Deadlifts': {'type': 'legs', 'target': 'hamstrings', 'level': 'advanced', 'equip': 'gym', 'impact': 'high'},
            'Leg Press': {'type': 'legs', 'target': 'quads', 'level': 'beginner', 'equip': 'gym', 'impact': 'low'},
            
            # --- SHOULDERS ---
            'Overhead Press': {'type': 'push', 'target': 'shoulders', 'level': 'intermediate', 'equip': 'dumbbell', 'impact': 'medium'},
            'Lateral Raises': {'type': 'push', 'target': 'shoulders', 'level': 'beginner', 'equip': 'dumbbell', 'impact': 'low'},
            
            # --- ARMS ---
            'Bicep Curls': {'type': 'pull', 'target': 'biceps', 'level': 'beginner', 'equip': 'dumbbell', 'impact': 'low'},
            'Tricep Dips': {'type': 'push', 'target': 'triceps', 'level': 'intermediate', 'equip': 'bodyweight', 'impact': 'low'},
            
            # --- CARDIO ---
            'Running': {'type': 'cardio', 'target': 'cardio', 'level': 'intermediate', 'equip': 'none', 'impact': 'high'},
            'Walking': {'type': 'cardio', 'target': 'cardio', 'level': 'beginner', 'equip': 'none', 'impact': 'low'},
            'Cycling': {'type': 'cardio', 'target': 'cardio', 'level': 'beginner', 'equip': 'bike', 'impact': 'low'},
            'Burpees': {'type': 'cardio', 'target': 'hiit', 'level': 'advanced', 'equip': 'none', 'impact': 'high'},
            'Swimming': {'type': 'cardio', 'target': 'full_body', 'level': 'intermediate', 'equip': 'pool', 'impact': 'low'},
        }
        
    def get_exercises(self, criteria: Dict[str, Any]) -> List[str]:
        """Filter exercises based on criteria"""
        filtered = []
        for name, data in self.db.items():
            if criteria.get('equip') == 'home' and data['equip'] == 'gym': continue
            if criteria.get('impact') == 'low' and data['impact'] == 'high': continue
            if criteria.get('level') == 'beginner' and data['level'] == 'advanced': continue
            
            target = criteria.get('target_group')
            if target and data['type'] != target and data['target'] != target: continue
            
            filtered.append(name)
        return filtered

class WorkoutEngine:
    """Advanced Training Logic for Periodization and Splits"""
    def __init__(self):
        self.ex_db = ExerciseDatabase()
        
    def generate_split(self, profile: Dict[str, Any], dosha: str) -> Dict[str, Any]:
        """Generate a scientific training split"""
        days_available = int(profile.get('frequency', '3 days').split()[0]) if 'frequency' in profile and profile['frequency'] else 3
        goal = profile.get('workout_goal', 'general fitness')
        equipment = profile.get('equipment_access', 'home')
        conditions = profile.get('medical_conditions', [])
        
        # Determine Split Structure
        if days_available <= 3:
            split_type = "Full Body"
            structure = ['Full Body A', 'Rest', 'Full Body B', 'Rest', 'Full Body A', 'Rest', 'Rest']
        elif days_available == 4:
            split_type = "Upper / Lower"
            structure = ['Upper Body', 'Lower Body', 'Rest', 'Upper Body', 'Lower Body', 'Rest', 'Rest']
        else:
            split_type = "Push / Pull / Legs"
            structure = ['Push', 'Pull', 'Legs', 'Push', 'Pull', 'Legs', 'Rest']
            
        # Determine Intensity & Volume based on Dosha & Goal
        if dosha == 'kapha' or goal == 'weight loss':
            sets, reps = 4, "12-15 (High Volume)"
            rest = "60 sec"
        elif dosha == 'vata' or goal == 'strength':
            sets, reps = 3, "6-8 (Heavy)"
            rest = "120 sec"
        else: # Pitta / Hypertrophy
            sets, reps = 3, "8-12 (Moderate)"
            rest = "90 sec"
            
        # Impact check
        impact_preference = 'low' if ('arthritis' in conditions or 'hypertension' in conditions) else 'any'
        
        # Build Weekly Plan
        weekly_plan = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for i, day in enumerate(days):
            workout_name = structure[i]
            if workout_name == 'Rest':
                weekly_plan[day] = "Active Recovery: Walking or Gentle Yoga"
                continue
                
            # Filter exercises for this day
            target_group = None
            if 'Upper' in workout_name: target_group = ['chest', 'back', 'shoulders', 'arms']
            elif 'Lower' in workout_name: target_group = ['legs']
            elif 'Push' in workout_name: target_group = ['push']
            elif 'Pull' in workout_name: target_group = ['pull']
            elif 'Full' in workout_name: target_group = ['push', 'pull', 'legs']
            
            # Select Exercises
            exercises = []
            import random
            
            # Helper to fetch by exact group
            def add_move(grp):
                opts = self.ex_db.get_exercises({'target_group': grp, 'equip': equipment, 'impact': impact_preference})
                if opts: exercises.append(f"{random.choice(opts)} ({sets} sets x {reps})")
            
            if isinstance(target_group, list):
                for grp in target_group: add_move(grp)
            else:
                add_move(target_group)
                
            weekly_plan[day] = f"{workout_name}: " + ", ".join(exercises)
            
        return {
            'structure': split_type,
            'weekly_scedule': weekly_plan,
            'parameters': {'sets': sets, 'reps': reps, 'rest': rest}
        }


class ConversationalHealthAssistant:
    """
    Advanced health assistant that asks clarifying questions and provides
    personalized recommendations
    """
    
    def __init__(self):
        self.conversation_context = {}
        # Initialize Advanced Engines
        self.nutrition_engine = NutritionalEngine()
        self.workout_engine = WorkoutEngine()
        
        # Initialize Hybrid AI System
        self.med_gemma_service = get_med_gemma_service()
        self.query_classifier = get_query_classifier()
        
        logger.info(f"Med-Gemma available: {self.med_gemma_service.is_available()}")
        
    # ... (extract_profile_info and needs_clarification remain same) ...

    def generate_diet_plan(self, user_profile: Dict[str, Any], dosha_analysis: Dict[str, int]) -> Dict[str, Any]:
        """
        Generate robust personalized diet plan using NutritionalEngine
        """
        dominant_dosha = max(dosha_analysis, key=dosha_analysis.get)
        
        # Use the advanced engine
        plan_data = self.nutrition_engine.generate_day_plan(user_profile, dominant_dosha)
        metrics = plan_data['metrics']
        
        # Get dosha specific advice (keep existing small helper or move to DB)
        dosha_foods = self._get_dosha_foods(dominant_dosha)
        
        return {
            'bmi': "Calculated in Engine", # Wrapper to match schema
            'target_calories': metrics['target_calories'],
            'dominant_dosha': dominant_dosha,
            'macros': {
                'protein': f"{metrics['macros_grams']['protein']}g",
                'carbs': f"{metrics['macros_grams']['carbs']}g",
                'fats': f"{metrics['macros_grams']['fat']}g"
            },
            'foods_to_favor': dosha_foods['favor'][:5], # Keep top 5
            'foods_to_avoid': dosha_foods['avoid'][:5],
            'meal_plan': {
                'breakfast': {'suggestion': plan_data['meals']['breakfast']['item'], 'calories': plan_data['meals']['breakfast']['cal']},
                'lunch': {'suggestion': plan_data['meals']['lunch']['item'], 'calories': plan_data['meals']['lunch']['cal']},
                'dinner': {'suggestion': plan_data['meals']['dinner']['item'], 'calories': plan_data['meals']['dinner']['cal']},
                'snacks': {'suggestion': plan_data['meals']['snacks']['item'], 'calories': plan_data['meals']['snacks']['cal']}
            },
            'hydration': "3-4 Liters (Engine Rec)",
            'conditions_considered': user_profile.get('medical_conditions', [])
        }

    def generate_workout_plan(self, user_profile: Dict[str, Any], dosha_analysis: Dict[str, int]) -> Dict[str, Any]:
        """
        Generate personalized workout plan using WorkoutEngine
        """
        dominant_dosha = max(dosha_analysis, key=dosha_analysis.get)
        
        # Use advanced engine
        workout_data = self.workout_engine.generate_split(user_profile, dominant_dosha)
        
        return {
            'dominant_dosha': dominant_dosha,
            'workout_style': f"Split: {workout_data['structure']} ({workout_data['parameters']['reps']} reps)",
            'recommended_activities': ["Detailed in Weekly Plan"], 
            'weekly_plan': workout_data['weekly_scedule'],
            'yoga_sequence': self._get_yoga_sequence(dominant_dosha, 30) # Keep yoga helper
        }
        
    def extract_profile_info(self, query: str) -> Dict[str, Any]:
        """Extract comprehensive user details from natural language query"""
        info = {}
        query_lower = query.lower()
        import re
        
        # 1. Metrics Extraction
        # Weight
        weight_match = re.search(r'(\d+)\s*(?:kg|kgs)', query_lower)
        if weight_match: info['weight'] = float(weight_match.group(1))
        
        # Height
        height_match = re.search(r'(\d+)\s*(?:cm|cms)', query_lower)
        if height_match: info['height'] = float(height_match.group(1))
        
        # Age
        age_match = re.search(r'(\d+)\s*(?:years|yrs|year old)', query_lower)
        if age_match: 
            info['age'] = int(age_match.group(1))
        else:
            # Fallback for "age is 20" or "i am 20"
            age_match_2 = re.search(r'(?:age|i am)\s*(?:is)?\s*(\d+)', query_lower)
            if age_match_2: info['age'] = int(age_match_2.group(1))
        
        # Gender
        if any(w in query_lower for w in ['female', 'woman', 'girl', 'lady']): info['gender'] = 'female'
        elif any(w in query_lower for w in ['male', 'man', 'boy', 'guy']): info['gender'] = 'male'

        # 2. Goal Extraction
        if any(w in query_lower for w in ['lose weight', 'weight loss', 'fat loss', 'slim down']):
            info['dietary_goal'] = 'weight loss'
            info['workout_goal'] = 'weight loss'
        elif any(w in query_lower for w in ['gain weight', 'muscle', 'bulk', 'mass']):
            info['dietary_goal'] = 'muscle building'
            info['workout_goal'] = 'strength'
        elif 'maintain' in query_lower:
             info['dietary_goal'] = 'maintenance'
            
        # 3. Dietary Restrictions Extraction
        restrictions = []
        restriction_map = {
            'vegetarian': ['vegetarian', 'no meat', 'veg'],
            'vegan': ['vegan', 'plant based'],
            'keto': ['keto', 'ketogenic', 'low carb'],
            'gluten-free': ['gluten free', 'no gluten', 'celiac'],
            'dairy-free': ['dairy free', 'no dairy', 'lactose'],
            'nut-free': ['nut free', 'no nuts'],
            'paleo': ['paleo', 'caveman']
        }
        for res, keywords in restriction_map.items():
            if any(k in query_lower for k in keywords):
                restrictions.append(res)
        
        if restrictions:
            info['dietary_restrictions'] = restrictions
            
        # 4. Medical Conditions Extraction
        conditions = []
        condition_map = {
            'diabetes': ['diabetes', 'diabetic', 'sugar', 'insulin'],
            'hypertension': ['bp', 'blood pressure', 'hypertension'],
            'thyroid': ['thyroid', 'hypothyroid', 'hyperthyroid'],
            'pcos': ['pcos', 'pcod'],
            'cholesterol': ['cholesterol', 'high lipid'],
            'arthritis': ['arthritis', 'joint pain']
        }
        for cond, keywords in condition_map.items():
            if any(k in query_lower for k in keywords):
                conditions.append(cond)
        
        if conditions:
            info['medical_conditions'] = conditions
            
        # 5. Activity Level
        if 'sedentary' in query_lower or 'desk job' in query_lower: info['activity_level'] = 'sedentary'
        elif 'lightly' in query_lower or 'walking' in query_lower: info['activity_level'] = 'lightly active'
        elif 'moderate' in query_lower or 'gym' in query_lower: info['activity_level'] = 'moderately active'
        elif 'very active' in query_lower or 'athlete' in query_lower or 'highly active' in query_lower: info['activity_level'] = 'very active'
        
        return info
    
    def needs_clarification(self, query: str, user_profile: Dict[str, Any]) -> Optional[Dict[str, List[str]]]:
        """
        Determine if clarifying questions are needed - ONLY for explicit plan requests
        Returns dict with categorized questions, or None if no clarification needed
        """
        query_lower = query.lower()
        
        # ONLY ask for clarification if user explicitly requests a detailed plan
        plan_keywords = ['diet plan', 'meal plan', 'workout plan', 'exercise plan', 'fitness plan', 
                        'give me a plan', 'create a plan', 'make a plan', 'need a plan']
        is_explicit_plan_request = any(keyword in query_lower for keyword in plan_keywords)
        
        # Skip clarification for general questions, symptoms, or casual queries
        if not is_explicit_plan_request:
            return None
        
        questions = {'basic_info': []}
        
        # Only ask ESSENTIAL missing info for plan generation
        if not user_profile.get('age'):
            questions['basic_info'].append("What is your age?")
        
        # Only ask weight for diet plans
        if 'diet' in query_lower or 'meal' in query_lower or 'food' in query_lower:
            if not user_profile.get('weight'):
                questions['basic_info'].append("What is your weight (in kg)?")
        
        # Return questions only if we have any
        return questions if questions['basic_info'] else None
    
    
    def _get_dosha_foods(self, dosha: str) -> Dict[str, List[str]]:
        """Return base food lists for dosha"""
        dosha_foods = {
            'vata': {
                'favor': ['Warm cooked foods', 'Sweet fruits (bananas, berries)', 'Cooked vegetables', 'Whole grains (rice, oats)', 'Nuts and seeds', 'Ghee', 'Warm milk', 'Root vegetables'],
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
        return dosha_foods.get(dosha, dosha_foods['vata'])


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
    
    def calculate_weight_loss_timeline(self, current_weight: float, target_weight: float) -> Dict[str, Any]:
        """
        Calculate estimated timeline for safe weight loss (0.5-1.0 kg/week)
        """
        weight_diff = current_weight - target_weight
        if weight_diff <= 0:
            return None
            
        # Safe loss rate: 0.5 to 1.0 kg per week
        weeks_min = weight_diff / 1.0
        weeks_max = weight_diff / 0.5
        
        today = datetime.now()
        date_min = today + timedelta(weeks=weeks_min)
        date_max = today + timedelta(weeks=weeks_max)
        
        return {
            "weeks_range": f"{int(weeks_min)}-{int(weeks_max)}",
            "date_range": f"{date_min.strftime('%B %Y')} to {date_max.strftime('%B %Y')}",
            "safe_rate": "0.5 - 1.0 kg/week"
        }

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
        timeline_info = None
        
        # 0. Extraction: Update profile with info from query
        extracted_info = self.extract_profile_info(query)
        # 0. Context Resumption Logic
        # If we extracted new info, check if we should resume a suspended intent from history
        context_resumed = False
        if extracted_info and conversation_history:
            # Check if last assistant message was asking for details
            # We look at the last few messages
            recent_msgs = conversation_history[-3:] # Last 3 messages
            for msg in reversed(recent_msgs):
                if msg.get('role') == 'assistant' and 'details' in msg.get('content', '').lower():
                    # Found clarification request. Now find the user's original request before that
                    # Iterate backwards from that assistant message
                   idx = conversation_history.index(msg)
                   if idx > 0:
                       prev_user_msg = conversation_history[idx-1]
                       if prev_user_msg.get('role') == 'user':
                           # Merge intents: treat the current query as an extension of the original
                           query = prev_user_msg.get('content', '') + " " + query
                           query_lower = query.lower()
                           logger.info(f"Enhanced Assistant: Resuming context from '{prev_user_msg.get('content')}'")
                           context_resumed = True
                           break
            
        # 1. Update Profile with extracted info
        if extracted_info:
            user_profile.update(extracted_info)
            # Retrigger dosha analysis if needed (not implemented here but good for future)

        # 0.5 Clarification: Check if missing info for key intents
        clarification_questions = self.needs_clarification(query, user_profile)
        if clarification_questions:
            # Flatten questions
            all_questions = []
            for cat, qs in clarification_questions.items():
                all_questions.extend(qs)
            
            if all_questions:
                return {
                    'type': 'clarification',
                    'message': "To provide the best personalized plan, I need a few details: " + " ".join(all_questions[:2]), # Ask max 2 at a time
                    'conversation_id': "new"
                }

        # 1. Intent: Water / Hydration
        if any(w in query_lower for w in ['water', 'hydrate', 'drink']):
             # Suggest setting water reminders
             actions.append({
                 "type": "create_reminder",
                 "label": "Set Water Reminders",
                 "data": {
                     "title": "Drink Water",
                     "message": "Time to hydrate! Drink a glass of water.",
                     "frequency": "daily",
                     "default_times": ["09:00", "11:00", "13:00", "15:00", "17:00", "19:00"],
                     "configurable": True
                 }
             })

        # 2. Intent: Weight Loss / Exercise
        if any(w in query_lower for w in ['weight', 'fat', 'lose', 'slim', 'exercise', 'workout', 'diet']):
             # Check if we have goal info to calculate timeline
             current_weight = user_profile.get('weight')
             # Simple heuristic: if query contains "lose weight" and we have current weight, assume a standard target or ask
             
             # Calculate generic schedule based on profile (or default)
             actions.append({
                 "type": "create_reminder",
                 "label": "Set Workout Reminders",
                 "data": {
                     "title": "Workout Session",
                     "message": "Time for your weight loss exercises!",
                     "frequency": "daily",
                     "default_times": ["07:00"],
                     "configurable": True
                 }
             })
             
             actions.append({
                 "type": "create_reminder",
                 "label": "Set Meal Reminders",
                 "data": {
                     "title": "Healthy Meal",
                     "message": "Time for a nutritious balanced meal.",
                     "frequency": "daily",
                     "default_times": ["08:00", "13:00", "19:00"],
                     "configurable": True
                 }
             })
             
             # Also suggest generating a full plan (existing logic reused via text generation context)
             
             # Timeline Logic
             # For now, let's assume a dummy target if not specified to show the capability, 
             # or purely rely on profile if 'target_weight' existed (it doesn't in current schema, so we estimate)
             # Let's assume a 5kg loss goal for the timeline example if not specified
             target_weight = current_weight - 5 if current_weight else None
             
             if current_weight and target_weight:
                 timeline = self.calculate_weight_loss_timeline(current_weight, target_weight)
                 if timeline:
                     timeline_info = f"Based on a safe weight loss rate of {timeline['safe_rate']}, you could reach your goal between {timeline['date_range']} ({timeline['weeks_range']} weeks)."
                     
                     # Add Doctor Consultation Fallback
                     actions.append({
                         "type": "find_practitioner",
                         "label": "Consult a Dietitian (If no results by " + timeline['weeks_range'].split('-')[0] + " weeks)",
                         "data": {
                             "specialization": "Dietitian"
                         }
                     })

        # 3. Intent: Medical Conditions / Disease Detection (ENHANCED)
        # Comprehensive disease symptom database
        disease_symptoms = {
            'fever': {
                'keywords': ['fever', 'temperature', 'hot', 'burning up'],
                'immediate': 'Rest in a cool place, drink plenty of fluids (water, ORS), monitor temperature every 2 hours',
                'ayurvedic': 'Tulsi (Holy Basil) tea, ginger water with honey, light khichdi diet, avoid heavy foods',
                'specialist': 'General Physician',
                'severity': 'moderate',
                'urgency': False
            },
            'chest pain': {
                'keywords': ['chest pain', 'heart pain', 'chest pressure', 'chest tightness'],
                'immediate': '🚨 EMERGENCY: Call ambulance immediately, sit upright, loosen tight clothing, take aspirin if prescribed',
                'ayurvedic': 'DO NOT self-treat - seek immediate medical attention',
                'specialist': 'Cardiologist',
                'severity': 'critical',
                'urgency': True
            },
            'headache': {
                'keywords': ['headache', 'head pain', 'migraine', 'head hurts'],
                'immediate': 'Rest in a dark, quiet room, apply cold compress to forehead, stay hydrated',
                'ayurvedic': 'Peppermint oil on temples, ginger tea, avoid screen time, practice deep breathing',
                'specialist': 'Neurologist',
                'severity': 'low',
                'urgency': False
            },
            'stomach pain': {
                'keywords': ['stomach pain', 'abdominal pain', 'belly pain', 'stomach ache'],
                'immediate': 'Avoid solid food temporarily, sip warm water, rest in comfortable position',
                'ayurvedic': 'Ajwain (carom seeds) water, fennel tea, warm compress on abdomen, avoid spicy/oily foods',
                'specialist': 'Gastroenterologist',
                'severity': 'moderate',
                'urgency': False
            },
            'cough': {
                'keywords': ['cough', 'coughing', 'throat irritation'],
                'immediate': 'Stay hydrated, avoid cold drinks, use steam inhalation',
                'ayurvedic': 'Honey with warm water, tulsi tea, ginger-turmeric milk, avoid dairy temporarily',
                'specialist': 'Pulmonologist',
                'severity': 'low',
                'urgency': False
            },
            'diabetes': {
                'keywords': ['diabetes', 'blood sugar', 'high sugar', 'diabetic'],
                'immediate': 'Monitor blood sugar regularly, maintain meal schedule, stay hydrated',
                'ayurvedic': 'Bitter gourd juice, fenugreek seeds soaked overnight, cinnamon tea, avoid refined sugars',
                'specialist': 'Endocrinologist',
                'severity': 'moderate',
                'urgency': False
            },
            'high blood pressure': {
                'keywords': ['blood pressure', 'hypertension', 'bp', 'high bp'],
                'immediate': 'Reduce salt intake, avoid stress, monitor BP daily, take prescribed medications',
                'ayurvedic': 'Garlic in morning, coconut water, reduce caffeine, practice meditation and pranayama',
                'specialist': 'Cardiologist',
                'severity': 'moderate',
                'urgency': False
            }
        }
        
        # Detect symptoms in query
        detected_diseases = []
        for disease, info in disease_symptoms.items():
            if any(keyword in query_lower for keyword in info['keywords']):
                detected_diseases.append((disease, info))
        
        # If disease detected, provide comprehensive response
        if detected_diseases:
            for disease, info in detected_diseases:
                # Build multi-step response
                disease_response = f"I understand you're experiencing {disease}. Here's what you should do:\n\n"
                
                if info['urgency']:
                    disease_response += f"⚠️ **URGENT - {info['severity'].upper()} SEVERITY**\n\n"
                
                disease_response += f"**Immediate Action:**\n{info['immediate']}\n\n"
                disease_response += f"**Ayurvedic Remedy:**\n{info['ayurvedic']}\n\n"
                
                if info['urgency']:
                    disease_response += "🚨 **Please seek immediate medical attention - this is a medical emergency!**\n\n"
                else:
                    disease_response += "💡 **Recommendation:** If symptoms persist for more than 2-3 days or worsen, please consult a specialist.\n\n"
                
                # Add to timeline_info for inclusion in final response
                if timeline_info:
                    timeline_info += "\n\n" + disease_response
                else:
                    timeline_info = disease_response
                
                # Add specialist consultation action
                actions.append({
                    "type": "find_practitioner",
                    "label": f"Consult {info['specialist']}" + (" URGENTLY" if info['urgency'] else ""),
                    "data": {
                        "specialization": info['specialist'],
                        "urgent": info['urgency'],
                        "condition": disease
                    }
                })
                
                # Add medication reminder for chronic conditions
                if disease in ['diabetes', 'high blood pressure']:
                    actions.append({
                        "type": "create_reminder",
                        "label": "Set Medication Reminder",
                        "data": {
                            "title": f"{disease.title()} Medication",
                            "message": "Time to take your prescribed medication",
                            "frequency": "daily",
                            "default_times": ["09:00", "21:00"],
                            "configurable": True
                        }
                    })
        
        # 3b. Legacy Medical Conditions (Keep for backward compatibility)
        # Broader catch for specific conditions
        medical_conditions = {
            'diabetes': {'specialist': 'Endocrinologist', 'avoid': 'Sugar, refined carbs, sugary drinks', 'favor': 'Leafy greens, whole grains, fiber-rich foods'},
            'sugar': {'specialist': 'Endocrinologist', 'avoid': 'Sugar, sweets, soda', 'favor': 'Vegetables, protein, water'}, # Colloquial for diabetes
            'bp': {'specialist': 'Cardiologist', 'avoid': 'Sodium (salt), processed foods, caffeine', 'favor': 'Fruits, vegetables, low-fat dairy'},
            'blood pressure': {'specialist': 'Cardiologist', 'avoid': 'Salt, fried foods', 'favor': 'Bananas, spinach, oats'},
            'thyroid': {'specialist': 'Endocrinologist', 'avoid': 'Processed foods, gluten (sometimes)', 'favor': 'Iodine-rich foods (if not hyper), selenium'},
            'pcos': {'specialist': 'Gynecologist', 'avoid': 'Sugar, refined carbs', 'favor': 'Whole foods, fiber'}
        }
        
        detected_condition = next((cond for cond in medical_conditions if cond in query_lower), None)
        
        if detected_condition:
            info = medical_conditions[detected_condition]
            
            # Action: Consult Specialist
            actions.append({
                "type": "find_practitioner",
                "label": f"Consult a {info['specialist']}",
                "data": {
                    "specialization": info['specialist']
                }
            })
            
            # Action: Medication Reminder (Generic)
            actions.append({
                "type": "create_reminder",
                "label": "Set Medication/Checkup Reminder",
                "data": {
                    "title": "Medication / Checkup",
                    "message": "Time for your medication or health check.",
                    "frequency": "daily",
                    "default_times": ["09:00", "21:00"],
                    "configurable": True
                }
            })
            
            # Add specific context for the prompt
            timeline_info = f"**Dietary Tip for {detected_condition.title()}:** Avoid {info['avoid']}. Favor {info['favor']}."

        # 4. Intent: Medical Help / Doctor (General)
        if any(w in query_lower for w in ['doctor', 'pain', 'sick', 'ill', 'fever', 'appointment', 'consult']) and not detected_condition:
             # Suggest finding a doctor
             actions.append({
                 "type": "find_practitioner",
                 "label": "Find a Practitioner",
                 "data": {
                     "specialization": "General" if "pain" not in query_lower else "Specialist"
                 }
             })

        # 5. Intent: Specific Plan Request (AGGRESSIVE ROUTING)
        response_type = 'conversation'
        plan_data = None
        plan_message = ""
        
        # Broad keywords for plan generation
        diet_keywords = ['diet', 'meal', 'food', 'eating', 'nutrition', 'recipe']
        workout_keywords = ['workout', 'exercise', 'gym', 'training', 'fitness', 'routine']
        action_keywords = ['plan', 'chart', 'table', 'schedule', 'give', 'suggest', 'help', 'want', 'need']
        
        is_diet_request = any(k in query_lower for k in diet_keywords) and any(a in query_lower for a in action_keywords)
        is_workout_request = any(k in query_lower for k in workout_keywords) and any(a in query_lower for a in action_keywords)
        
        # Prioritize Diet if ambiguous "help me lose weight" -> Diet usually first
        if 'lose weight' in query_lower and not is_workout_request:
            is_diet_request = True

        if is_diet_request:
            response_type = 'diet_plan'
            try:
                plan_data = self.generate_diet_plan(user_profile, dosha_analysis)
                plan_message = f"Here is your personalized diet plan:\n\n"
                plan_message += f"**Target Calories:** {plan_data['target_calories']} kcal/day\n"
                plan_message += f"**Macros:** Protein: {plan_data['macros']['protein']}, Carbs: {plan_data['macros']['carbs']}, Fats: {plan_data['macros']['fats']}\n\n"
                plan_message += "**Daily Meal Plan:**\n"
                for meal_name, meal_details in plan_data['meal_plan'].items():
                    plan_message += f"\n**{meal_name.title()}** ({meal_details['calories']} kcal)\n"
                    plan_message += f"  {meal_details['suggestion']}\n"
                
                plan_message += f"\n**Foods to Favor:** {', '.join(plan_data['foods_to_favor'][:5])}\n"
                plan_message += f"**Foods to Avoid:** {', '.join(plan_data['foods_to_avoid'][:5])}\n"
                
                if plan_data['conditions_considered']:
                    plan_message += f"\n*Tailored for: {', '.join(plan_data['conditions_considered'])}*"
                
                # Add structured meal reminders with specific times
                meal_times = {
                    'breakfast': '08:00',
                    'lunch': '13:00',
                    'dinner': '19:00',
                    'snacks': '16:00'
                }
                
                meal_reminders = []
                for meal_name, meal_details in plan_data['meal_plan'].items():
                    if meal_name in meal_times:
                        meal_reminders.append({
                            "title": f"{meal_name.title()} Time",
                            "time": meal_times[meal_name],
                            "message": meal_details['suggestion'][:100]  # Truncate long messages
                        })
                
                actions.append({
                    "type": "create_reminder",
                    "label": "Schedule Daily Meal Reminders",
                    "data": {
                        "reminders": meal_reminders,
                        "frequency": "daily",
                        "configurable": True
                    }
                })
                
            except Exception as e:
                logger.error(f"Diet Plan Generation Error: {e}")
                response_type = 'conversation'
                plan_message = f"I struggled to generate a detailed diet plan. However, focus on fresh, whole foods suitable for your body type."

            if timeline_info:
                plan_message += f"\n\n{timeline_info}"
                
        elif is_workout_request:
            response_type = 'workout_plan'
            try:
                plan_data = self.generate_workout_plan(user_profile, dosha_analysis)
                plan_message = f"Here is your personalized workout routine:\n\n"
                plan_message += f"**Workout Style:** {plan_data['workout_style']}\n\n"
                plan_message += "**Weekly Schedule:**\n"
                for day, workout in plan_data['weekly_plan'].items():
                    plan_message += f"\n**{day}:**\n  {workout}\n"
                
                if 'yoga_sequence' in plan_data:
                    plan_message += "\n**Recommended Yoga Sequence:**\n"
                    for pose in plan_data['yoga_sequence'][:5]:
                        plan_message += f"  • {pose}\n"
            except Exception as e:
                logger.error(f"Workout Plan Generation Error: {e}")
                response_type = 'conversation'
                plan_message = "I couldn't generate the full workout plan, but staying active is key! Try 30 minutes of moderate exercise daily."
                
            if timeline_info:
                plan_message += f"\n\n{timeline_info}"

        # ===== HYBRID AI ROUTING =====
        # Classify query to determine which AI model to use
        query_type, classification_confidence, classification_metadata = self.query_classifier.classify(query)
        
        logger.info(f"Query classified as: {query_type} (confidence: {classification_confidence:.2f})")
        
        # Generate text response using Gemini or Templates
        conversation_context = f"""
        User Profile: {user_profile}
        Dosha: {dosha_analysis}
        Query: {query}
        Proposed Actions: {[a['label'] for a in actions]}
        Additional Info: {timeline_info}
        """
        
        reply_text = ""
        ai_model_used = "none"
        
        # Only use Gemini if we don't have a specific plan type, OR to generate the intro message for the plan
        if response_type == 'conversation':
            # HYBRID ROUTING: Use Med-Gemma for medical queries, Gemini Pro for Ayurvedic/wellness
            if query_type == 'medical' and self.med_gemma_service.is_available():
                # Use Med-Gemma for medical queries
                try:
                    logger.info("Using Med-Gemma for medical query")
                    med_response = self.med_gemma_service.generate_medical_response(
                        query=query,
                        context=f"Patient conditions: {user_profile.get('medical_conditions', [])}. Dosha: {dosha_analysis}",
                        conversation_history=conversation_history
                    )
                    
                    if med_response.get('response'):
                        reply_text = med_response['response']
                        ai_model_used = "med-gemma"
                        
                        # Add Ayurvedic context if relevant
                        if dosha_analysis:
                            dominant_dosha = max(dosha_analysis, key=dosha_analysis.get)
                            reply_text += f"\n\n**Ayurvedic Perspective:** Your dominant dosha is {dominant_dosha}. Consider this in your treatment approach."
                    else:
                        # Fallback to Gemini if Med-Gemma fails
                        logger.warning(f"Med-Gemma failed: {med_response.get('error')}. Falling back to Gemini.")
                        query_type = 'ayurvedic'  # Force Gemini fallback
                except Exception as e:
                    logger.error(f"Med-Gemma Error: {e}. Falling back to Gemini.")
                    query_type = 'ayurvedic'  # Force Gemini fallback
            
            # Use Gemini Pro for Ayurvedic/wellness queries OR as fallback
            if query_type in ['ayurvedic', 'general', 'hybrid'] or not reply_text:
                if model:
                    try:
                        logger.info(f"Using Gemini Pro for {query_type} query")
                        base_prompt = f"You are a helpful AyurSutra Health Agent specializing in Ayurveda and wellness. The user asked: '{query}'. "
                        
                        if detected_condition:
                             base_prompt += f"IMPORTANT: The user mentioned '{detected_condition}'. Provide helpful dietary and lifestyle advice suitable for this condition properly referencing Ayurveda where applicable. "
                             base_prompt += "ALWAYS start with a disclaimer: 'I am an AI assistant, not a doctor. Please consult a medical professional for advice.' "
                             base_prompt += f"Use this info if helpful: {timeline_info}. "
                        
                        if timeline_info and not detected_condition: # For weight loss flow
                            base_prompt += f"Include this timeline information in your response: {timeline_info}. "
                            base_prompt += "Mention that if they don't see results by then, they should consult a doctor (use the provided action). "
                        
                        if actions:
                            base_prompt += f"You have proposed these actions: {[a['label'] for a in actions]}. Explain why they are good."
                        
                        base_prompt += " Provide helpful health advice based on their profile and dosha."
                        
                        resp = model.generate_content(base_prompt)
                        reply_text = resp.text
                        ai_model_used = "gemini-pro"
                    except Exception as e:
                        logger.error(f"Gemini Error: {e}")
                        reply_text = "I can help you with that. I've also suggested some actions for you below."
                        if timeline_info:
                            reply_text += f"\n\n{timeline_info}"
                        ai_model_used = "fallback"
                else:
                     reply_text = "I've analyzed your request. Please check the suggested actions below."
                     if timeline_info:
                         reply_text += f"\n\n{timeline_info}"
                     ai_model_used = "template"
        else:
            # For plan types, use the plan_message as the base reply
            reply_text = plan_message
            
            # Optionally add AI commentary if Gemini is available
            if model and response_type in ['diet_plan', 'workout_plan']:
                try:
                    commentary_prompt = f"The user requested a {response_type.replace('_', ' ')}. I've generated a detailed plan. Add a brief encouraging message (2-3 sentences) about following this plan."
                    resp = model.generate_content(commentary_prompt)
                    reply_text = resp.text + "\n\n" + reply_text
                    ai_model_used = "gemini-pro"
                except:
                    pass  # Use plan_message as-is

        return {
            'type': response_type,
            'reply': reply_text, # Used for conversation type
            'message': reply_text, # Used for plan types by main.py
            'data': plan_data,
            'actions': actions,
            'conversation_id': "new",
            'extracted_info': extracted_info if 'extracted_info' in locals() else None,
            # Hybrid AI metadata
            'ai_model_used': ai_model_used,
            'query_classification': {
                'type': query_type,
                'confidence': classification_confidence,
                'metadata': classification_metadata
            }
        }


# Singleton instance
health_assistant = ConversationalHealthAssistant()
