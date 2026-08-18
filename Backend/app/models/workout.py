"""
app/models/workout.py

لایه‌ی مدل‌ها - وابسته به core/enums.py و database.py (Base) موجودت.
فرض: توی database.py یک `Base = declarative_base()` یا `DeclarativeBase` داری.
اگه اسم فایل یا مسیر Base فرق می‌کنه، فقط ایمپورت خط زیر رو اصلاح کن.
"""

from datetime import datetime

from sqlalchemy import String, Integer, Float, ForeignKey, JSON, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.user import User  # مدل احراز هویت موجودت (username, email, password)
from app.core.enum import (
    Level,
    Goal,
    DaysPerWeek,
    SplitType,
    Gender,
    Equipment,
    Mechanic,
)


def str_enum(enum_cls, *, name: str):
    """
    دو نکته مهم درباره Enum در Postgres:
    ۱. پیش‌فرض SQLAlchemy، .name عضوها رو ذخیره می‌کنه نه .value - برای همین
       values_callable رو صریح می‌دیم تا .value ("beginner") ذخیره بشه.
    ۲. هر Enum پایتونی یک TYPE سراسری در سطح دیتابیس می‌سازه (نه محدود به یک
       جدول)! اگه اسمش رو صریح ندیم، SQLAlchemy از اسم کلاس (مثلاً "goal")
       استفاده می‌کنه که ممکنه با Enum هم‌نام از ماژول‌های دیگه (تغذیه و ...)
       تصادم کنه - دقیقاً همون اروری که با type "goal" already exists گرفتی.
       برای همین همه‌ی Enumهای این ماژول با پیشوند workout_ نام‌گذاری می‌شن.
    """
    return SAEnum(enum_cls, name=name, values_callable=lambda cls: [e.value for e in cls])


# ---------------------------------------------------------------------------
# Exercise — بازتاب مستقیم رکوردهای exercise.json پس از seed
# ---------------------------------------------------------------------------
class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    force: Mapped[str | None] = mapped_column(String(50), nullable=True)
    level: Mapped[Level] = mapped_column(str_enum(Level, name="workout_level"), nullable=False, index=True)
    mechanic: Mapped[Mechanic | None] = mapped_column(str_enum(Mechanic, name="workout_mechanic"), nullable=True, index=True)
    equipment: Mapped[Equipment | None] = mapped_column(str_enum(Equipment, name="workout_equipment"), nullable=True, index=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # آرایه‌ها به‌صورت JSON نگه داشته می‌شن - برای فیلتر روی primary_muscles
    # در ExerciseRepository از عملگرهای JSON دیتابیس (مثلاً @> در Postgres) استفاده می‌شه
    primary_muscles: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    secondary_muscles: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    instructions: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    def __repr__(self) -> str:
        return f"<Exercise id={self.id} name={self.name!r} level={self.level}>"


# ---------------------------------------------------------------------------
# UserProfile — پاسخ ۱۰ سوال کاربر، وصل به مدل User موجود (auth) با رابطه یک‌به‌یک
# فرض: کلاس User توی app/models/user.py با __tablename__ = "users" تعریف شده.
# اگه مسیر یا اسم جدول فرق داره، فقط ایمپورت و ForeignKey زیر رو اصلاح کن.
# ---------------------------------------------------------------------------
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    # unique=True یعنی هر کاربر فقط یک پروفایل ورزشی داره (رابطه یک‌به‌یک، نه یک‌به‌چند)

    location: Mapped[str] = mapped_column(String(100), nullable=False)
    days_per_week: Mapped[DaysPerWeek] = mapped_column(str_enum(DaysPerWeek, name="workout_days_per_week"), nullable=False)
    goal: Mapped[Goal] = mapped_column(str_enum(Goal, name="workout_goal"), nullable=False)
    level: Mapped[Level] = mapped_column(str_enum(Level, name="workout_level"), nullable=False)  # <-- فیلد جدید
    equipment_available: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    gender: Mapped[Gender] = mapped_column(str_enum(Gender, name="workout_gender"), nullable=False)
    focus_areas: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    # عمداً این‌جا نگه داشته شدن نه در جدول profiles: ماژول ورزش باید مستقل از
    # ماژول تغذیه کار کنه (کاربر ممکنه فقط برنامه ورزشی بخواد و اصلاً وارد
    # ماژول تغذیه نشه)، پس نمی‌شه به وجود رکورد توی profiles تکیه کرد.
    height_cm: Mapped[float] = mapped_column(Float, nullable=False)
    current_weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    target_weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="workout_profile")
    programs: Mapped[list["WorkoutProgram"]] = relationship(back_populates="user_profile")

    def __repr__(self) -> str:
        return f"<UserProfile id={self.id} user_id={self.user_id} level={self.level}>"


# ---------------------------------------------------------------------------
# WorkoutProgram — خروجی نهایی هدر برنامه (یک اسپلیت کامل)
# ---------------------------------------------------------------------------
class WorkoutProgram(Base):
    __tablename__ = "workout_programs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"), nullable=False)
    split_type: Mapped[SplitType] = mapped_column(str_enum(SplitType, name="workout_split_type"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # برنامه ۲۸ روز معتبره - کاربر تا این تاریخ باید همین برنامه رو ادامه بده،
    # بعدش پروفایلش رو آپدیت کنه و برنامه جدید بگیره. این مقدار موقع ساخت
    # برنامه در WorkoutOrchestratorService محاسبه و ذخیره می‌شه.
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user_profile: Mapped["UserProfile"] = relationship(back_populates="programs")
    days: Mapped[list["WorkoutDay"]] = relationship(
        back_populates="program", cascade="all, delete-orphan", order_by="WorkoutDay.day_index"
    )


# ---------------------------------------------------------------------------
# WorkoutDay — یک روز از اسپلیت (مثلاً "Push" یا "Upper")
# ---------------------------------------------------------------------------
class WorkoutDay(Base):
    __tablename__ = "workout_days"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("workout_programs.id"), nullable=False)
    day_index: Mapped[int] = mapped_column(Integer, nullable=False)  # ترتیب روز در هفته
    label: Mapped[str] = mapped_column(String(50), nullable=False)  # "Push" / "Upper" / "Full Body"

    program: Mapped["WorkoutProgram"] = relationship(back_populates="days")
    slots: Mapped[list["WorkoutSlot"]] = relationship(
        back_populates="day", cascade="all, delete-orphan", order_by="WorkoutSlot.order_index"
    )


# ---------------------------------------------------------------------------
# WorkoutSlot — یک جایگاه حرکت که توسط Slot-filling پر می‌شه
# این جدول هم اسکلت خالی (قبل از پر شدن) و هم نتیجه نهایی رو نگه می‌داره
# ---------------------------------------------------------------------------
class WorkoutSlot(Base):
    __tablename__ = "workout_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day_id: Mapped[int] = mapped_column(ForeignKey("workout_days.id"), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)

    # مشخصات اسکلت خالی - قبل از اجرای Slot-filling توسط TemplateGeneratorService پر می‌شه
    target_muscle: Mapped[str] = mapped_column(String(50), nullable=False)
    mechanic_preference: Mapped[Mechanic | None] = mapped_column(str_enum(Mechanic, name="workout_mechanic"), nullable=True)

    # نتیجه Slot-filling - بعد از اجرای الگوریتم پر می‌شه، تا آخرین لحظه nullable
    chosen_exercise_id: Mapped[int | None] = mapped_column(
        ForeignKey("exercises.id", ondelete="SET NULL"), nullable=True
    )

    # خروجی SetsRepsEngine
    sets: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reps_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reps_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rest_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    day: Mapped["WorkoutDay"] = relationship(back_populates="slots")
    chosen_exercise: Mapped["Exercise | None"] = relationship()