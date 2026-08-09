from pydantic import BaseModel, Field , EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime
class UserRole(str, Enum):
    admin = "admin"
    trainer = "trainer"
    nutritionist = "nutritionist"
    user = "user"


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.user


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserOut(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Gender(str, Enum):
    male   = "male"
    female = "female"


class ActivityLevel(str, Enum):
    sedentary   = "sedentary"    # کم‌تحرک
    light       = "light"        # کم‌فعالیت
    moderate    = "moderate"     # متوسط
    active      = "active"       # فعال
    very_active = "very_active"  # خیلی فعال


class Goal(str, Enum):
    lose_weight   = "lose_weight"
    maintain      = "maintain"
    gain_weight   = "gain_weight"


class UserPhysicalInfo(BaseModel):
    age:            int            = Field(..., ge=10, le=100)
    weight_kg:      float          = Field(..., gt=20, lt=300)
    height_cm:      float          = Field(..., gt=100, lt=250)
    gender:         Gender
    activity_level: ActivityLevel
    goal:           Goal
    allergens:      list[str]      = Field(default_factory=list)


class UserRead(BaseModel):
    id:         int
    name:       str
    phone:      str
    is_active:  bool

    class Config:
        from_attributes = True
