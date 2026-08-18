"""
app/core/enums.py

پایه‌ای‌ترین لایه‌ی پروژه — هیچ وابستگی‌ای به models/schemas/services نداره.
همه‌ی مقادیر ثابتی که در کل پایپ‌لاین (فرم کاربر، فیلتر، Slot-filling، Sets/Reps) استفاده
می‌شن این‌جا تعریف می‌شن تا هیچ‌جای پروژه رشته‌ی خام (magic string) نداشته باشیم.
"""

from enum import Enum


# ---------------------------------------------------------------------------
# سطح آمادگی کاربر
# ---------------------------------------------------------------------------
class Level(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


# ترتیب سختی سطوح - برای مقایسه استفاده می‌شه (مثلاً user_level >= exercise.level)
_LEVEL_ORDER: dict[Level, int] = {
    Level.BEGINNER: 0,
    Level.INTERMEDIATE: 1,
    Level.EXPERT: 2,
}


def allowed_levels(user_level: Level) -> list[Level]:
    """
    سطوحی که یک کاربر با سطح مشخص مجاز به دیدن حرکاتشونه.
    مبتدی فقط beginner، متوسط تا intermediate، حرفه‌ای همه چیز.
    این تابع هم در ExerciseRepository (فیلتر حرکت) و هم در SetsRepsEngine
    (تعیین شدت تمرین) استفاده می‌شه.
    """
    threshold = _LEVEL_ORDER[user_level]
    return [lvl for lvl, order in _LEVEL_ORDER.items() if order <= threshold]


# ---------------------------------------------------------------------------
# هدف تمرینی کاربر
# ---------------------------------------------------------------------------
class Goal(str, Enum):
    STRENGTH = "strength"
    MUSCLE_GAIN = "muscle_gain"
    FAT_LOSS = "fat_loss"


# ---------------------------------------------------------------------------
# تعداد روزهای تمرین در هفته -> ورودی مستقیم Template Generator
# ---------------------------------------------------------------------------
class DaysPerWeek(str, Enum):
    LOW = "1-2"
    MID = "3-4"
    HIGH = "5-6"


# ---------------------------------------------------------------------------
# نوع اسپلیت -> خروجی Template Generator
# ---------------------------------------------------------------------------
class SplitType(str, Enum):
    FULL_BODY = "full_body"
    UPPER_LOWER = "upper_lower"
    PPL = "ppl"


DAYS_TO_SPLIT: dict[DaysPerWeek, SplitType] = {
    DaysPerWeek.LOW: SplitType.FULL_BODY,
    DaysPerWeek.MID: SplitType.UPPER_LOWER,
    DaysPerWeek.HIGH: SplitType.PPL,
}


# ---------------------------------------------------------------------------
# ناحیه تمرکز بدنی -> نگاشت مستقیم به مقادیر primaryMuscles در دیتاست
# ---------------------------------------------------------------------------
class FocusArea(str, Enum):
    ABS = "abdominals"
    GLUTES = "glutes"
    CHEST = "chest"
    ARMS = "arms"  # در فیلتر واقعی به بایسپس/ترایسپس/فورآرمز باز می‌شه


FOCUS_AREA_TO_MUSCLES: dict[FocusArea, list[str]] = {
    FocusArea.ABS: ["abdominals"],
    FocusArea.GLUTES: ["glutes"],
    FocusArea.CHEST: ["chest"],
    FocusArea.ARMS: ["biceps", "triceps", "forearms"],
}


# ---------------------------------------------------------------------------
# تجهیزات در دسترس -> باید دقیقاً با مقادیر equipment در exercise.json هم‌راستا باشه
# این مقادیر از خودِ فایل exercise.json استخراج شدن (۱۳ مقدار یکتا + null):
# ['bands','barbell','body only','cable','dumbbell','e-z curl bar',
#  'exercise ball','foam roll','kettlebells','machine','medicine ball','other', None]
# ---------------------------------------------------------------------------
class Equipment(str, Enum):
    NONE = "body only"
    DUMBBELL = "dumbbell"        # مفرده، نه dumbbells - این رو با نسخه قبلی enums.py اصلاح کن
    BAND = "bands"
    MACHINE = "machine"
    BARBELL = "barbell"
    KETTLEBELL = "kettlebells"
    CABLE = "cable"
    FOAM_ROLL = "foam roll"
    EXERCISE_BALL = "exercise ball"
    MEDICINE_BALL = "medicine ball"
    EZ_CURL_BAR = "e-z curl bar"
    OTHER = "other"


# رکوردهایی که در دیتاست equipment=null دارن (مثل "Adductor/Groin") به‌عنوان
# "بدون نیاز به تجهیزات خاص" در نظر گرفته می‌شن و همیشه مجاز هستن.
NULL_EQUIPMENT_IS_UNIVERSAL = True


# ---------------------------------------------------------------------------
# جنسیت -> فقط برای شخصی‌سازی محتوای متنی/لحن، در فیلتر حرکت استفاده نمی‌شه
# ---------------------------------------------------------------------------
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


# ---------------------------------------------------------------------------
# نوع مکانیک حرکت -> برای امتیازدهی در Slot-filling (compound اولویت داره)
# ---------------------------------------------------------------------------
class Mechanic(str, Enum):
    COMPOUND = "compound"
    ISOLATION = "isolation"


# ---------------------------------------------------------------------------
# جدول شدت تمرین بر اساس هدف -> ورودی پایه SetsRepsEngine (قبل از ضریب سطح)
# ---------------------------------------------------------------------------
class SetsRepsProfile:
    def __init__(self, sets: tuple[int, int], reps: tuple[int, int], rest_seconds: int):
        self.sets = sets
        self.reps = reps
        self.rest_seconds = rest_seconds


GOAL_BASE_PROFILE: dict[Goal, SetsRepsProfile] = {
    Goal.STRENGTH: SetsRepsProfile(sets=(3, 5), reps=(3, 6), rest_seconds=150),
    Goal.MUSCLE_GAIN: SetsRepsProfile(sets=(3, 4), reps=(8, 12), rest_seconds=75),
    Goal.FAT_LOSS: SetsRepsProfile(sets=(2, 3), reps=(15, 20), rest_seconds=40),
}


# ضریب حجم بر اساس سطح - روی sets پایه ضرب می‌شه (در SetsRepsEngine)
LEVEL_VOLUME_MULTIPLIER: dict[Level, float] = {
    Level.BEGINNER: 0.7,
    Level.INTERMEDIATE: 1.0,
    Level.EXPERT: 1.2,
}


# ---------------------------------------------------------------------------
# مدت اعتبار یک برنامه - کاربر تا این تعداد روز باید همین برنامه رو دنبال کنه،
# قبل از این‌که بشه دوباره پروفایلش رو آپدیت کنه و برنامه جدید بگیره.
# ---------------------------------------------------------------------------
PROGRAM_VALIDITY_DAYS = 28


# ---------------------------------------------------------------------------
# دسته‌هایی که هیچ‌وقت نباید یک Slot تمرینی رو پر کنن، حتی اگه از نظر عضله
# match بشن. مثلاً یک حرکت "stretching" ممکنه chest رو به‌عنوان عضله دوم
# داشته باشه، ولی حرکت کششی نمی‌تونه جای یک ست تمرین قدرتی سینه رو بگیره.
# دسته‌های موجود در دیتاست: cardio, plyometrics, powerlifting, strength,
# stretching, strongman. فعلاً فقط stretching رو مستقیم حذف می‌کنیم.
# ---------------------------------------------------------------------------
EXCLUDED_SLOT_CATEGORIES = {"stretching"}