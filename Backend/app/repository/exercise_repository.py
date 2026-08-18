"""
app/repository/exercise_repository.py

لایه‌ی دسترسی داده برای Exercise. این‌جا دقیقاً همون الگوریتم
Rule-based Filtering که در طرح معماری گفتیم پیاده می‌شه:
سطح کاربر + تجهیزات موجود + عضله هدف.

وابسته به: models.Exercise, core.enums
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workout import Exercise
from app.core.enum import (
    Level,
    Equipment,
    Mechanic,
    allowed_levels,
    NULL_EQUIPMENT_IS_UNIVERSAL,
    EXCLUDED_SLOT_CATEGORIES,
)


class ExerciseRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_candidates(
        self,
        muscle: str,
        user_level: Level,
        user_equipment: list[Equipment],
        mechanic: Mechanic | None = None,
        exclude_ids: list[int] | None = None,
    ) -> list[Exercise]:
        """
        کاندیداهای مجاز برای پر کردن یک Slot.
        فیلتر سه‌مرحله‌ای: سطح -> تجهیزات -> عضله.
        ترتیب فیلترها عمدیه: سطح و تجهیزات ارزون‌ترن (اندیس‌دار روی ستون enum)،
        فیلتر عضله چون روی JSON هست گرون‌تره و باید آخر اجرا بشه.
        """
        exclude_ids = exclude_ids or []

        allowed = allowed_levels(user_level)

        # user_equipment ممکنه enum باشه (وقتی مستقیم از schema میاد) یا رشته خام
        # (وقتی از دیتابیس لود شده، چون ستون equipment_available یک JSON از
        # رشته‌هاست، نه enum پایتونی). این‌جا با هر دو حالت سازگاریم.
        equipment_values = [e.value if isinstance(e, Equipment) else e for e in user_equipment]
        query = select(Exercise).where(Exercise.level.in_(allowed))

        # دسته‌هایی مثل stretching هیچ‌وقت نباید یک Slot تمرینی رو پر کنن،
        # حتی اگه از نظر عضله match بشن (مثلاً یک حرکت کششی که chest رو
        # به‌عنوان عضله دوم داره نباید جای یک ست تمرین سینه رو بگیره).
        query = query.where(
            (Exercise.category.is_(None)) | (Exercise.category.notin_(EXCLUDED_SLOT_CATEGORIES))
        )

        if exclude_ids:
            query = query.where(Exercise.id.notin_(exclude_ids))

        if mechanic is not None:
            query = query.where(Exercise.mechanic == mechanic)

        # فیلتر تجهیزات: equipment=None در دیتاست یعنی "بدون نیاز خاص"
        # طبق تصمیمی که در core/enums.py مستند شده، این رکوردها همیشه مجازن.
        if NULL_EQUIPMENT_IS_UNIVERSAL:
            query = query.where(
                (Exercise.equipment.is_(None)) | (Exercise.equipment.in_(equipment_values))
            )
        else:
            query = query.where(Exercise.equipment.in_(equipment_values))

        rows = self.db.execute(query).scalars().all()

        # فیلتر عضله در پایتون انجام می‌شه، نه SQL — چون primary_muscles/secondary_muscles
        # ستون JSON هستن و عملگر containment (مثل @> در Postgres) بین دیتابیس‌ها یکسان نیست.
        # اگه بعداً فقط روی Postgres کار کردی و candidate pool خیلی بزرگ شد،
        # این بخش رو می‌شه با func.jsonb_exists جایگزین کرد تا فیلتر توی خود SQL بره.
        candidates = [
            ex for ex in rows
            if muscle in ex.primary_muscles or muscle in ex.secondary_muscles
        ]

        return candidates

    def find_candidates_with_fallback(
        self,
        muscle: str,
        user_level: Level,
        user_equipment: list[Equipment],
        mechanic: Mechanic | None = None,
        exclude_ids: list[int] | None = None,
    ) -> list[Exercise]:
        """
        همون find_candidates، ولی اگه استخر خالی برگشت، فیلتر مکانیک رو نرم می‌کنه.
        این دقیقاً همون قدم fallback در الگوریتم Slot-filling هست
        (وقتی هیچ حرکت compound با این تجهیزات برای این عضله پیدا نشد).
        """
        result = self.find_candidates(
            muscle=muscle,
            user_level=user_level,
            user_equipment=user_equipment,
            mechanic=mechanic,
            exclude_ids=exclude_ids,
        )
        if result:
            return result

        if mechanic is not None:
            return self.find_candidates(
                muscle=muscle,
                user_level=user_level,
                user_equipment=user_equipment,
                mechanic=None,
                exclude_ids=exclude_ids,
            )
        return result

    def bulk_create(self, exercises: list[dict]) -> None:
        """برای seed_exercises.py - ریختن دیتاست خام توی دیتابیس."""
        self.db.bulk_insert_mappings(Exercise, exercises)
        self.db.commit()

    def get_by_id(self, exercise_id: int) -> Exercise | None:
        return self.db.get(Exercise, exercise_id)