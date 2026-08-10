from datetime import date, timedelta
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.meal_plan import (
    MealPlan,
    MealPlanDay,
    MealPlanItem,
    PlanStatus,
    PlanMode,
    MealType,
)
from app.models.food import Food


class MealPlanRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ─────────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────────

    async def get_active_plan(
        self,
        user_id: int
    ) -> Optional[MealPlan]:

        result = await self.db.execute(
            select(MealPlan)
            .where(
                MealPlan.user_id == user_id,
                MealPlan.status == PlanStatus.active
            )
            .options(
                selectinload(MealPlan.days)
                .selectinload(MealPlanDay.items)
            )
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_plan_by_id(
        self,
        plan_id: int,
        user_id: int
    ) -> Optional[MealPlan]:

        result = await self.db.execute(
            select(MealPlan)
            .where(
                MealPlan.id == plan_id,
                MealPlan.user_id == user_id
            )
            .options(
                selectinload(MealPlan.days)
                .selectinload(MealPlanDay.items)
            )
        )

        return result.scalar_one_or_none()

    # ─────────────────────────────────────────────
    # DEACTIVATE
    # ─────────────────────────────────────────────

    async def deactivate_existing_plans(
        self,
        user_id: int
    ) -> None:

        await self.db.execute(
            update(MealPlan)
            .where(
                MealPlan.user_id == user_id,
                MealPlan.status == PlanStatus.active
            )
            .values(
                status=PlanStatus.cancelled
            )
        )

    # ─────────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────────

    async def create_plan(
        self,
        user_id: int,
        age: int,
        weight_kg: float,
        height_cm: float,
        gender: str,
        activity_level: str,
        goal: str,
        allergens: list[str],

        target_calories: float,
        target_protein: float,
        target_carbs: float,
        target_fat: float,

        days_data: list[dict],

        mode: PlanMode = PlanMode.auto,

        ga_fitness_score: float | None = None,
        ga_generations: int | None = None,
    ) -> MealPlan:

        start_date = date.today()
        end_date = start_date + timedelta(
            days=len(days_data) - 1
        )

        plan = MealPlan(
            user_id=user_id,

            age=age,
            weight_kg=weight_kg,
            height_cm=height_cm,
            gender=gender,
            activity_level=activity_level,
            goal=goal,

            allergens=allergens,

            target_calories=target_calories,
            target_protein_g=target_protein,
            target_carbs_g=target_carbs,
            target_fat_g=target_fat,

            start_date=start_date,
            end_date=end_date,

            status=PlanStatus.active,
            mode=mode,

            ga_fitness_score=ga_fitness_score,
            ga_generations=ga_generations,
        )

        self.db.add(plan)

        await self.db.flush()

        for day_data in days_data:

            items_data = day_data.get(
                "items",
                []
            )

            day = MealPlanDay(
                plan_id=plan.id,
                day_number=day_data["day_number"],
                day_date=day_data["day_date"],

                total_calories=day_data["total_calories"],
                total_protein_g=day_data["total_protein_g"],
                total_carbs_g=day_data["total_carbs_g"],
                total_fat_g=day_data["total_fat_g"],
            )

            self.db.add(day)

            await self.db.flush()

            for item_data in items_data:

                item = MealPlanItem(
                    day_id=day.id,

                    food_id=item_data["food_id"],
                    meal_type=item_data["meal_type"],

                    food_name=item_data["food_name"],
                    food_category=item_data["food_category"],

                    serving_size=item_data["serving_size"],
                    serving_unit=item_data["serving_unit"],

                    calories=item_data["calories"],
                    protein_g=item_data["protein_g"],
                    carbs_g=item_data["carbs_g"],
                    fat_g=item_data["fat_g"],

                    is_completed=False,
                    note=item_data.get("note"),
                )

                self.db.add(item)

        await self.db.flush()

        return plan

    # ─────────────────────────────────────────────
    # COMPLETE ITEM
    # ─────────────────────────────────────────────

    async def update_item_completion(
        self,
        user_id: int,
        item_id: int,
        completed: bool
    ) -> bool:

        result = await self.db.execute(
            select(MealPlanItem)
            .join(
                MealPlanDay,
                MealPlanDay.id == MealPlanItem.day_id
            )
            .join(
                MealPlan,
                MealPlan.id == MealPlanDay.plan_id
            )
            .where(
                MealPlanItem.id == item_id,
                MealPlan.user_id == user_id,
                MealPlan.status == PlanStatus.active,
            )
        )

        item = result.scalar_one_or_none()

        if item is None:
            return False

        item.is_completed = completed

        await self.db.flush()

        return True

    async def replace_item(
            self,
            user_id: int,
            item_id: int,
            new_food_id: int,
            new_quantity: float,
    ) -> bool:

        result = await self.db.execute(
            select(MealPlanItem)
            .join(
                MealPlanDay,
                MealPlanDay.id == MealPlanItem.day_id
            )
            .join(
                MealPlan,
                MealPlan.id == MealPlanDay.plan_id
            )
            .where(
                MealPlanItem.id == item_id,
                MealPlan.user_id == user_id,
                MealPlan.status == PlanStatus.active,
            )
            .options(
                selectinload(MealPlanItem.day)
            )
        )

        item = result.scalar_one_or_none()

        if item is None:
            return False

        food_result = await self.db.execute(
            select(Food)
            .where(
                Food.id == new_food_id,
                Food.is_active == True
            )
        )

        new_food = food_result.scalar_one_or_none()

        if new_food is None:
            return False

        ratio = new_quantity / 100.0

        new_calories = new_food.calories * ratio
        new_protein = new_food.protein * ratio
        new_carbs = new_food.carbs * ratio
        new_fat = new_food.fat * ratio

        day = item.day

        day.total_calories = (
                day.total_calories
                - item.calories
                + new_calories
        )

        day.total_protein_g = (
                day.total_protein_g
                - item.protein_g
                + new_protein
        )

        day.total_carbs_g = (
                day.total_carbs_g
                - item.carbs_g
                + new_carbs
        )

        day.total_fat_g = (
                day.total_fat_g
                - item.fat_g
                + new_fat
        )

        item.food_id = new_food.id
        item.food_name = new_food.name_en
        item.food_category = new_food.category

        item.serving_size = new_quantity
        item.serving_unit = "g"

        item.calories = new_calories
        item.protein_g = new_protein
        item.carbs_g = new_carbs
        item.fat_g = new_fat

        await self.db.flush()

        return True