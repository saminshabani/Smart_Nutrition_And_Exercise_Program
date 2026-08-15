from enum import Enum


class WorkoutGoal(str, Enum):
    STRENGTH = "strength"
    HYPERTROPHY = "hypertrophy"
    MAINTENANCE = "maintenance"


class WorkoutLocation(str, Enum):
    HOME = "home"
    GYM = "gym"
    OUTDOOR = "outdoor"


class EquipmentType(str, Enum):
    DUMBBELL = "dumbbell"
    RESISTANCE_BAND = "resistance_band"
    NONE = "none"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class FocusArea(str, Enum):
    ABS = "abs"
    GLUTES = "glutes"
    CHEST = "chest"
    ARMS = "arms"


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"