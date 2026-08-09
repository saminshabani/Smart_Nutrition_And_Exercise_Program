# schemas/meal_plan.py

from pydantic import BaseModel, Field
from app.schemas.user import UserPhysicalInfo


class GeneratePlanRequest(BaseModel):
    days: int = Field(default=7, ge=1, le=30)


class ItemCompletionUpdate(BaseModel):
    completed: bool


class ItemReplaceRequest(BaseModel):
    new_food_id:  int
    new_quantity: float = Field(..., gt=0)
