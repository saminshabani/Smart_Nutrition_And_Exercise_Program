"""
app/services/template_generator.py

اسکلت خالی برنامه رو می‌سازه: بر اساس days_per_week، نوع اسپلیت رو تعیین می‌کنه
و برای هر روز، لیستی از SlotRequest (بدون حرکت انتخاب‌شده) برمی‌گردونه.
خروجی این سرویس مستقیم ورودی SlotFillerService می‌شه.

وابسته به: core.enums, services.slot_filler.SlotRequest
"""

from dataclasses import dataclass

from app.core.enum import DaysPerWeek, SplitType, DAYS_TO_SPLIT, Mechanic, FocusArea
from app.services.slot_filltering import SlotRequest


@dataclass
class DayTemplate:
    label: str
    slots: list[SlotRequest]


# تعداد واقعی روزهای برنامه برای هر بازه - چون DaysPerWeek یک enum بازه‌ایه
# (نه عدد دقیق)، فعلاً کران بالای هر بازه رو در نظر می‌گیریم.
# اگه بعداً خواستی عدد دقیق از کاربر بگیری، این mapping باید با یک فیلد
# days_count در UserProfile جایگزین بشه.
DAYS_COUNT: dict[DaysPerWeek, int] = {
    DaysPerWeek.LOW: 2,
    DaysPerWeek.MID: 4,
    DaysPerWeek.HIGH: 6,
}


# ---------------------------------------------------------------------------
# قالب‌های ثابت هر اسپلیت - این‌جا همون "جدول ثابت" هست که قبلاً توضیح دادیم:
# فقط اسکلت (عضله + نوع مکانیک ترجیحی) رو مشخص می‌کنه، نه حرکت واقعی.
# ---------------------------------------------------------------------------
SPLIT_TEMPLATES: dict[SplitType, list[DayTemplate]] = {
    SplitType.FULL_BODY: [
        DayTemplate(
            label="Full Body",
            slots=[
                SlotRequest("quadriceps", Mechanic.COMPOUND),
                SlotRequest("chest", Mechanic.COMPOUND),
                SlotRequest("lats", Mechanic.COMPOUND),
                SlotRequest("shoulders", Mechanic.ISOLATION),
                SlotRequest("abdominals", Mechanic.ISOLATION),
            ],
        ),
    ],
    SplitType.UPPER_LOWER: [
        DayTemplate(
            label="Upper",
            slots=[
                SlotRequest("chest", Mechanic.COMPOUND),
                SlotRequest("lats", Mechanic.COMPOUND),
                SlotRequest("shoulders", Mechanic.ISOLATION),
                SlotRequest("biceps", Mechanic.ISOLATION),
                SlotRequest("triceps", Mechanic.ISOLATION),
            ],
        ),
        DayTemplate(
            label="Lower",
            slots=[
                SlotRequest("quadriceps", Mechanic.COMPOUND),
                SlotRequest("hamstrings", Mechanic.COMPOUND),
                SlotRequest("glutes", Mechanic.ISOLATION),
                SlotRequest("calves", Mechanic.ISOLATION),
            ],
        ),
    ],
    SplitType.PPL: [
        DayTemplate(
            label="Push",
            slots=[
                SlotRequest("chest", Mechanic.COMPOUND),
                SlotRequest("shoulders", Mechanic.COMPOUND),
                SlotRequest("triceps", Mechanic.ISOLATION),
            ],
        ),
        DayTemplate(
            label="Pull",
            slots=[
                SlotRequest("lats", Mechanic.COMPOUND),
                SlotRequest("middle back", Mechanic.COMPOUND),
                SlotRequest("biceps", Mechanic.ISOLATION),
            ],
        ),
        DayTemplate(
            label="Legs",
            slots=[
                SlotRequest("quadriceps", Mechanic.COMPOUND),
                SlotRequest("hamstrings", Mechanic.COMPOUND),
                SlotRequest("glutes", Mechanic.ISOLATION),
                SlotRequest("calves", Mechanic.ISOLATION),
            ],
        ),
    ],
}


class TemplateGeneratorService:
    def generate(
        self,
        days_per_week: DaysPerWeek,
        focus_areas: list[str] | None = None,
    ) -> list[DayTemplate]:
        """
        اسکلت کامل هفته رو می‌سازه: نوع اسپلیت رو از روی days_per_week تعیین می‌کنه،
        قالب روزها رو به تعداد لازم تکرار می‌کنه، و اگه کاربر focus_areas مشخص کرده،
        یک Slot اضافه (isolation) برای هرکدوم اضافه می‌کنه.
        """
        split_type = DAYS_TO_SPLIT[days_per_week]
        base_days = SPLIT_TEMPLATES[split_type]
        total_days = DAYS_COUNT[days_per_week]

        result: list[DayTemplate] = []
        for i in range(total_days):
            template = base_days[i % len(base_days)]
            # کپی عمیق لازم داریم چون قراره focus slot اضافه کنیم و نباید
            # روی آبجکت مشترک SPLIT_TEMPLATES تغییر ایجاد بشه.
            day_slots = list(template.slots)
            result.append(DayTemplate(label=template.label, slots=day_slots))

        if focus_areas:
            self._distribute_focus_slots(result, focus_areas)

        return result

    def _distribute_focus_slots(self, days: list[DayTemplate], focus_areas: list[str]) -> None:
        """
        هر focus area رو یکی‌درمیون روی روزهای برنامه پخش می‌کنه، نه این‌که همه‌شون
        رو به یک روز اضافه کنه (تا یک روز غیرمنطقی سنگین نشه).
        """
        for idx, focus in enumerate(focus_areas):
            target_day = days[idx % len(days)]
            muscle = FocusArea(focus).value if focus in [f.value for f in FocusArea] else focus
            target_day.slots.append(SlotRequest(muscle, Mechanic.ISOLATION))