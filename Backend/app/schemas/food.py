from pydantic import BaseModel, Field
from typing import Optional


class FoodBase(BaseModel):
    name:           str
    name_en:        str
    category:       str
    calories:       float = Field(..., ge=0)
    fat:            float = Field(..., ge=0)
    carbs:          float = Field(..., ge=0)
    protein:        float = Field(..., ge=0)
    suitable_meals: str   = "breakfast,morning_snack,lunch,afternoon_snack,dinner"
    allergens:      str   = ""
    score_base:     float = 1.0
    is_active:      bool  = True


class FoodCreate(FoodBase):
    pass


class FoodRead(FoodBase):
    id: int

    model_config = {"from_attributes": True}


class FoodFilter(BaseModel):
    category:    Optional[str]  = None
    meal:        Optional[str]  = None   # "breakfast" | "lunch" | ...
    allergens:   Optional[list[str]] = []
