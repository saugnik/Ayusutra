
import asyncio
import logging
import json
from enhanced_health_assistant import ConversationalHealthAssistant

# Mock Data simulating the request
user_profile = {
    "weight": 80,
    "height": 180,
    "age": 30,
    "gender": "male",
    "activity_level": "moderately active",
    "dietary_restrictions": ["vegan"],
    "medical_conditions": ["hypertension"]
}

dosha_analysis = {"vata": 40, "pitta": 40, "kapha": 20}
query = "I am a 30 year old vegan male with high blood pressure. I want to build muscle but only have 3 days a week to train. Give me a plan."
conversation_history = []

async def test():
    print("--- Starting Debug ---")
    assistant = ConversationalHealthAssistant()
    try:
        response = await assistant.generate_conversational_response(
            query=query,
            user_profile=user_profile,
            conversation_history=conversation_history,
            dosha_analysis=dosha_analysis
        )
        print("--- Success ---")
        print(json.dumps(response, default=str, indent=2))
    except Exception as e:
        print("--- CRASH DETECTED ---")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
