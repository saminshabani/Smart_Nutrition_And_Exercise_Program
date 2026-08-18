"""
app/schemas/workout.py

اسکیمای خروجی برنامه تمرینی نهایی - چیزی که از /workout/generate برمی‌گرده.
همه از from_attributes=True استفاده می‌کنن تا مستقیم از آبجکت‌های ORM (مدل‌های
WorkoutProgram/WorkoutDay/WorkoutSlot) ساخته بشن، بدون map دستی.

وابسته به: core.enums
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enum import SplitType


class ExerciseOut(BaseModel):
    """نسخه فشرده Exercise برای نمایش داخل یک Slot - نه کل رکورد دیتاست."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    primary_muscles: list[str]
    instructions: list[str]


class SlotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    target_muscle: str
    chosen_exercise: ExerciseOut | None
    sets: int | None
    reps_min: int | None
    reps_max: int | None
    rest_seconds: int | None


class WorkoutDayOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    day_index: int
    label: str
    slots: list[SlotOut]


class WorkoutProgramOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    split_type: SplitType
    created_at: datetime
    expires_at: datetime
    days: list[WorkoutDayOut]