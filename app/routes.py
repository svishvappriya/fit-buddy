import os
from fastapi import APIRouter, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import (
    get_all_users_with_plans,
    get_original_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.gemini_generator import generate_workout_gemini
from app.schemas import (
    FeedbackRequest,
    FeedbackResponse,
    NutritionResponse,
    UserInput,
    WorkoutResponse,
)
from app.updated_plan import update_workout_plan

# Resolve templates directory relative to current file location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    """Render the homepage with the fitness profile input form."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout_form(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    """Handle HTML form submission, generate plan & nutrition tip, persist to DB, and render results."""
    # Persist or update user record
    save_user(
        user_id=user_id,
        name=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
    )

    user_dict = {
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
    }

    # Generate 7-day plan with Gemini 1.5 Pro
    workout_plan = generate_workout_gemini(user_dict)

    # Generate nutrition & recovery tip with Gemini Flash
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    # Persist workout plan to database
    save_plan(user_id=user_id, plan=workout_plan)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": username,
            "user_id": user_id,
            "age": age,
            "weight": weight,
            "goal": goal,
            "intensity": intensity,
            "workout_plan": workout_plan,
            "original_plan": workout_plan,
            "updated_plan": None,
            "nutrition_tip": nutrition_tip,
            "is_updated": False,
            "feedback_applied": None,
        },
    )


@router.post("/generate_plan", response_model=WorkoutResponse)
async def generate_plan_json(payload: UserInput):
    """Accept JSON UserInput payload, generate workout and nutrition tip, and return structured JSON."""
    save_user(
        user_id=payload.user_id,
        name=payload.username,
        age=payload.age,
        weight=payload.weight,
        goal=payload.goal,
        intensity=payload.intensity,
    )

    user_dict = {
        "username": payload.username,
        "user_id": payload.user_id,
        "age": payload.age,
        "weight": payload.weight,
        "goal": payload.goal,
        "intensity": payload.intensity,
    }

    workout_plan = generate_workout_gemini(user_dict)
    nutrition_tip = generate_nutrition_tip_with_flash(payload.goal)
    save_plan(user_id=payload.user_id, plan=workout_plan)

    return WorkoutResponse(
        user_id=payload.user_id,
        username=payload.username,
        workout_plan=workout_plan,
        nutrition_tip=nutrition_tip,
    )


@router.get("/nutrition-tip", response_model=NutritionResponse)
async def get_nutrition_tip(goal: str = Query(..., description="Target fitness goal")):
    """Accept goal query parameter and return a quick Gemini Flash nutrition & recovery tip."""
    tip = generate_nutrition_tip_with_flash(goal)
    return NutritionResponse(goal=goal, nutrition_tip=tip)


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback_form(
    request: Request,
    user_id: int = Form(...),
    user_feedback: str = Form(...),
):
    """Process user feedback via form, query original plan, trigger Gemini update, save, and render."""
    original_plan = get_original_plan(user_id)
    user = get_user(user_id)

    if not original_plan:
        raise HTTPException(
            status_code=404,
            detail=f"No existing workout plan found for User ID {user_id}. Please generate an initial plan first.",
        )

    # Call Gemini 1.5 Pro to adjust plan according to feedback
    updated_plan_text = update_workout_plan(original_plan, user_feedback)

    # Persist updated plan to database
    update_plan(user_id=user_id, updated_text=updated_plan_text)

    # Refresh nutrition tip for user's goal
    user_goal = user.goal if user else "General Fitness"
    nutrition_tip = generate_nutrition_tip_with_flash(user_goal)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": user.name if user else "Athlete",
            "user_id": user_id,
            "age": user.age if user else 25,
            "weight": user.weight if user else 70.0,
            "goal": user_goal,
            "intensity": user.intensity if user else "Intermediate",
            "workout_plan": updated_plan_text,
            "original_plan": original_plan,
            "updated_plan": updated_plan_text,
            "nutrition_tip": nutrition_tip,
            "is_updated": True,
            "feedback_applied": user_feedback,
        },
    )


@router.post("/update-plan/{user_id}", response_model=FeedbackResponse)
async def update_plan_json(user_id: int, payload: FeedbackRequest):
    """JSON endpoint to update an existing plan based on feedback."""
    original_plan = get_original_plan(user_id)
    if not original_plan:
        raise HTTPException(
            status_code=404,
            detail=f"No workout plan found for User ID {user_id}. Generate a plan first.",
        )

    updated_plan_text = update_workout_plan(original_plan, payload.user_feedback)
    update_plan(user_id=user_id, updated_text=updated_plan_text)

    return FeedbackResponse(
        user_id=user_id,
        original_plan=original_plan,
        updated_plan=updated_plan_text,
        message="Workout plan successfully updated with Gemini Pro.",
    )


@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users_page(request: Request):
    """Query all registered users and their joined workout plans, rendering the admin dashboard."""
    users = get_all_users_with_plans()
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users,
        },
    )
