"""
app/services/sets_reps_engine.py

بر اساس هدف کاربر (Goal) و سطح آمادگیش (Level)، تعداد ست، بازه تکرار و
زمان استراحت رو محاسبه می‌کنه. جدول پایه از core/enums.py میاد (GOAL_BASE_PROFILE)
و بر اساس سطح، ضریب حجم (LEVEL_VOLUME_MULTIPLIER) و تنظیم استراحت اعمال می‌شه.

وابسته به: core.enums
"""

from dataclasses import dataclass

from app.core.enum import Goal, Level, GOAL_BASE_PROFILE, LEVEL_VOLUME_MULTIPLIER


@dataclass
class SetsRepsResult:
    sets: int
    reps_min: int
    reps_max: int
    rest_seconds: int


# تنظیم استراحت بر اساس سطح - مبتدی استراحت بیشتر برای ریکاوری کامل‌تر لازم داره،
# حرفه‌ای می‌تونه استراحت کمتری بگیره چون تراکم تمرینش بالاتره.
_REST_ADJUSTMENT_SECONDS: dict[Level, int] = {
    Level.BEGINNER: +15,
    Level.INTERMEDIATE: 0,
    Level.EXPERT: -15,
}


class SetsRepsEngine:
    def compute(self, goal: Goal, level: Level) -> SetsRepsResult:
        base = GOAL_BASE_PROFILE[goal]
        multiplier = LEVEL_VOLUME_MULTIPLIER[level]

        base_sets_avg = sum(base.sets) / 2
        sets = round(base_sets_avg * multiplier)
        sets = max(1, sets)  # هیچ‌وقت کمتر از ۱ ست منطقی نیست

        rest = base.rest_seconds + _REST_ADJUSTMENT_SECONDS[level]
        rest = max(20, rest)  # کف امن برای استراحت، مستقل از سطح

        return SetsRepsResult(
            sets=sets,
            reps_min=base.reps[0],
            reps_max=base.reps[1],
            rest_seconds=rest,
        )