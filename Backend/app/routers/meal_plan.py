from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.core.deps import get_current_user
from app.schemas.meal_plan import GeneratePlanRequest, ItemCompletionUpdate, ItemReplaceRequest
from app.services.meal_plan_service import MealPlanService

router = APIRouter(prefix="/meal-plans", tags=["Meal Plans"])


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_plan(
    request: GeneratePlanRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = MealPlanService(db)

    plan = await service.generate_plan(
        user_id=current_user.id,
        days=request.days,
    )

    return plan


@router.get("/active")
async def get_active_plan(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = MealPlanService(db)

    plan = await service.plan_repo.get_active_plan(current_user.id)

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="پلن فعالی وجود ندارد."
        )

    return plan


@router.patch("/items/{item_id}/complete")
async def mark_item_complete(
    item_id: int,
    body: ItemCompletionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = MealPlanService(db)

    ok = await service.mark_item(
        current_user.id,
        item_id,
        body.completed,
    )

    if not ok:
        raise HTTPException(404, "آیتم پیدا نشد.")

    return {"detail": "آپدیت شد."}


@router.patch("/items/{item_id}/replace")
async def replace_item(
    item_id: int,
    body: ItemReplaceRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = MealPlanService(db)

    ok = await service.replace_food(
        current_user.id,
        item_id,
        body.new_food_id,
        body.new_quantity,
    )

    if not ok:
        raise HTTPException(404, "آیتم یا غذا پیدا نشد.")

    return {"detail": "جایگزین شد."}