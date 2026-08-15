from enum import Enum


class MovementPattern(str, Enum):
    SQUAT = "squat"
    HINGE = "hinge"
    UNILATERAL_LEG = "unilateral_leg"

    HORIZONTAL_PUSH = "horizontal_push"
    HORIZONTAL_PULL = "horizontal_pull"

    VERTICAL_PUSH = "vertical_push"
    VERTICAL_PULL = "vertical_pull"

    KNEE_FLEXION = "knee_flexion"
    ELBOW_FLEXION = "elbow_flexion"
    ELBOW_EXTENSION = "elbow_extension"

    SHOULDER_ABDUCTION = "shoulder_abduction"
    SHOULDER_ELEVATION = "shoulder_elevation"

    HIP_ABDUCTION = "hip_abduction"
    PLANTAR_FLEXION = "plantar_flexion"

    CARRY = "carry"
    LOCOMOTION = "locomotion"

    ROTATION = "rotation"
    ANTI_ROTATION = "anti_rotation"
    ANTI_EXTENSION = "anti_extension"
    ANTI_FLEXION = "anti_flexion"
    LATERAL_FLEXION = "lateral_flexion"

    CORE_FLEXION = "core_flexion"

    PLYOMETRIC = "plyometric"
    CARDIO = "cardio"
    MOBILITY = "mobility"
    STRETCHING = "stretching"
    RECOVERY = "recovery"
    BALANCE = "balance"
    CONDITIONING = "conditioning"

    UNKNOWN = "unknown"