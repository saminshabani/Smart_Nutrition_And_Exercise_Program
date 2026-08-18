"""
app/services/slot_filler.py

قلب الگوریتم Slot-filling: برای یک Slot خالی، از بین کاندیداهای مجاز
(که ExerciseRepository برگردونده) بهترین حرکت رو با امتیازدهی انتخاب می‌کنه.

وابسته به: repository.ExerciseRepository, models.Exercise/UserProfile, core.enums
"""

from dataclasses import dataclass

from app.models.workout import Exercise, UserProfile
from app.repository.exercise_repository import ExerciseRepository
from app.core.enum import Mechanic, FOCUS_AREA_TO_MUSCLES, FocusArea


@dataclass
class SlotRequest:
    """ورودی سبک برای یک Slot - جدا از مدل WorkoutSlot تا سرویس به ORM وابسته نباشه."""
    target_muscle: str
    mechanic_preference: Mechanic | None = None


class NoCandidateFoundError(Exception):
    """وقتی حتی بعد از fallback هم هیچ حرکتی برای این Slot پیدا نشد."""
    def __init__(self, muscle: str):
        super().__init__(f"هیچ حرکتی برای عضله '{muscle}' با شرایط کاربر پیدا نشد.")
        self.muscle = muscle


class SlotFillerService:
    def __init__(self, exercise_repo: ExerciseRepository):
        self.exercise_repo = exercise_repo

    def fill_slot(
        self,
        slot: SlotRequest,
        user_profile: UserProfile,
        already_used_ids: list[int],
    ) -> Exercise:
        """
        یک Slot رو با بهترین حرکت ممکن پر می‌کنه.
        already_used_ids: حرکاتی که در همین برنامه (یا همین روز) قبلاً انتخاب شدن،
        تا سیستم یک حرکت رو دوبار در برنامه تکرار نکنه.
        """
        candidates = self.exercise_repo.find_candidates_with_fallback(
            muscle=slot.target_muscle,
            user_level=user_profile.level,
            user_equipment=user_profile.equipment_available,
            mechanic=slot.mechanic_preference,
            exclude_ids=already_used_ids,
        )

        if not candidates:
            raise NoCandidateFoundError(slot.target_muscle)

        scored = [(self._score(ex, slot, user_profile), ex) for ex in candidates]

        # مرتب‌سازی نزولی بر اساس امتیاز، و برای دترمینیستیک بودن (قابل تست بودن)
        # در امتیاز مساوی بر اساس نام الفبایی مرتب می‌کنیم، نه رندوم.
        scored.sort(key=lambda pair: (-pair[0], pair[1].name))

        return scored[0][1]

    def _score(self, exercise: Exercise, slot: SlotRequest, user_profile: UserProfile) -> int:
        """
        امتیازدهی طبق طرح معماری:
        - حرکت compound اولویت داره (به‌خصوص برای Slotهای اصلی)
        - تطابق با primaryMuscles (نه فقط secondary) امتیاز بیشتر می‌ده
        - اگه عضله، جزو focus_areas انتخابی کاربر باشه، امتیاز اضافه می‌گیره
        """
        score = 0

        if exercise.mechanic == Mechanic.COMPOUND:
            score += 3

        if slot.target_muscle in exercise.primary_muscles:
            score += 2
        elif slot.target_muscle in exercise.secondary_muscles:
            score += 1

        user_focus_muscles: set[str] = set()
        for focus in user_profile.focus_areas:
            user_focus_muscles.update(FOCUS_AREA_TO_MUSCLES.get(FocusArea(focus), []))

        if user_focus_muscles & set(exercise.primary_muscles):
            score += 2

        return score