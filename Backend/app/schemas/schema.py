from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.schemas.user import Gender, ActivityLevel, Goal

ACTIVITY_MULTIPLIERS = {
    "sedentary":   1.2,
    "light":       1.375,
    "moderate":    1.55,
    "active":      1.725,
    "very_active": 1.9,
}
# --- Auth ---
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

# --- User ---
class UserResponse(BaseModel):
    id: int
    email: str
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}

# --- Profile ---
class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    goal: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int

    name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None

    gender: Gender | None = None
    activity_level: ActivityLevel | None = None
    goal: Goal | None = None

    target_calories: Optional[float] = None
    target_protein: Optional[float] = None
    target_carbs: Optional[float] = None
    target_fat: Optional[float] = None

    allergies: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }