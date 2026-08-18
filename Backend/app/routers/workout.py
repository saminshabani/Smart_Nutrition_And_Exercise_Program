"""
app/routers/workout.py

فقط صدا زدن WorkoutOrchestratorService - هیچ منطق الگوریتمی این‌جا نیست.
همون‌طور که در معماری گفتیم: Router -> Orchestrator -> (Template + SlotFiller + SetsReps).
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database_sync import get_db_sync
from app.core.deps import get_current_user
from app.models.user import User
from app.models.workout import UserProfile, WorkoutProgram
from app.schemas.workout import WorkoutProgramOut
from app.repository.exercise_repository import ExerciseRepository
from app.services.template_generator import TemplateGeneratorService
from app.services.slot_filltering import SlotFillerService
from app.services.sets_reps_engine import SetsRepsEngine
from app.services.workout_orchestrator import WorkoutOrchestratorService

router = APIRouter(prefix="/workout", tags=["workout"])


def get_orchestrator(db: Session = Depends(get_db_sync)) -> WorkoutOrchestratorService:
    """
    Composition root سبک: همه‌ی سرویس‌ها این‌جا کنار هم ساخته می‌شن.
    اگه پروژه بزرگ‌تر شد، این تابع می‌تونه بره توی یک container/DI جدا،
    ولی برای الان همین سطح کافیه.
    """
    exercise_repo = ExerciseRepository(db)
    return WorkoutOrchestratorService(
        db=db,
        template_generator=TemplateGeneratorService(),
        slot_filler=SlotFillerService(exercise_repo),
        sets_reps_engine=SetsRepsEngine(),
    )


@router.post("/generate", response_model=WorkoutProgramOut)
def generate_workout(
    db: Session = Depends(get_db_sync),
    current_user: User = Depends(get_current_user),
    orchestrator: WorkoutOrchestratorService = Depends(get_orchestrator),
) -> WorkoutProgramOut:
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=400,
            detail="اول باید پروفایل ورزشی رو از طریق POST /profile ثبت کنی.",
        )

    # قانون ۲۸ روزه: اگه کاربر یک برنامه فعال (هنوز منقضی‌نشده) داره، همون رو
    # برمی‌گردونیم، نه این‌که یک برنامه جدید بسازیم. کاربر باید صبر کنه تا
    # برنامه فعلی تموم بشه، بعد پروفایلش رو آپدیت کنه و دوباره درخواست بده.
    latest_program = (
        db.query(WorkoutProgram)
        .filter(WorkoutProgram.user_profile_id == profile.id)
        .order_by(WorkoutProgram.created_at.desc())
        .first()
    )
    if latest_program is not None and latest_program.expires_at > datetime.utcnow():
        return latest_program

    program = orchestrator.build_program(profile)
    return program


@router.delete("/current", status_code=204)
def delete_current_program(
        db: Session = Depends(get_db_sync),
        current_user: User = Depends(get_current_user),
) -> None:
    """
    حذف دستی برنامه فعلی کاربر - دور زدن آگاهانه‌ی قفل ۲۸ روزه، وقتی خودِ
    کاربر می‌خواد زودتر از موعد یک برنامه‌ی جدید بگیره (نه یک اتفاق خودکار).
    چون WorkoutProgram.days و WorkoutDay.slots هر دو با
    cascade="all, delete-orphan" تعریف شدن، با db.delete() روی خودِ برنامه،
    روزها و Slotهای زیرمجموعه‌ش هم خودکار پاک می‌شن - نیازی به حذف دستی
    جداگونه‌ی هرکدوم نیست.
    """
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="اول باید پروفایل ورزشی رو ثبت کنی.")

    latest_program = (
        db.query(WorkoutProgram)
        .filter(WorkoutProgram.user_profile_id == profile.id)
        .order_by(WorkoutProgram.created_at.desc())
        .first()
    )
    if latest_program is None:
        raise HTTPException(status_code=404, detail="برنامه‌ای برای حذف نداری.")

    db.delete(latest_program)
    db.commit()
