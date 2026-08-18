"""
app/data/seed_exercises.py

اسکریپت یک‌باره: exercise.json رو می‌خونه، نرمالایز می‌کنه، و از طریق
ExerciseRepository.bulk_create() توی جدول exercises می‌ریزه.

نکته مهم درباره دیتاست فعلی: فایل exercise.json که الان داری فقط ۱۰۹ رکورد
داره و تا حرف B پیش می‌ره (آخرین رکورد "Butt-Ups")؛ ظاهراً یک نمونه/زیرمجموعه‌ست
نه دیتاست کامل. اگه بعداً نسخه کامل‌تری گرفتی، همین اسکریپت بدون تغییر کار می‌کنه،
فقط seed رو دوباره اجرا کن.

اجرا: python -m app.data.seed_exercises
"""

import json
from pathlib import Path

from app.database_sync import SessionLocal
from app.repository.exercise_repository import ExerciseRepository

DATA_PATH = Path(__file__).parent / "exercise.json"


def normalize_record(raw: dict) -> dict:
    """
    یک رکورد خام JSON رو به دیکشنری سازگار با ستون‌های مدل Exercise تبدیل می‌کنه.
    equipment/level/mechanic دیگه نیازی به map کردن ندارن چون مقادیر خام دیتاست
    از قبل دقیقاً با .value مقادیر Enum توی core/enums.py یکی هستن (بعد از اصلاحی
    که روی Equipment انجام دادیم). فقط camelCase -> snake_case رو تبدیل می‌کنیم.
    """
    return {
        "name": raw["name"],
        "force": raw.get("force"),
        "level": raw["level"],
        "mechanic": raw.get("mechanic"),
        "equipment": raw.get("equipment"),
        "category": raw.get("category"),
        "primary_muscles": raw.get("primaryMuscles") or [],
        "secondary_muscles": raw.get("secondaryMuscles") or [],
        "instructions": raw.get("instructions") or [],
    }


def run() -> None:
    with open(DATA_PATH, encoding="utf-8") as f:
        raw_records = json.load(f)

    normalized = [normalize_record(r) for r in raw_records]

    db = SessionLocal()
    try:
        repo = ExerciseRepository(db)
        repo.bulk_create(normalized)
        print(f"{len(normalized)} حرکت با موفقیت ذخیره شد.")
    finally:
        db.close()


if __name__ == "__main__":
    run()