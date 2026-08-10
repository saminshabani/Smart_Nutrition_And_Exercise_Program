from app.schemas.user import UserPhysicalInfo, Gender, ActivityLevel, Goal

# ضریب فعالیت (Harris-Benedict / Mifflin-St Jeor)
ACTIVITY_MULTIPLIERS = {
    "sedentary":   1.2,
    "light":       1.375,
    "moderate":    1.55,
    "active":      1.725,
    "very_active": 1.9,
}

# تنظیم کالری بر اساس هدف (نسبت به TDEE)
GOAL_ADJUSTMENTS = {
    "lose_weight": -500,   # کسری ۵۰۰ کالری
    "maintain":     0,
    "gain_weight": +300,   # مازاد ۳۰۰ کالری
}


class NutritionEngine:
    def __init__(self, info: UserPhysicalInfo):
        self.info = info

        targets = self.calculate_targets()

        self.calories = targets["calories"]
        self.protein = targets["protein"]
        self.carbs = targets["carbs"]
        self.fat = targets["fat"]

    def _bmr(self) -> float:
        """Mifflin-St Jeor BMR"""
        w = self.info.weight_kg
        h = self.info.height_cm
        a = self.info.age

        if self.info.gender == Gender.male:
            return 10 * w + 6.25 * h - 5 * a + 5
        else:
            return 10 * w + 6.25 * h - 5 * a - 161

    def _tdee(self) -> float:
        multiplier = ACTIVITY_MULTIPLIERS[self.info.activity_level.value]
        return self._bmr() * multiplier

    def calculate_targets(self) -> dict[str, float]:
        tdee       = self._tdee()
        adjustment = GOAL_ADJUSTMENTS[self.info.goal.value]
        target_cal = max(tdee + adjustment, 1200.0)  # حداقل ۱۲۰۰ کالری

        # ماکروها
        protein_g = self.info.weight_kg * 2.0           # ۲ گرم به ازای هر کیلو
        fat_g     = (target_cal * 0.28) / 9             # ۲۸٪ از کالری
        # باقی کالری از کربوهیدرات
        carbs_g   = (target_cal - (protein_g * 4) - (fat_g * 9)) / 4

        return {
            "calories": round(target_cal, 1),
            "protein":  round(protein_g,  1),
            "fat":      round(fat_g,      1),
            "carbs":    round(max(carbs_g, 0), 1),
        }
