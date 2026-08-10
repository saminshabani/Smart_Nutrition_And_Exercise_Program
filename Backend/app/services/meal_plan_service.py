from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import select

from app.repository.food_repository import FoodRepository
from app.repository.meal_plan_repository import MealPlanRepository
from app.models.profile import Profile
from app.models.meal_plan import PlanMode
from app.gn.gn_algorithm import (
    FoodItem,
    MealTarget,
    MEAL_TYPES,
    run_ga,
)

from datetime import date, timedelta


class MealPlanService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.food_repo = FoodRepository(db)
        self.plan_repo = MealPlanRepository(db)

    async def generate_plan(
        self,
        user_id: int,
        days: int = 7,
    ) -> dict:

        # ============================================================
        # 1. دریافت پروفایل
        # ============================================================

        result = await self.db.execute(
            select(Profile).where(
                Profile.user_id == user_id
            )
        )

        profile = result.scalar_one_or_none()

        if profile is None:
            raise HTTPException(
                status_code=400,
                detail="ابتدا اطلاعات فیزیکی خود را ثبت کنید."
            )

        required = [
            profile.age,
            profile.height,
            profile.weight,
            profile.gender,
            profile.activity_level,
            profile.goal,
            profile.target_calories,
            profile.target_protein,
            profile.target_carbs,
            profile.target_fat,
        ]

        if any(v is None for v in required):
            raise HTTPException(
                status_code=400,
                detail="پروفایل ناقص است. ابتدا آن را تکمیل یا بروزرسانی کنید."
            )

        # ============================================================
        # 2. هدف روزانه
        # ============================================================

        daily_target = MealTarget(
            calories=profile.target_calories,
            protein=profile.target_protein,
            carbs=profile.target_carbs,
            fat=profile.target_fat,
        )

        # ============================================================
        # 3. آلرژن‌ها
        # ============================================================

        allergens = []

        if profile.allergies:
            allergens = [
                a.strip()
                for a in profile.allergies.split(",")
                if a.strip()
            ]

        # ============================================================
        # 4. دریافت غذاها
        # ============================================================

        food_pools: dict[str, list[FoodItem]] = {}

        for meal in MEAL_TYPES:

            db_foods = await self.food_repo.get_for_meal(
                meal,
                allergens,
            )

            food_pools[meal] = [
                FoodItem.from_orm(food)
                for food in db_foods
            ]

        # ============================================================
        # 5. بررسی وجود غذا برای تمام وعده‌ها
        # ============================================================

        meal_names = {
            "breakfast": "صبحانه",
            "morning_snack": "میان‌وعده صبح",
            "lunch": "ناهار",
            "afternoon_snack": "میان‌وعده عصر",
            "dinner": "شام",
        }

        empty_meals = [
            meal
            for meal in MEAL_TYPES
            if not food_pools.get(meal)
        ]

        if empty_meals:

            missing_names = [
                meal_names.get(meal, meal)
                for meal in empty_meals
            ]

            raise HTTPException(
                status_code=400,
                detail=(
                    "برای وعده‌های زیر غذای مناسب پیدا نشد: "
                    + ", ".join(missing_names)
                )
            )

        # ============================================================
        # 6. اجرای Genetic Algorithm
        # ============================================================

        best_days = run_ga(
            food_pools=food_pools,
            daily_target=daily_target,
            days=days,
        )

        if not best_days:
            raise HTTPException(
                status_code=500,
                detail="الگوریتم تولید برنامه غذایی نتوانست برنامه‌ای ایجاد کند."
            )

        # ============================================================
        # 7. بررسی خروجی GA
        #
        # هر روز باید دقیقاً هر ۵ وعده را داشته باشد.
        # ============================================================

        for day_index, chromosome in enumerate(
            best_days,
            start=1
        ):

            missing_meals = [
                meal
                for meal in MEAL_TYPES
                if not chromosome.get(meal)
            ]

            if missing_meals:

                missing_names = [
                    meal_names.get(meal, meal)
                    for meal in missing_meals
                ]

                raise HTTPException(
                    status_code=500,
                    detail=(
                        f"الگوریتم برای روز {day_index} "
                        f"وعده‌های زیر را تولید نکرد: "
                        + ", ".join(missing_names)
                    )
                )

        # ============================================================
        # 8. غیرفعال کردن برنامه قبلی
        # ============================================================

        await self.plan_repo.deactivate_existing_plans(
            user_id
        )

        # ============================================================
        # 9. ساخت روزهای برنامه
        # ============================================================

        days_data = []

        start_date = date.today()

        for day_num, chromosome in enumerate(
            best_days,
            start=1
        ):

            items_data = []

            # --------------------------------------------------------
            # ترتیب قطعی وعده‌ها
            # --------------------------------------------------------

            for meal_type in MEAL_TYPES:

                genes = chromosome.get(
                    meal_type,
                    []
                )

                # اگر GA وعده‌ای را خالی برگرداند
                # اینجا اجازه نمی‌دهیم برنامه ناقص ذخیره شود.
                if not genes:
                    raise HTTPException(
                        status_code=500,
                        detail=(
                            f"روز {day_num} برای وعده "
                            f"{meal_names.get(meal_type, meal_type)} "
                            f"هیچ غذایی تولید نشده است."
                        )
                    )

                for gene in genes:

                    items_data.append({
                        "food_id": gene.food.id,

                        "meal_type": meal_type,

                        "food_name": gene.food.name,

                        "food_category": gene.food.category,

                        "serving_size": round(
                            gene.quantity,
                            1
                        ),

                        "serving_unit": "g",

                        "calories": round(
                            gene.calories,
                            2
                        ),

                        "protein_g": round(
                            gene.protein,
                            2
                        ),

                        "carbs_g": round(
                            gene.carbs,
                            2
                        ),

                        "fat_g": round(
                            gene.fat,
                            2
                        ),
                    })

            # ========================================================
            # 10. بررسی اینکه واقعاً ۵ وعده داریم
            # ========================================================

            generated_meals = {
                item["meal_type"]
                for item in items_data
            }

            expected_meals = set(MEAL_TYPES)

            if generated_meals != expected_meals:

                missing = expected_meals - generated_meals

                raise HTTPException(
                    status_code=500,
                    detail=(
                        f"برنامه روز {day_num} ناقص است. "
                        f"وعده‌های مفقود: "
                        f"{', '.join(missing)}"
                    )
                )

            # ========================================================
            # 11. محاسبه مجموع روز
            # ========================================================

            total_cal = sum(
                item["calories"]
                for item in items_data
            )

            total_pro = sum(
                item["protein_g"]
                for item in items_data
            )

            total_carb = sum(
                item["carbs_g"]
                for item in items_data
            )

            total_fat = sum(
                item["fat_g"]
                for item in items_data
            )

            # ========================================================
            # 12. ذخیره اطلاعات روز
            # ========================================================

            days_data.append({
                "day_number": day_num,

                "day_date": (
                    start_date
                    + timedelta(days=day_num - 1)
                ),

                "total_calories": round(
                    total_cal,
                    2
                ),

                "total_protein_g": round(
                    total_pro,
                    2
                ),

                "total_carbs_g": round(
                    total_carb,
                    2
                ),

                "total_fat_g": round(
                    total_fat,
                    2
                ),

                "items": items_data,
            })

        # ============================================================
        # 13. ساخت Meal Plan
        # ============================================================

        plan = await self.plan_repo.create_plan(

            user_id=user_id,

            age=profile.age,

            weight_kg=profile.weight,

            height_cm=profile.height,

            gender=profile.gender,

            activity_level=profile.activity_level,

            goal=profile.goal,

            allergens=allergens,

            target_calories=daily_target.calories,

            target_protein=daily_target.protein,

            target_carbs=daily_target.carbs,

            target_fat=daily_target.fat,

            days_data=days_data,

            mode=PlanMode.auto,
        )

        # ============================================================
        # 14. Commit
        # ============================================================

        await self.db.commit()

        # ============================================================
        # 15. برگرداندن برنامه
        # ============================================================

        return await self.plan_repo.get_plan_by_id(
            plan.id,
            user_id
        )

    # ================================================================
    # Mark Item
    # ================================================================

    async def mark_item(
        self,
        user_id: int,
        item_id: int,
        completed: bool,
    ) -> bool:

        result = await self.plan_repo.update_item_completion(
            user_id,
            item_id,
            completed
        )

        await self.db.commit()

        return result

    # ================================================================
    # Replace Food
    # ================================================================

    async def replace_food(
        self,
        user_id: int,
        item_id: int,
        new_food_id: int,
        new_quantity: float,
    ) -> bool:

        result = await self.plan_repo.replace_item(
            user_id,
            item_id,
            new_food_id,
            new_quantity
        )

        await self.db.commit()

        return result