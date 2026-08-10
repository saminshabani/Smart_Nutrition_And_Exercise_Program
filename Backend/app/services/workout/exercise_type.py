from enum import Enum


class ExerciseType(str, Enum):
    COMPOUND = "compound"
    ISOLATION = "isolation"

    CORE = "core"

    CARDIO = "cardio"
    PLYOMETRIC = "plyometric"
    CONDITIONING = "conditioning"

    MOBILITY = "mobility"
    STRETCHING = "stretching"
    RECOVERY = "recovery"

    BALANCE = "balance"

    UNKNOWN = "unknown"