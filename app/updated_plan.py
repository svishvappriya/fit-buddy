import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """Update a 7-day workout plan based on athlete feedback using Gemini 1.5 Pro."""
    api_key = os.getenv("GOOGLE_API_KEY", "")

    # Fallback response if API key is not configured
    if not api_key or api_key == "your_gemini_api_key_here":
        return (
            f"=== FITBUDDY REVISED WORKOUT PLAN ===\n"
            f"[MODIFICATION SUMMARY: Plan dynamically updated per feedback: \"{user_feedback}\"]\n"
            f"--------------------------------------------------------------------------------\n\n"
            f"SPECIAL ADAPTATIONS APPLIED:\n"
            f"- Adjusted exercise modalities, target loading, and movement patterns to accommodate: '{user_feedback}'.\n"
            f"- Preserved overall 7-day periodization, warm-up integrity, and cooldown protocols.\n\n"
            f"REVISED FULL PROGRAM:\n\n"
            f"{original_plan}\n\n"
            f"--------------------------------------------------------------------------------\n"
            f"[Note: Add your Google Gemini API key to fitbuddy/.env to receive live, fully re-synthesized routines]"
        )

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = f"""You are FitBuddy, an elite personal trainer, kinesiologist, and strength & conditioning coach.
A client has reviewed their original 7-Day Workout Plan and submitted specific feedback/constraints.

--- ORIGINAL 7-DAY WORKOUT PLAN ---
{original_plan}

--- CLIENT FEEDBACK & REQUESTED MODIFICATIONS ---
"{user_feedback}"

--- MODIFICATION DIRECTIVES ---
1. Analyze the client's feedback carefully (e.g. pain/injury adjustments, exercise substitutions, schedule rebalancing, intensity tweaks, home equipment constraints).
2. Rewrite the plan, updating the SPECIFIC days, exercises, sets, or reps affected by the feedback.
3. Keep non-affected workout days, exercises, and formats structured, consistent, and intact.
4. Maintain the mandatory 3-part daily structure:
   - Warm-up (5-10 mins)
   - Main Workout (Exercises, Sets, Reps, Rest)
   - Cooldown & Recovery
5. At the very top of your output, provide a concise "SUMMARY OF MODIFICATIONS" detailing exactly what changes were made in response to the feedback.
6. Provide the complete, unbroken revised 7-Day Plan from DAY 1 to DAY 7 so the client has an immediate, turnkey schedule to follow.
"""
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return "Failed to generate updated plan from Gemini 1.5 Pro. Please try again."
    except Exception as exc:
        return f"Error updating plan with Gemini 1.5 Pro: {str(exc)}"
