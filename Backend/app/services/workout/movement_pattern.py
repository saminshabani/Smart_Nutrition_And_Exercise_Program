from enum import Enum


class MovementPattern(str, Enum):
    SQUAT = "squat"
    HINGE = "hinge"

    UNILATERAL_LEG = "unilateral_leg"

    HORIZONTAL_PUSH = "horizontal_push"
    HORIZONTAL_PULL = "horizontal_pull"

    VERTICAL_PUSH = "vertical_push"
    VERTICAL_PULL = "vertical_pull"

    CARRY = "carry"

    ROTATION = "rotation"
    ANTI_ROTATION = "anti_rotation"
    ANTI_EXTENSION = "anti_extension"
    ANTI_FLEXION = "anti_flexion"

    UNKNOWN = "unknown"