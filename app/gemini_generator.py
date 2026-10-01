import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY", "")
if API_KEY and API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=API_KEY)


def generate_workout_gemini(user_input: dict) -> str:
    """Generate a structured 7-day workout plan using Gemini 1.5 Pro."""
    api_key = os.getenv("GOOGLE_API_KEY", "")

    # Resilient fallback if API key is not yet configured or is default placeholder
    if not api_key or api_key == "your_gemini_api_key_here":
        return (
            f"=== FITBUDDY 7-DAY WORKOUT BLUEPRINT ===\n"
            f"Athlete: {user_input.get('username')} (ID: {user_input.get('user_id')})\n"
            f"Profile: Age {user_input.get('age')} | Weight {user_input.get('weight')} kg\n"
            f"Primary Goal: {user_input.get('goal')} | Intensity Level: {user_input.get('intensity')}\n"
            f"--------------------------------------------------------------------------------\n\n"
            f"DAY 1: CHEST & TRICEPS (STRENGTH & HYPERTROPHY FOCUS)\n"
            f"  - Warm-up (5-10 mins):\n"
            f"      * Dynamic arm circles (30s forward, 30s backward)\n"
            f"      * Band pull-aparts: 2 sets x 15 reps\n"
            f"      * Push-up walkouts to high plank: 2 sets x 8 reps\n"
            f"  - Main Workout:\n"
            f"      * Barbell Bench Press: 4 sets x 8-10 reps (Rest: 90s)\n"
            f"      * Incline Dumbbell Press: 3 sets x 10-12 reps (Rest: 60s)\n"
            f"      * Cable Chest Flyes: 3 sets x 12-15 reps (Rest: 45s)\n"
            f"      * Tricep Rope Pushdowns: 4 sets x 12 reps (Rest: 45s)\n"
            f"      * Overhead Dumbbell Extension: 3 sets x 10 reps (Rest: 60s)\n"
            f"  - Cooldown & Recovery (5 mins):\n"
            f"      * Doorway pectoral stretch (45s per side)\n"
            f"      * Tricep overhead stretch and foam roll thoracic spine\n\n"
            f"DAY 2: BACK & BICEPS (POSTERIOR CHAIN & PULL POWER)\n"
            f"  - Warm-up (5-10 mins):\n"
            f"      * Dead hangs from pull-up bar: 3 sets x 20-30s\n"
            f"      * Scapular retractions: 2 sets x 12 reps\n"
            f"      * Cat-Cow spinal waves: 10 slow cycles\n"
            f"  - Main Workout:\n"
            f"      * Conventional Deadlifts or Lat Pulldowns: 4 sets x 6-8 reps (Rest: 120s)\n"
            f"      * Bent-Over Barbell Rows: 4 sets x 8-10 reps (Rest: 90s)\n"
            f"      * Seated Cable Rows (Neutral Grip): 3 sets x 10-12 reps (Rest: 60s)\n"
            f"      * Standing Barbell Bicep Curls: 3 sets x 10-12 reps (Rest: 60s)\n"
            f"      * Incline Dumbbell Hammer Curls: 3 sets x 12 reps (Rest: 45s)\n"
            f"  - Cooldown & Recovery (5 mins):\n"
            f"      * Child's pose with side lat reach (60s each)\n"
            f"      * Wall bicep stretch and deep breathing\n\n"
            f"DAY 3: ACTIVE RECOVERY & CORE STABILIZATION\n"
            f"  - Warm-up (5 mins):\n"
            f"      * Light jog or brisk incline walk\n"
            f"      * World's Greatest Stretch: 5 reps per side\n"
            f"  - Main Workout:\n"
            f"      * 30-40 minutes Low-Intensity Steady State (LISS) cardio (Heart Rate: 120-135 BPM)\n"
            f"      * Hanging Knee/Leg Raises: 3 sets x 12-15 reps\n"
            f"      * RKC Plank: 3 sets x 45 seconds\n"
            f"      * Russian Twists with light plate: 3 sets x 20 total reps\n"
            f"  - Cooldown & Recovery (10 mins):\n"
            f"      * Full-body mobility flow, hip flexor stretch, and foam rolling\n\n"
            f"DAY 4: LEGS & GLUTES (LOWER BODY FOUNDATION)\n"
            f"  - Warm-up (5-10 mins):\n"
            f"      * Bodyweight air squats with pause: 2 sets x 12 reps\n"
            f"      * Glute bridges: 2 sets x 15 reps\n"
            f"      * Leg swings (front-to-back, side-to-side): 15 reps per leg\n"
            f"  - Main Workout:\n"
            f"      * Barbell Back Squats: 4 sets x 8-10 reps (Rest: 120s)\n"
            f"      * Romanian Deadlifts (Dumbbell or Barbell): 4 sets x 10-12 reps (Rest: 90s)\n"
            f"      * Leg Press: 3 sets x 12-15 reps (Rest: 60s)\n"
            f"      * Walking Dumbbell Lunges: 3 sets x 12 steps per leg (Rest: 60s)\n"
            f"      * Standing Calf Raises: 4 sets x 15 reps (2-second hold at peak)\n"
            f"  - Cooldown & Recovery (5 mins):\n"
            f"      * Standing quad stretch and seated butterfly stretch\n"
            f"      * Foam roll IT bands, calves, and piriformis\n\n"
            f"DAY 5: SHOULDERS, TRAPS & UPPER BODY SCULPT\n"
            f"  - Warm-up (5-10 mins):\n"
            f"      * PVC pipe shoulder dislocates: 15 reps\n"
            f"      * Y-T-W shoulder raises on floor: 10 reps each\n"
            f"  - Main Workout:\n"
            f"      * Standing Overhead Barbell/Dumbbell Press: 4 sets x 8-10 reps (Rest: 90s)\n"
            f"      * Dumbbell Lateral Raises: 4 sets x 12-15 reps (Rest: 45s)\n"
            f"      * Face Pulls (with external rotation): 4 sets x 15 reps (Rest: 45s)\n"
            f"      * Dumbbell Shrugs (2-second contraction): 3 sets x 12-15 reps (Rest: 45s)\n"
            f"      * Abdominal Cable Crunches: 3 sets x 15 reps (Rest: 45s)\n"
            f"  - Cooldown & Recovery (5 mins):\n"
            f"      * Cross-body deltoid stretch and overhead tricep/lat release\n\n"
            f"DAY 6: HIGH-INTENSITY FUNCTIONAL METABOLIC CONDITIONING\n"
            f"  - Warm-up (5-10 mins):\n"
            f"      * Jumping jacks, high knees, inchworms with push-up\n"
            f"  - Main Workout (Circuit Style - 4 Rounds, 90s rest between rounds):\n"
            f"      * Kettlebell Swings: 15 reps\n"
            f"      * Goblet Squats: 12 reps\n"
            f"      * Dumbbell Renegade Rows: 10 reps per side\n"
            f"      * Push-ups to Downward Dog: 12 reps\n"
            f"      * Box Jumps or Step-ups: 10 reps\n"
            f"  - Cooldown & Recovery (5 mins):\n"
            f"      * Downward dog calf pedals and cobra abdominal stretch\n\n"
            f"DAY 7: SYSTEMIC REST & CENTRAL NERVOUS SYSTEM REPAIR\n"
            f"  - Complete rest from intense mechanical resistance.\n"
            f"  - Light 20-minute restorative walk in nature.\n"
            f"  - Hydration target: 3.5 liters with electrolytes.\n"
            f"  - Sleep goal: 8-9 hours of uninterrupted deep sleep.\n\n"
            f"[SYSTEM NOTICE: Set a valid GOOGLE_API_KEY in fitbuddy/.env to activate direct dynamic Gemini 1.5 Pro generation]"
        )

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = f"""You are FitBuddy, an elite personal trainer, exercise physiologist, and strength & conditioning coach.
Generate an exhaustive, highly structured 7-Day Workout Plan calibrated specifically for this client:

CLIENT PROFILE:
- Name: {user_input.get('username')}
- User ID: {user_input.get('user_id')}
- Age: {user_input.get('age')}
- Weight: {user_input.get('weight')} kg
- Primary Fitness Goal: {user_input.get('goal')}
- Training Intensity: {user_input.get('intensity')}

STRUCTURAL GUIDELINES (MANDATORY):
1. Create a complete, unbroken day-by-day regimen from DAY 1 through DAY 7.
2. For EVERY day, you MUST provide three explicit subsections:
   * Warm-up (5-10 mins): Dynamic mobility, joint preparation, and muscle activation drills.
   * Main Workout: Explicit exercise names, exact number of working sets, target repetition ranges, and suggested rest intervals matching the client's goal and intensity.
   * Cooldown & Recovery: Static stretching, foam rolling, and recovery protocols.
3. Align exercise selection and volume directly with the client's goal ({user_input.get('goal')}) and intensity ({user_input.get('intensity')}).
4. Ensure tone is professional, encouraging, disciplined, and focused on progressive overload and injury prevention.
5. Format clearly with clean headers and bullet points.
"""
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        return "Unable to generate workout plan from Gemini 1.5 Pro. Please try again."
    except Exception as exc:
        return f"Error connecting to Gemini 1.5 Pro: {str(exc)}"
