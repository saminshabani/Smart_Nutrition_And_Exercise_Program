from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.user import UserPhysicalInfo
from app.schemas.schema import ProfileResponse
from app.services.nutrition_engine import NutritionEngine
from sqlalchemy import select
from app.models.profile import Profile
from app.models.user_progress import UserProgress

router = APIRouter(prefix="/users", tags=["users"])


@router.put("/me/physical-info", response_model=ProfileResponse)
async def update_physical_info(
    data: UserPhysicalInfo,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Profile).where(Profile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)

    profile.height = data.height_cm
    profile.weight = data.weight_kg
    profile.age = data.age
    profile.gender = data.gender.value
    profile.activity_level = data.activity_level.value
    profile.goal = data.goal.value

    # محاسبه اهداف تغذیه‌ای و ذخیره
    nutrition = NutritionEngine(data)
    profile.target_calories = nutrition.calories
    profile.target_protein = nutrition.protein
    profile.target_carbs = nutrition.carbs
    profile.target_fat = nutrition.fat

    progress = UserProgress(
        user_id=current_user.id,

        age=profile.age,
        weight=profile.weight,
        height=profile.height,

        gender=profile.gender,
        activity_level=profile.activity_level,
        goal=profile.goal,

        allergies=profile.allergies,

        target_calories=profile.target_calories,
        target_protein=profile.target_protein,
        target_carbs=profile.target_carbs,
        target_fat=profile.target_fat,
    )
    db.add(progress)
    await db.commit()
    await db.refresh(profile)
    return profile
