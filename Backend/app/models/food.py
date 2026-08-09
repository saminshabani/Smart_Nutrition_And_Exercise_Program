from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Food(Base):
    __tablename__ = "foods"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    name_en = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    # --------------------------------------------------
    # Category
    # --------------------------------------------------
    # مثال:
    # soup
    # Dairy
    # shirini
    # drink
    # fast_food
    #
    # category فقط نوع کلی غذاست.
    # این مقدار توسط GA به role تبدیل نمی‌شود.
    # --------------------------------------------------

    category = Column(
        String(100),
        nullable=False,
        index=True
    )

    # --------------------------------------------------
    # Role
    # --------------------------------------------------
    #
    # heavy_main
    # easy_main
    # main_side
    # side_side
    # hot_drink
    # cold_drink
    # snack
    # dessert
    #
    # role مشخص می‌کند غذا در ساختار وعده چه نقشی دارد.
    # --------------------------------------------------

    role = Column(
        String(30),
        nullable=False
    )

    # --------------------------------------------------
    # Nutrition - per 100g
    # --------------------------------------------------

    calories = Column(
        Float,
        nullable=False
    )

    fat = Column(
        Float,
        nullable=False
    )

    carbs = Column(
        Float,
        nullable=False
    )

    protein = Column(
        Float,
        nullable=False
    )

    # --------------------------------------------------
    # Suitable meals
    # --------------------------------------------------

    suitable_meals = Column(
        String(100),
        default="breakfast,morning_snack,lunch,afternoon_snack,dinner"
    )

    # --------------------------------------------------
    # Allergens
    # --------------------------------------------------

    allergens = Column(
        String(255),
        default=""
    )

    # --------------------------------------------------
    # GA score
    # --------------------------------------------------

    score_base = Column(
        Float,
        default=1.0
    )

    # --------------------------------------------------
    # Active
    # --------------------------------------------------

    is_active = Column(
        Boolean,
        default=True
    )

    # --------------------------------------------------
    # Relationship
    # --------------------------------------------------

    meal_plan_items = relationship(
        "MealPlanItem",
        back_populates="food"
    )