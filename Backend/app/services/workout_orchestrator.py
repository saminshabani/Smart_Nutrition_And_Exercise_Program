"""
app/services/workout_orchestrator.py

جایی که کل پایپ‌لاین به هم وصل می‌شه:
TemplateGenerator -> برای هر Slot: SlotFiller -> SetsRepsEngine -> ذخیره در دیتابیس.

این سرویس تنها جاییه که همه‌ی سرویس‌های دیگه رو کنار هم می‌بینه؛ خودِ آن‌ها
از وجود هم خبر ندارن (decoupled) - دقیقاً طبق چیزی که در معماری اولیه گفتیم.

وابسته به: همه‌ی services دیگه + models + core.enums
"""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.enum import DAYS_TO_SPLIT, PROGRAM_VALIDITY_DAYS
from app.models.workout import UserProfile, WorkoutProgram, WorkoutDay, WorkoutSlot
from app.services.template_generator import TemplateGeneratorService
from app.services.slot_filltering import SlotFillerService, NoCandidateFoundError
from app.services.sets_reps_engine import SetsRepsEngine


class WorkoutOrchestratorService:
    def __init__(
        self,
        db: Session,
        template_generator: TemplateGeneratorService,
        slot_filler: SlotFillerService,
        sets_reps_engine: SetsRepsEngine,
    ):
        self.db = db
        self.template_generator = template_generator
        self.slot_filler = slot_filler
        self.sets_reps_engine = sets_reps_engine

    def build_program(self, user_profile: UserProfile) -> WorkoutProgram:
        split_type = DAYS_TO_SPLIT[user_profile.days_per_week]
        day_templates = self.template_generator.generate(
            days_per_week=user_profile.days_per_week,
            focus_areas=user_profile.focus_areas,
        )

        program = WorkoutProgram(
            user_profile_id=user_profile.id,
            split_type=split_type,
            expires_at=datetime.utcnow() + timedelta(days=PROGRAM_VALIDITY_DAYS),
        )
        self.db.add(program)
        self.db.flush()  # program.id لازمه قبل از ساخت WorkoutDayها

        # ردیابی حرکات استفاده‌شده در کل برنامه (نه فقط یک روز)، تا یک حرکت
        # دوبار در کل هفته تکرار نشه.
        used_exercise_ids: list[int] = []

        for day_index, day_template in enumerate(day_templates):
            day = WorkoutDay(
                program_id=program.id,
                day_index=day_index,
                label=day_template.label,
            )
            self.db.add(day)
            self.db.flush()

            for order_index, slot_request in enumerate(day_template.slots):
                try:
                    exercise = self.slot_filler.fill_slot(
                        slot=slot_request,
                        user_profile=user_profile,
                        already_used_ids=used_exercise_ids,
                    )
                except NoCandidateFoundError:
                    # هیچ حرکتی با شرایط فعلی پیدا نشد. به‌جای متوقف کردن کل
                    # ساخت برنامه، Slot رو خالی ثبت می‌کنیم تا کاربر بعداً
                    # بتونه دستی جایگزینش کنه - تصمیم UX، نه خطای سیستمی.
                    exercise = None

                sr = self.sets_reps_engine.compute(user_profile.goal, user_profile.level)

                slot = WorkoutSlot(
                    day_id=day.id,
                    order_index=order_index,
                    target_muscle=slot_request.target_muscle,
                    mechanic_preference=slot_request.mechanic_preference,
                    chosen_exercise_id=exercise.id if exercise else None,
                    sets=sr.sets,
                    reps_min=sr.reps_min,
                    reps_max=sr.reps_max,
                    rest_seconds=sr.rest_seconds,
                )
                self.db.add(slot)

                if exercise is not None:
                    used_exercise_ids.append(exercise.id)

        self.db.commit()
        self.db.refresh(program)
        return program