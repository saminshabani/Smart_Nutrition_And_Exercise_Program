from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models.food import Food


class FoodRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # async def get_for_meal(
    #     self,
    #     meal_name: str,
    #     exclude_allergens: list[str] | None = None,
    # ) -> List[Food]:
    #     """
    #     غذاهای مناسب یه وعده رو برمی‌گردونه.
    #     suitable_meals به صورت 'breakfast,lunch,dinner' ذخیره شده،
    #     پس LIKE برای جستجو کافیه.
    #     """
    #     result = await self.db.execute(
    #         select(Food).where(
    #             Food.is_active == True,
    #             Food.suitable_meals.like(f"%{meal_name}%"),
    #         )
    #     )
    #     foods = result.scalars().all()
    #
    #     # فیلتر آلرژی در Python (چون comma-separated)
    #     if exclude_allergens:
    #         foods = [
    #             f for f in foods
    #             if not any(
    #                 allergen.lower() in f.allergens.lower()
    #                 for allergen in exclude_allergens
    #             )
    #         ]
    #
    #     return foods

    async def get_for_meal(
            self,
            meal_name: str,
            exclude_allergens: list[str] | None = None,
            roles: list[str] | None = None,
    ) -> List[Food]:
        """
        غذاهای مناسب یک وعده را برمی‌گرداند.

        meal_name:
            breakfast
            morning_snack
            lunch
            afternoon_snack
            dinner

        roles:
            main
            side
            snack
            drink
            dessert
            fat_addition
        """

        query = select(Food).where(
            Food.is_active == True,
            Food.suitable_meals.like(f"%{meal_name}%"),
        )

        # اگر role مشخص شده باشد، فقط همان roleها
        if roles:
            query = query.where(
                Food.role.in_(roles)
            )

        result = await self.db.execute(query)

        foods = result.scalars().all()

        # فیلتر آلرژی
        if exclude_allergens:
            foods = [
                f
                for f in foods
                if not any(
                    allergen.lower() in (f.allergens or "").lower()
                    for allergen in exclude_allergens
                )
            ]

        return foods

    async def get_by_id(self, food_id: int) -> Food | None:
        result = await self.db.execute(
            select(Food).where(Food.id == food_id, Food.is_active == True)
        )
        return result.scalar_one_or_none()

    async def get_by_category(self, category: str) -> List[Food]:
        result = await self.db.execute(
            select(Food).where(
                Food.category == category,
                Food.is_active == True,
            )
        )
        return result.scalars().all()

    async def create(self, data: dict) -> Food:
        food = Food(**data)
        self.db.add(food)
        await self.db.flush()
        return food
