from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.schemas.user import Gender, ActivityLevel, Goal


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Snapshot Profile
    age = Column(Integer, nullable=False)

    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)

    gender = Column(Enum(Gender), nullable=False)
    activity_level = Column(Enum(ActivityLevel), nullable=False)
    goal = Column(Enum(Goal), nullable=False)

    allergies = Column(JSON, default=list)

    # Nutrition Targets
    target_calories = Column(Float, nullable=False)
    target_protein = Column(Float, nullable=False)
    target_carbs = Column(Float, nullable=False)
    target_fat = Column(Float, nullable=False)

    # آینده
    bmi = Column(Float, nullable=True)
    body_fat = Column(Float, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="progress_history")