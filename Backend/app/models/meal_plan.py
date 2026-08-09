# app/models/meal_plan.py

import enum
from datetime import date
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date,
    ForeignKey, Enum, JSON, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.database import Base


class PlanStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"
    archived = "archived"


class PlanMode(str, enum.Enum):
    auto = "auto"       # GA-generated
    manual = "manual"   # user-built


class MealType(str, enum.Enum):
    breakfast = "breakfast"
    morning_snack = "morning_snack"
    lunch = "lunch"
    afternoon_snack = "afternoon_snack"
    dinner = "dinner"


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # snapshot of user data at plan creation time
    age = Column(Integer, nullable=False)
    weight_kg = Column(Float, nullable=False)
    height_cm = Column(Float, nullable=False)
    gender = Column(String(10), nullable=False)
    activity_level = Column(String(30), nullable=False)
    goal = Column(String(30), nullable=False)
    allergens = Column(JSON, default=list)   # list of allergen strings

    # nutritional targets (calculated at creation)
    target_calories = Column(Float, nullable=False)
    target_protein_g = Column(Float, nullable=False)
    target_carbs_g = Column(Float, nullable=False)
    target_fat_g = Column(Float, nullable=False)

    start_date = Column(Date, nullable=False, default=date.today)
    end_date = Column(Date, nullable=False)          # start + 6 days

    status = Column(Enum(PlanStatus), default=PlanStatus.active, nullable=False)
    mode = Column(Enum(PlanMode), default=PlanMode.auto, nullable=False)

    # GA metadata
    ga_fitness_score = Column(Float, nullable=True)
    ga_generations = Column(Integer, nullable=True)

    days = relationship(
        "MealPlanDay",
        back_populates="plan",
        cascade="all, delete-orphan",
        order_by="MealPlanDay.day_number",
    )
    user = relationship("User", back_populates="meal_plans")


class MealPlanDay(Base):
    __tablename__ = "meal_plan_days"

    id = Column(Integer, primary_key=True, index=True)

    plan_id = Column(
        Integer,
        ForeignKey("meal_plans.id", ondelete="CASCADE"),
        nullable=False
    )

    day_number = Column(Integer, nullable=False)
    day_date = Column(Date, nullable=False)

    total_calories = Column(Float, default=0.0)
    total_protein_g = Column(Float, default=0.0)
    total_carbs_g = Column(Float, default=0.0)
    total_fat_g = Column(Float, default=0.0)

    __table_args__ = (
        UniqueConstraint(
            "plan_id",
            "day_number",
            name="uq_plan_day"
        ),
    )

    plan = relationship(
        "MealPlan",
        back_populates="days"
    )

    items = relationship(
        "MealPlanItem",
        back_populates="day",
        cascade="all, delete-orphan",
        order_by="MealPlanItem.meal_type",
    )

class MealPlanItem(Base):
    __tablename__ = "meal_plan_items"

    id = Column(Integer, primary_key=True, index=True)

    day_id = Column(
        Integer,
        ForeignKey(
            "meal_plan_days.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    food_id = Column(
        Integer,
        ForeignKey(
            "foods.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )

    meal_type = Column(
        Enum(MealType),
        nullable=False
    )

    food_name = Column(
        String(200),
        nullable=False
    )

    food_category = Column(
        String(100),
        nullable=True
    )

    serving_size = Column(
        Float,
        nullable=False,
        default=1.0
    )

    serving_unit = Column(
        String(30),
        nullable=True
    )

    calories = Column(
        Float,
        nullable=False
    )

    protein_g = Column(
        Float,
        nullable=False
    )

    carbs_g = Column(
        Float,
        nullable=False
    )

    fat_g = Column(
        Float,
        nullable=False
    )

    is_completed = Column(
        Boolean,
        default=False,
        nullable=False
    )

    note = Column(
        Text,
        nullable=True
    )

    day = relationship(
        "MealPlanDay",
        back_populates="items"
    )

    food = relationship(
        "Food",
        back_populates="meal_plan_items"
    )