from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import pandas as pd
import io

from app.database import get_db
from app.core.deps import get_current_admin
from app.models.food import Food

router = APIRouter(prefix="/admin/foods", tags=["Admin - Foods"])

REQUIRED_COLUMNS = {
    "food_name",
    "calory",
    "fat",
    "carbohidrate",
    "protein",
    "role",
}

VALID_ROLES = {
    "heavy_main",
    "easy_main",
    "main_side",
    "side_side",
    "hot_drink",
    "cold_drink",
    "snack",
    "dessert",
    "fat_addition",
}

@router.post("/import-excel", status_code=status.HTTP_201_CREATED)
async def import_foods_from_excel(
    files: List[UploadFile] = File(...),
    overwrite: bool = False,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(get_current_admin),
):

    total_added = 0
    total_updated = 0
    total_skipped = 0
    all_errors = []

    for file in files:

        filename = file.filename.lower()
        category = file.filename.rsplit(".", 1)[0]

        # ---------- خواندن فایل ----------
        try:
            content = await file.read()

            if filename.endswith((".xlsx", ".xls")):

                df = pd.read_excel(io.BytesIO(content))

            elif filename.endswith(".csv"):

                encodings = [
                    "utf-8",
                    "utf-8-sig",
                    "cp1256",
                    "windows-1256",
                    "cp1252",
                ]

                df = None

                for enc in encodings:
                    try:
                        df = pd.read_csv(
                            io.BytesIO(content),
                            encoding="utf-8-sig",
                            sep=None,
                            engine="python",
                        )
                        break
                    except Exception:
                        continue

                if df is None:
                    raise Exception("CSV قابل خواندن نیست.")

            else:
                all_errors.append({
                    "file": file.filename,
                    "error": "فرمت فایل پشتیبانی نمی‌شود."
                })
                continue

        except Exception as e:
            all_errors.append({
                "file": file.filename,
                "error": str(e)
            })
            continue
        print(df.columns.tolist())
        print(df.head())
        # ---------- نرمال سازی ----------
        df.columns = (
            df.columns
            .str.replace("\ufeff", "", regex=False)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        missing = REQUIRED_COLUMNS - set(df.columns)

        if missing:
            all_errors.append({
                "file": file.filename,
                "error": f"ستون‌های ناقص: {', '.join(missing)}"
            })
            continue

        df = df.where(pd.notna(df), None)

        # ---------- گرفتن همه غذاهای موجود فقط یک بار ----------
        result = await db.execute(select(Food))
        existing_foods = {
            food.name_en.lower(): food
            for food in result.scalars().all()
        }

        added = 0
        updated = 0

        for index, row in df.iterrows():

            try:

                food_name = str(row["food_name"]).strip()

                if not food_name:
                    continue

                key = food_name.lower()

                role = str(row["role"]).strip().lower()

                if role not in VALID_ROLES:
                    all_errors.append({
                        "file": file.filename,
                        "row": index + 2,
                        "error": (
                            f"role نامعتبر: '{role}'. "
                            f"مقادیر مجاز: {', '.join(sorted(VALID_ROLES))}"
                        )
                    })
                    continue

                food_data = {
                    "name": food_name,
                    "name_en": food_name,
                    "calories": float(row["calory"]),
                    "fat": float(row["fat"]),
                    "carbs": float(row["carbohidrate"]),
                    "protein": float(row["protein"]),
                    "category": category,

                    "role": role,

                    "suitable_meals": (
                        "breakfast,"
                        "morning_snack,"
                        "lunch,"
                        "afternoon_snack,"
                        "dinner"
                    ),

                    "allergens": "",
                    "score_base": 1,
                    "is_active": True,
                }

                if key in existing_foods:

                    if overwrite:

                        food = existing_foods[key]

                        for k, v in food_data.items():
                            setattr(food, k, v)

                        updated += 1

                    else:
                        total_skipped += 1

                else:

                    food = Food(**food_data)

                    db.add(food)

                    existing_foods[key] = food

                    added += 1


            except Exception as e:

                all_errors.append({
                    "file": file.filename,
                    "row": index + 2,
                    "error": str(e)
                })

        total_added += added
        total_updated += updated
        print(df.columns.tolist())
        print(df.head())

    await db.commit()

    return {
        "added": total_added,
        "updated": total_updated,
        "skipped": total_skipped,
        "errors": all_errors,
    }