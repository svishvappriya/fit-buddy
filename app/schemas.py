from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserInput(BaseModel):
    user_id: int
    username: str
    age: int
    weight: float
    goal: str
    intensity: str

    model_config = ConfigDict(from_attributes=True)


class FeedbackRequest(BaseModel):
    user_id: int
    user_feedback: str

    model_config = ConfigDict(from_attributes=True)


class WorkoutResponse(BaseModel):
    user_id: int
    username: str
    workout_plan: str
    nutrition_tip: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class NutritionResponse(BaseModel):
    goal: str
    nutrition_tip: str

    model_config = ConfigDict(from_attributes=True)


class FeedbackResponse(BaseModel):
    user_id: int
    original_plan: str
    updated_plan: str
    message: str

    model_config = ConfigDict(from_attributes=True)
