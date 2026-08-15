from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    Float,
    Enum as SQLEnum,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database import Base


# ============================================================
# ENUMS
# ============================================================

class WorkoutLocation(str, Enum):
    HOME = "home"
    GYM = "gym"


class WorkoutDays(str, Enum):
    ONE_TO_TWO = "1_2"
    THREE_TO_FOUR = "3_4"
    FIVE_TO_SIX = "5_6"


class WorkoutGoal(str, Enum):
    STRENGTH = "strength"
    HYPERTROPHY = "hypertrophy"
    FITNESS = "fitness"


class Equipment(str, Enum):
    DUMBBELL = "dumbbell"
    RESISTANCE_BAND = "resistance_band"
    NONE = "none"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class FocusArea(str, Enum):
    ABS = "abs"
    GLUTES = "glutes"
    CHEST = "chest"
    ARMS = "arms"


# ============================================================
# WORKOUT PROFILE
# ============================================================

class WorkoutProfile(Base):
    __tablename__ = "workout_profiles"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    location = Column(
        SQLEnum(WorkoutLocation),
        nullable=False,
    )

    days_per_week = Column(
        Integer,
        nullable=False,
    )

    goal = Column(
        SQLEnum(WorkoutGoal),
        nullable=False,
    )

    equipment = Column(
        SQLEnum(Equipment),
        nullable=False,
    )

    gender = Column(
        SQLEnum(Gender),
        nullable=False,
    )

    focus_area = Column(
        SQLEnum(FocusArea),
        nullable=False,
    )

    age = Column(Integer, nullable=False)

    height_cm = Column(Float, nullable=False)

    current_weight_kg = Column(Float, nullable=False)

    target_weight_kg = Column(Float, nullable=False)

    user = relationship(
        "User",
        back_populates="workout_profile",
    )