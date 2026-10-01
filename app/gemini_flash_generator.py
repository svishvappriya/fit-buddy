import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """Generate a fast, actionable daily nutrition and recovery tip using Gemini Flash."""
    api_key = os.getenv("GOOGLE_API_KEY", "")

    # Fallback tips if API key is not configured
    if not api_key or api_key == "your_gemini_api_key_here":
        normalized_goal = goal.strip().lower()
        if "muscle" in normalized_goal or "hypertrophy" in normalized_goal or "bulk" in normalized_goal:
            return (
                "Consume 1.8 to 2.2 grams of quality protein per kilogram of body weight spread across 4-5 meals. "
                "Pair your post-workout protein with fast-digesting carbohydrates to optimize glycogen replenishment and trigger maximal muscle protein synthesis."
            )
        elif "loss" in normalized_goal or "fat" in normalized_goal or "cut" in normalized_goal:
            return (
                "Maintain a measured caloric deficit of 350-500 kcal below maintenance while keeping protein intake elevated at 2.0g/kg. "
                "Front-load your meals with fibrous green vegetables and drink 500ml of water 20 minutes before each meal to enhance satiety."
            )
        elif "endurance" in normalized_goal or "stamina" in normalized_goal or "running" in normalized_goal:
            return (
                "Target 6-8 grams of complex carbohydrates per kilogram of body weight on heavy training days. "
                "Replenish lost sodium and potassium with an electrolyte solution during sessions exceeding 60 minutes to maintain intracellular hydration."
            )
        else:
            return (
                "Prioritize whole, minimally processed whole foods following an 80/20 lifestyle balance. "
                "Ensure a minimum of 35-40ml of water per kg of body weight daily and secure 7-9 hours of consistent, quality sleep to support central nervous system recovery."
            )

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""You are an elite sports nutritionist and performance recovery specialist.
Generate ONE highly actionable, science-based daily nutrition and recovery tip specifically tailored for an athlete with the primary goal of: '{goal}'.

CONSTRAINTS:
1. Provide exactly 2 to 4 punchy, practical sentences.
2. Focus on precise macronutrient targets, nutrient timing, hydration, or sleep hygiene.
3. No greeting, no boilerplate introduction, no sign-offs. Deliver the tip directly.
"""
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return (
            "Prioritize lean protein (1.6-2.2g/kg body weight), adequate hydration with electrolytes, and 8 hours of sleep to drive muscular repair and systemic recovery."
        )
    except Exception as exc:
        return (
            f"Daily Nutrition Tip: Target 2g of protein per kg of body weight, drink 3-4 liters of water, and ensure 8 hours of restorative sleep to support your '{goal}' journey."
        )
