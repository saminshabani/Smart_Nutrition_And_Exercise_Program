from pydantic import BaseModel, Field, field_validator

from app.services.workout.user_preferences import (
    WorkoutGoal,
    WorkoutLocation,
    EquipmentType,
    Gender,
    FocusArea,
    ExperienceLevel,
)


class WorkoutPlanRequest(BaseModel):
    location: WorkoutLocation

    training_days: int = Field(
        ge=1,
        le=6,
    )

    goal: WorkoutGoal

    equipment: list[EquipmentType] = Field(
        min_length=1,
    )

    experience_level: ExperienceLevel

    gender: Gender

    focus_area: FocusArea

    height_cm: float = Field(
        gt=0,
        le=250,
    )

    weight_kg: float = Field(
        gt=0,
        le=300,
    )

    target_weight_kg: float = Field(
        gt=0,
        le=300,
    )

    age: int = Field(
        ge=13,
        le=100,
    )

    @field_validator("equipment")
    @classmethod
    def validate_equipment(
        cls,
        equipment: list[EquipmentType],
    ) -> list[EquipmentType]:

        has_none = EquipmentType.NONE in equipment

        if has_none and len(equipment) > 1:
            raise ValueError(
                "Equipment 'none' cannot be combined with other equipment."
            )

        return equipment