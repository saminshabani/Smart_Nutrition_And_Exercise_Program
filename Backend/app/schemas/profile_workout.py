"""
app/schemas/profile.py

اسکیمای ورودی/خروجی پروفایل کاربر. UserProfileIn دقیقاً معادل همون فرم
۱۰ سوالیه (location, days_per_week, goal, level, equipment, gender,
focus_areas, height, current_weight, target_weight, age).

وابسته به: core.enums
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.enum import DaysPerWeek, Goal, Level, Gender, Equipment, FocusArea


class UserProfileIn(BaseModel):
    location: str = Field(min_length=1, max_length=100)
    days_per_week: DaysPerWeek
    goal: Goal
    level: Level
    equipment_available: list[Equipment] = Field(default_factory=list)
    gender: Gender
    focus_areas: list[FocusArea] = Field(default_factory=list)

    height_cm: float = Field(gt=0, le=260)
    current_weight_kg: float = Field(gt=0, le=400)
    target_weight_kg: float = Field(gt=0, le=400)
    age: int = Field(ge=10, le=100)

    @model_validator(mode="after")
    def enforce_business_rules(self) -> "UserProfileIn":
        """
        قانون کسب‌وکار، نه محدودیت دیتابیسی: کاربر زیر ۱۶ سال صرف‌نظر از چیزی
        که خودش انتخاب کرده، همیشه به‌عنوان مبتدی در نظر گرفته می‌شه - چون
        امن‌ترین سطح شدت تمرینه. اینجا انجامش می‌دیم، نه در سرویس، چون این
        محض validation ورودیه و باید قبل از رسیدن به orchestrator اعمال بشه.
        """
        if self.age < 16 and self.level != Level.BEGINNER:
            self.level = Level.BEGINNER
        return self


class UserProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    location: str
    days_per_week: DaysPerWeek
    goal: Goal
    level: Level
    equipment_available: list[str]
    gender: Gender
    focus_areas: list[str]
    height_cm: float
    current_weight_kg: float
    target_weight_kg: float
    age: int
    created_at: datetime