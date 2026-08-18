"""
app/routers/profile.py

فقط validation (از طریق schema) و صدا زدن دیتابیس - هیچ منطق الگوریتمی این‌جا نیست.

فرض‌های زیر رو با ساختار واقعی پروژه‌ت تطبیق بده:
- app.database.get_db  : dependency ای که یک Session می‌سازه و می‌بنده
- app.core.security.get_current_user : dependency ای که از روی توکن/سشن،
  آبجکت User لاگین‌شده رو برمی‌گردونه (چون گفتی احراز هویت داری)
اگه اسم یا مسیر این دو تا فرق داره، فقط همین دو ایمپورت رو اصلاح کن.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database_sync import get_db_sync
from app.core.deps import get_current_user
from app.models.user import User
from app.models.workout import UserProfile
from app.schemas.profile_workout import UserProfileIn, UserProfileOut

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("", response_model=UserProfileOut)
def create_or_update_profile(
    payload: UserProfileIn,
    db: Session = Depends(get_db_sync),
    current_user: User = Depends(get_current_user),
) -> UserProfile:
    """
    یک کاربر فقط یک پروفایل ورزشی داره (رابطه یک‌به‌یک، طبق مدل).
    اگه از قبل داشته، آپدیت می‌کنیم؛ وگرنه می‌سازیم.
    """
    existing = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

    data = payload.model_dump()
    # لیست‌های Enum رو به رشته خام تبدیل می‌کنیم چون ستون‌های JSON در مدل، رشته می‌خوان
    data["equipment_available"] = [e.value for e in payload.equipment_available]
    data["focus_areas"] = [f.value for f in payload.focus_areas]

    if existing:
        for key, value in data.items():
            setattr(existing, key, value)
        profile = existing
    else:
        profile = UserProfile(user_id=current_user.id, **data)
        db.add(profile)

    db.commit()
    db.refresh(profile)
    return profile


@router.get("", response_model=UserProfileOut)
def get_my_profile(
    db: Session = Depends(get_db_sync),
    current_user: User = Depends(get_current_user),
) -> UserProfile:
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="هنوز پروفایل ورزشی ثبت نکردی.")
    return profile