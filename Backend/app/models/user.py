import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    trainer = "trainer"
    nutritionist = "nutritionist"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False)
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="user", uselist=False)
    progress_history = relationship(
        "UserProgress",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="UserProgress.created_at.desc()",
    )
    workout_profile = relationship("UserProfile" , back_populates="user", uselist=False)