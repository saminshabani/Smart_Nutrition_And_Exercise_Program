# app/scripts/analyze_exercises.py

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = BASE_DIR / "data" / "exercise" / "exercise.json"

OUTPUT_DIR = BASE_DIR / "data" / "exercise"
OUTPUT_PATH = OUTPUT_DIR / "classified_exercises.json"


# ============================================================
# TAXONOMY
# ============================================================

VALID_MOVEMENT_PATTERNS = {
    "squat",
    "hinge",
    "unilateral_leg",

    "horizontal_push",
    "horizontal_pull",

    "vertical_push",
    "vertical_pull",

    "knee_flexion",
    "elbow_flexion",
    "elbow_extension",

    "shoulder_abduction",
    "shoulder_elevation",

    "anti_extension",
    "anti_flexion",
    "anti_rotation",
    "lateral_flexion",

    "carry",
    "locomotion",

    "plantar_flexion",

    "core_flexion",

    "plyometric",
    "cardio",
    "mobility",
    "stretching",
    "recovery",
    "balance",
    "conditioning",

    "unknown",
}

VALID_EXERCISE_TYPES = {
    "compound",
    "isolation",
    "core",
    "cardio",
    "plyometric",
    "conditioning",
    "mobility",
    "stretching",
    "recovery",
    "balance",
    "unknown",
}

# ============================================================
# HELPERS
# ============================================================

def normalize_text(value: Any) -> str:
    """
    Normalize arbitrary text for matching.

    Examples:
        "Barbell  Hip-Thrust" -> "barbell hip thrust"
        "Bent-Over Row"       -> "bent over row"
    """
    if value is None:
        return ""

    text = str(value).lower()

    text = text.replace("&", " and ")
    text = text.replace("/", " ")
    text = text.replace("-", " ")
    text = text.replace("_", " ")

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def text_contains(text: str, *terms: str) -> bool:
    """
    True if at least one term exists in normalized text.
    """
    normalized_terms = [
        normalize_text(term)
        for term in terms
        if term
    ]

    return any(term in text for term in normalized_terms)


def text_contains_all(text: str, *terms: str) -> bool:
    """
    True if all terms exist in normalized text.
    """
    normalized_terms = [
        normalize_text(term)
        for term in terms
        if term
    ]

    return all(term in text for term in normalized_terms)


def make_search_text(exercise: dict[str, Any]) -> str:
    """
    Build a searchable representation from the actual dataset fields.

    We intentionally include:
        name
        category
        force
        mechanic
        equipment
        primaryMuscles
        secondaryMuscles
        instructions
    """

    parts: list[str] = []

    for key in (
        "name",
        "category",
        "force",
        "mechanic",
        "equipment",
    ):
        value = exercise.get(key)

        if value:
            parts.append(str(value))

    for key in (
        "primaryMuscles",
        "secondaryMuscles",
    ):
        value = exercise.get(key)

        if isinstance(value, list):
            parts.extend(str(item) for item in value)

    instructions = exercise.get("instructions")

    if isinstance(instructions, list):
        parts.extend(str(item) for item in instructions)

    elif instructions:
        parts.append(str(instructions))

    return normalize_text(" ".join(parts))


def get_category(exercise: dict[str, Any]) -> str:
    return normalize_text(exercise.get("category"))


def get_name(exercise: dict[str, Any]) -> str:
    return normalize_text(exercise.get("name"))


def get_force(exercise: dict[str, Any]) -> str:
    return normalize_text(exercise.get("force"))


def get_mechanic(exercise: dict[str, Any]) -> str:
    return normalize_text(exercise.get("mechanic"))


def get_primary_muscles(exercise: dict[str, Any]) -> set[str]:
    muscles = exercise.get("primaryMuscles", [])

    if not isinstance(muscles, list):
        return set()

    return {
        normalize_text(muscle)
        for muscle in muscles
        if muscle
    }


def get_secondary_muscles(exercise: dict[str, Any]) -> set[str]:
    muscles = exercise.get("secondaryMuscles", [])

    if not isinstance(muscles, list):
        return set()

    return {
        normalize_text(muscle)
        for muscle in muscles
        if muscle
    }


def get_instructions(exercise: dict[str, Any]) -> str:
    instructions = exercise.get("instructions", [])

    if isinstance(instructions, list):
        return normalize_text(" ".join(str(x) for x in instructions))

    return normalize_text(instructions)


def muscle_contains(
    exercise: dict[str, Any],
    *muscles: str,
) -> bool:
    all_muscles = (
        get_primary_muscles(exercise)
        | get_secondary_muscles(exercise)
    )

    normalized = {
        normalize_text(muscle)
        for muscle in muscles
    }

    return bool(all_muscles & normalized)

def classify_exercise_type(
    exercise: dict[str, Any],
    movement_classification: dict[str, Any],
) -> str:

    category = get_category(exercise)
    mechanic = get_mechanic(exercise)
    name = get_name(exercise)

    movement_pattern = movement_classification.get(
        "movement_pattern",
        "unknown",
    )

    # ========================================================
    # 1. EXPLICIT TRAINING CATEGORIES
    # ========================================================

    if category == "cardio":
        return "cardio"

    if category == "plyometrics":
        return "plyometric"

    # ========================================================
    # 2. RECOVERY / MOBILITY / STRETCHING
    # ========================================================

    if category == "stretching":

        if text_contains(
            name,
            "smr",
            "foam roll",
            "foam roller",
            "self myofascial",
        ):
            return "recovery"

        return "stretching"

    # ========================================================
    # 3. CONDITIONING
    # ========================================================

    if text_contains(
        name,
        "battle rope",
        "battling rope",
        "sled",
        "drag",
        "bear crawl",
        "farmer walk",
        "farmer carry",
        "suitcase carry",
        "waiter carry",
    ):
        return "conditioning"

    if movement_pattern == "conditioning":
        return "conditioning"

    # ========================================================
    # 4. BALANCE
    # ========================================================

    if text_contains(
        name,
        "balance board",
        "bosu",
        "single leg balance",
    ):
        return "balance"

    if movement_pattern == "balance":
        return "balance"

    # ========================================================
    # 5. CORE
    # ========================================================

    core_name_patterns = (
        "crunch",
        "sit up",
        "sit-up",
        "ab rollout",
        "ab wheel",
        "ab roller",
        "rollout",
        "plank",
        "hip raise",
        "leg raise",
        "knee raise",
        "russian twist",
        "russian twists",
        "bicycle crunch",
        "bicycle",
        "heel toucher",
        "heel touchers",
        "v up",
        "v-up",
        "jackknife",
        "toe touch",
        "toe touches",
    )

    if text_contains(name, *core_name_patterns):
        return "core"

    if movement_pattern in {
        "anti_extension",
        "anti_flexion",
        "anti_rotation",
        "lateral_flexion",
        "core_flexion",
    }:
        return "core"

    # ========================================================
    # 6. MOBILITY
    # ========================================================

    if movement_pattern == "mobility":
        return "mobility"

    # ========================================================
    # 7. RECOVERY
    # ========================================================

    if movement_pattern == "recovery":
        return "recovery"

    # ========================================================
    # 8. PLYOMETRIC
    # ========================================================

    if movement_pattern == "plyometric":
        return "plyometric"

    # ========================================================
    # 9. CARDIO
    # ========================================================

    if movement_pattern == "cardio":
        return "cardio"

    # ========================================================
    # 10. CONDITIONING
    # ========================================================

    if movement_pattern == "conditioning":
        return "conditioning"

    # ========================================================
    # 11. MECHANIC-BASED CLASSIFICATION
    # ========================================================

    if mechanic == "compound":
        return "compound"

    if mechanic == "isolation":
        return "isolation"

    # ========================================================
    # 12. UNKNOWN
    # ========================================================

    return "unknown"

# ============================================================
# RESULT OBJECT
# ============================================================

def result(
    pattern: str,
    confidence: float,
    rule_id: str,
    reason: str,
) -> dict[str, Any]:
    return {
        "movement_pattern": pattern,
        "confidence": round(confidence, 2),
        "rule_id": rule_id,
        "reason": reason,
    }


# ============================================================
# LEVEL 1
# EXPLICIT NAME RULES
# ============================================================


def classify_explicit_name(
    exercise: dict[str, Any],
) -> dict[str, Any] | None:

    name = get_name(exercise)
    text = make_search_text(exercise)

    # ========================================================
    # CALF RAISE
    # ========================================================

    if text_contains(
        name,
        "calf raise",
        "calf raises",
        "seated calf raise",
        "standing calf raise",
    ):
        return result(
            "plantar_flexion",
            0.99,
            "N021_PLANTAR_FLEXION_CALF_RAISE",
            "Explicit calf-raise exercise; primary action is ankle plantar flexion.",
        )

    # ========================================================
    # HIP ABDUCTION
    # ========================================================

    if text_contains(
        name,
        "hip abduction",
        "hip abductions",
        "band hip adductions",
    ):
        return result(
            "hip_abduction",
            0.96,
            "N022_HIP_ABDUCTION",
            "Exercise moves the leg laterally away from the body's midline.",
        )

    # ========================================================
    # BODYWEIGHT SQUAT
    # ========================================================

    if text_contains(
        name,
        "bodyweight squat",
        "body weight squat",
        "air squat",
    ):
        return result(
            "squat",
            0.99,
            "N023_BODYWEIGHT_SQUAT",
            "Explicit bodyweight squat exercise name.",
        )

    # ========================================================
    # BODYWEIGHT FLYES
    # ========================================================

    if text_contains(
        name,
        "bodyweight flyes",
        "bodyweight fly",
        "body weight flyes",
        "body weight fly",
    ):
        return result(
            "horizontal_push",
            0.94,
            "N024_BODYWEIGHT_FLY",
            "Bodyweight fly is a horizontal chest pressing/adduction pattern.",
        )

    # ========================================================
    # BUTTERFLY
    # ========================================================

    if name == "butterfly":
        return result(
            "horizontal_push",
            0.94,
            "N025_BUTTERFLY_CHEST",
            "Butterfly is a chest fly movement performed in the horizontal plane.",
        )

    # ========================================================
    # BACK FLYES
    # ========================================================

    if text_contains(
        name,
        "back flyes",
        "back fly",
        "reverse fly",
        "rear fly",
    ):
        return result(
            "horizontal_pull",
            0.91,
            "N026_BACK_FLY_HORIZONTAL_PULL",
            "Rear/back fly movement is treated as horizontal pulling/scapular retraction.",
        )

    # ========================================================
    # LOW-PULLEY SIDE LATERAL
    # ========================================================

    if text_contains(
        name,
        "side lateral",
        "lateral raise",
        "side raise",
    ):
        return result(
            "shoulder_abduction",
            0.96,
            "N027_SHOULDER_ABDUCTION_LATERAL",
            "Lateral raise explicitly abducts the shoulder.",
        )

    # ========================================================
    # HANG CLEAN
    # ========================================================

    if text_contains(
        name,
        "hang clean",
        "clean from the hang",
        "clean from hang",
    ):
        return result(
            "hinge",
            0.94,
            "N028_HANG_CLEAN",
            "Hang clean is an explosive hip-extension/hinge movement.",
        )


    # --------------------------------------------------------
    # SQUAT
    # --------------------------------------------------------

    if text_contains(
        name,
        "barbell squat",
        "full squat",
        "box squat",
        "hack squat",
        "front squat",
        "zercher squat",
        "safety bar squat",
        "smith machine squat",
    ):
        return result(
            "squat",
            0.99,
            "N001_SQUAT_NAME",
            "Explicit squat exercise name.",
        )

    # --------------------------------------------------------
    # LUNGES / STEP UPS
    # --------------------------------------------------------

    if text_contains(
        name,
        "lunge",
        "split squat",
        "step up",
        "step-up",
        "bulgarian split",
    ):
        return result(
            "unilateral_leg",
            0.99,
            "N002_UNILATERAL_LEG_NAME",
            "Explicit unilateral leg exercise name.",
        )

    # --------------------------------------------------------
    # DEADLIFT / HIP HINGE
    # --------------------------------------------------------

    if text_contains(
        name,
        "deadlift",
        "romanian deadlift",
        "stiff leg deadlift",
        "straight leg deadlift",
        "good morning",
        "hip thrust",
        "glute bridge",
        "glute bridge",
        "butt lift bridge",
    ):
        return result(
            "hinge",
            0.99,
            "N003_HINGE_NAME",
            "Explicit hip hinge / hip extension exercise name.",
        )

    # --------------------------------------------------------
    # ROWS
    # --------------------------------------------------------

    if text_contains(
        name,
        "row",
        "rear delt row",
        "bodyweight mid row",
    ):
        # Exceptions handled later.
        if not text_contains(
            name,
            "upright row",
        ):
            return result(
                "horizontal_pull",
                0.96,
                "N004_HORIZONTAL_PULL_ROW",
                "Exercise name explicitly identifies a rowing movement.",
            )

    # --------------------------------------------------------
    # PULL UPS / CHIN UPS
    # --------------------------------------------------------

    if text_contains(
        name,
        "pull up",
        "pullup",
        "pull-up",
        "chin up",
        "chinup",
        "chin-up",
        "lat pulldown",
        "pulldown",
        "pulldown",
    ):
        return result(
            "vertical_pull",
            0.98,
            "N005_VERTICAL_PULL_NAME",
            "Explicit vertical pulling exercise name.",
        )

    # --------------------------------------------------------
    # PRESSING
    # --------------------------------------------------------

    if text_contains(
        name,
        "bench press",
        "floor press",
        "board press",
        "chest press",
        "guillotine bench press",
        "push up",
        "pushup",
        "push-up",
        "dip",
        "dips",
    ):
        return result(
            "horizontal_push",
            0.98,
            "N006_HORIZONTAL_PUSH_NAME",
            "Explicit horizontal pressing exercise name.",
        )

    # --------------------------------------------------------
    # OVERHEAD PRESS
    # --------------------------------------------------------

    if text_contains(
        name,
        "overhead press",
        "shoulder press",
        "military press",
        "arnold press",
        "arnold dumbbell press",
        "kettlebell press",
        "bradford",
        "rocky press",
    ):
        return result(
            "vertical_push",
            0.98,
            "N007_VERTICAL_PUSH_NAME",
            "Explicit overhead pressing exercise name.",
        )

    # --------------------------------------------------------
    # CURLS
    # --------------------------------------------------------

    if text_contains(
        name,
        "curl",
        "hammer curl",
        "preacher curl",
        "concentration curl",
        "incline dumbbell curl",
    ):
        return result(
            "elbow_flexion",
            0.98,
            "N008_ELBOW_FLEXION_CURL",
            "Explicit elbow-flexion / curl exercise name.",
        )

    # --------------------------------------------------------
    # TRICEPS EXTENSION
    # --------------------------------------------------------

    if text_contains(
        name,
        "skull crusher",
        "tricep extension",
        "triceps extension",
        "pressdown",
        "pushdown",
        "tricep pushdown",
        "triceps pushdown",
    ):
        return result(
            "elbow_extension",
            0.98,
            "N009_ELBOW_EXTENSION_TRICEPS",
            "Explicit triceps extension exercise name.",
        )

    # --------------------------------------------------------
    # SHRUG
    # --------------------------------------------------------

    if text_contains(
        name,
        "shrug",
    ):
        return result(
            "shoulder_elevation",
            0.99,
            "N010_SHOULDER_ELEVATION_SHRUG",
            "Shrug is shoulder elevation, not horizontal pulling.",
        )

    # --------------------------------------------------------
    # SIDE BEND
    # --------------------------------------------------------

    if text_contains(
        name,
        "side bend",
        "side bends",
        "lateral flexion",
    ):
        return result(
            "lateral_flexion",
            0.98,
            "N011_LATERAL_FLEXION",
            "Explicit lateral trunk flexion exercise.",
        )

    # --------------------------------------------------------
    # ROLLOUT
    # --------------------------------------------------------

    if text_contains(
        name,
        "ab rollout",
        "ab wheel",
        "ab roller",
        "rollout",
    ):
        return result(
            "anti_extension",
            0.99,
            "N012_ANTI_EXTENSION_ROLLOUT",
            "Rollout trains trunk anti-extension.",
        )

    # --------------------------------------------------------
    # CRUNCH
    # --------------------------------------------------------

    if text_contains(
        name,
        "crunch",
        "sit up",
        "sit-up",
        "heel toucher",
        "heel touchers",
    ):
        return result(
            "core_flexion",
            0.96,
            "N013_CORE_FLEXION_NAME",
            "Explicit trunk flexion exercise name.",
        )

    # --------------------------------------------------------
    # HIP RAISE
    # --------------------------------------------------------

    if text_contains(
        name,
        "hip raise",
        "leg raise",
        "knee raise",
        "butt ups",
        "butt-ups",
    ):
        return result(
            "core_flexion",
            0.92,
            "N014_CORE_HIP_RAISE",
            "Exercise primarily uses abdominal hip/pelvic flexion.",
        )

    # --------------------------------------------------------
    # PLYOMETRIC NAME
    # --------------------------------------------------------

    if text_contains(
        name,
        "box jump",
        "bench jump",
        "depth jump",
        "broad jump",
        "vertical jump",
        "jump squat",
        "bound",
        "bounds",
        "skip",
        "medicine ball throw",
        "med ball throw",
    ):
        return result(
            "plyometric",
            0.98,
            "N015_PLYOMETRIC_NAME",
            "Explicit explosive / jumping / throwing exercise name.",
        )

    # --------------------------------------------------------
    # CARDIO
    # --------------------------------------------------------

    if text_contains(
        name,
        "bicycling",
        "stationary bike",
        "air bike",
        "cycling",
        "treadmill",
        "running",
        "sprint",
        "jog",
        "rowing machine",
        "elliptical",
    ):
        return result(
            "cardio",
            0.95,
            "N016_CARDIO_NAME",
            "Explicit cardiovascular exercise name.",
        )

    # --------------------------------------------------------
    # MOBILITY / STRETCHING
    # --------------------------------------------------------

    if text_contains(
        name,
        "stretch",
        "circles",
        "90 90 hamstring",
        "adductor",
        "groin",
        "ankle",
        "mobility",
    ):
        return result(
            "mobility",
            0.90,
            "N017_MOBILITY_NAME",
            "Exercise name indicates mobility/stretching work.",
        )

    # --------------------------------------------------------
    # RECOVERY / SMR
    # --------------------------------------------------------

    if text_contains(
        name,
        "smr",
        "foam roll",
        "foam roller",
        "self myofascial",
    ):
        return result(
            "recovery",
            0.99,
            "N018_RECOVERY_NAME",
            "Explicit self-myofascial recovery exercise.",
        )

    # --------------------------------------------------------
    # BALANCE
    # --------------------------------------------------------

    if text_contains(
        name,
        "balance board",
        "bosu",
        "single leg balance",
    ):
        return result(
            "balance",
            0.98,
            "N019_BALANCE_NAME",
            "Explicit balance exercise.",
        )

    # --------------------------------------------------------
    # CARRY / DRAG
    # --------------------------------------------------------

    if text_contains(
        name,
        "farmer walk",
        "farmer carry",
        "suitcase carry",
        "waiter carry",
        "carry",
    ):
        return result(
            "carry",
            0.98,
            "N020_CARRY_NAME",
            "Explicit loaded carry exercise.",
        )

    return None


# ============================================================
# LEVEL 2
# SPECIAL CASES
# ============================================================

def classify_special_cases(
    exercise: dict[str, Any],
) -> dict[str, Any] | None:

    name = get_name(exercise)
    text = make_search_text(exercise)
    category = get_category(exercise)

    # --------------------------------------------------------
    # AROUND THE WORLD
    # --------------------------------------------------------

    if text_contains(name, "around the worlds"):
        return result(
            "horizontal_push",
            0.82,
            "S001_AROUND_THE_WORLD",
            "Chest-focused fly/circular pressing pattern.",
        )

    # --------------------------------------------------------
    # PULLOVER
    # --------------------------------------------------------

    if text_contains(name, "pullover"):
        if muscle_contains(exercise, "lats"):
            return result(
                "vertical_pull",
                0.88,
                "S002_PULLOVER_LATS",
                "Pullover primarily targets lats; classified as vertical pulling.",
            )

        if muscle_contains(exercise, "chest"):
            return result(
                "horizontal_push",
                0.70,
                "S003_PULLOVER_CHEST",
                "Pullover has chest involvement but lacks a clean canonical pattern.",
            )

    # --------------------------------------------------------
    # WINDMILL
    # --------------------------------------------------------

    if text_contains(name, "windmill"):
        return result(
            "anti_flexion",
            0.88,
            "S004_WINDMILL",
            "Windmill requires trunk stabilization against flexion.",
        )

    # --------------------------------------------------------
    # BENT PRESS
    # --------------------------------------------------------

    if text_contains(name, "bent press"):
        return result(
            "anti_flexion",
            0.84,
            "S005_BENT_PRESS",
            "Bent press combines pressing with substantial lateral trunk stabilization.",
        )

    # --------------------------------------------------------
    # ALTERNATING DELTOID RAISE
    # --------------------------------------------------------

    if text_contains(name, "alternating deltoid raise"):
        return result(
            "shoulder_abduction",
            0.97,
            "S006_DELTOID_RAISE",
            "Exercise explicitly raises arms forward/laterally.",
        )

    # --------------------------------------------------------
    # REAR DELT RAISES
    # --------------------------------------------------------

    if text_contains(
        name,
        "rear delt raise",
        "rear deltoid raise",
        "rear delt fly",
    ):
        return result(
            "horizontal_pull",
            0.84,
            "S007_REAR_DELT_RAISE",
            "Rear-delt fly/raise is treated as a horizontal pulling pattern.",
        )

    # --------------------------------------------------------
    # BAND PULL APART
    # --------------------------------------------------------

    if text_contains(name, "band pull apart"):
        return result(
            "horizontal_pull",
            0.94,
            "S008_BAND_PULL_APART",
            "Band pull-apart is a horizontal pulling/retraction pattern.",
        )

    # --------------------------------------------------------
    # BODY-UP
    # --------------------------------------------------------

    if text_contains(name, "body up"):
        return result(
            "elbow_extension",
            0.94,
            "S009_BODY_UP",
            "Body-Up is primarily an elbow-extension movement targeting the triceps.",
        )

    # --------------------------------------------------------
    # BODY TRICEP PRESS
    # --------------------------------------------------------

    if text_contains(name, "body tricep press"):
        return result(
            "elbow_extension",
            0.94,
            "S010_BODY_TRICEP_PRESS",
            "Primary movement is elbow extension.",
        )

    # --------------------------------------------------------
    # BARBELL INCLINE SHOULDER RAISE
    # --------------------------------------------------------

    if text_contains(name, "barbell incline shoulder raise"):
        return result(
            "shoulder_elevation",
            0.97,
            "S011_SHOULDER_PROTRACTION",
            "Instructions describe scapular protraction/elevation, not overhead pressing.",
        )

    # --------------------------------------------------------
    # BATTLE ROPES
    # --------------------------------------------------------

    if text_contains(name, "battling ropes"):
        return result(
            "conditioning",
            0.98,
            "S012_BATTLING_ROPES",
            "Battle ropes are conditioning work rather than vertical pressing.",
        )

    # --------------------------------------------------------
    # BEAR CRAWL SLED DRAGS
    # --------------------------------------------------------

    if text_contains(name, "bear crawl sled"):
        return result(
            "conditioning",
            0.98,
            "S013_BEAR_CRAWL_SLED",
            "Combined sled dragging/crawling is conditioning.",
        )

    # --------------------------------------------------------
    # BACKWARD DRAG
    # --------------------------------------------------------

    if text_contains(name, "backward drag"):
        return result(
            "conditioning",
            0.92,
            "S014_BACKWARD_DRAG",
            "Loaded backward dragging is conditioning/locomotion.",
        )

    # --------------------------------------------------------
    # ATLAS STONES
    # --------------------------------------------------------

    if text_contains(
        name,
        "atlas stone",
        "atlas stones",
    ):
        return result(
            "hinge",
            0.86,
            "S015_ATLAS_STONE",
            "Atlas stone lifting is dominated by hip hinge and extension.",
        )

    # --------------------------------------------------------
    # MEDICINE BALL THROW
    # --------------------------------------------------------

    if text_contains(name, "medicine ball throw"):
        return result(
            "plyometric",
            0.98,
            "S016_MEDICINE_BALL_THROW",
            "Explosive medicine-ball throw is plyometric/power work.",
        )

    # --------------------------------------------------------
    # BOX SKIP
    # --------------------------------------------------------

    if text_contains(name, "box skip"):
        return result(
            "plyometric",
            0.98,
            "S017_BOX_SKIP",
            "Explosive skip/jump movement.",
        )

    # --------------------------------------------------------
    # BENCH SPRINT
    # --------------------------------------------------------

    if text_contains(name, "bench sprint"):
        return result(
            "plyometric",
            0.94,
            "S018_BENCH_SPRINT",
            "Alternating explosive step/jump movement.",
        )

    # --------------------------------------------------------
    # BOTTOMS-UP CLEAN
    # --------------------------------------------------------

    if text_contains(name, "bottoms up clean"):
        return result(
            "hinge",
            0.86,
            "S019_BOTTOMS_UP_CLEAN",
            "Clean from hang is driven by hip extension.",
        )

    # --------------------------------------------------------
    # BOTTOMS UP
    # --------------------------------------------------------

    if name == "bottoms up":
        return result(
            "anti_extension",
            0.76,
            "S020_BOTTOMS_UP",
            "Ambiguous name; dataset muscle/instruction context suggests trunk-focused movement.",
        )

    # --------------------------------------------------------
    # AIR BIKE
    #
    # IMPORTANT:
    # The dataset's "Air Bike" is actually a bicycle-crunch
    # exercise, despite the misleading name.
    # --------------------------------------------------------

    if name == "air bike":
        if muscle_contains(exercise, "abdominals"):
            return result(
                "core_flexion",
                0.97,
                "S021_AIR_BIKE_DATASET",
                "Dataset instructions describe a bicycle-crunch movement.",
            )

        return result(
            "cardio",
            0.90,
            "S022_AIR_BIKE_CARDIO",
            "Air bike interpreted as cardio when abdominal-crunch evidence is absent.",
        )

    # --------------------------------------------------------
    # ANKLE CIRCLES
    # --------------------------------------------------------

    if text_contains(name, "ankle circles"):
        return result(
            "mobility",
            0.99,
            "S023_ANKLE_CIRCLES",
            "Joint mobility exercise.",
        )

    # --------------------------------------------------------
    # ARM CIRCLES
    # --------------------------------------------------------

    if text_contains(name, "arm circles"):
        return result(
            "mobility",
            0.99,
            "S024_ARM_CIRCLES",
            "Shoulder mobility exercise.",
        )

    # --------------------------------------------------------
    # BALANCE BOARD
    # --------------------------------------------------------

    if text_contains(name, "balance board"):
        return result(
            "balance",
            0.99,
            "S025_BALANCE_BOARD",
            "Explicit balance exercise.",
        )

    # --------------------------------------------------------
    # ADductor
    # --------------------------------------------------------

    if text_contains(name, "adductor", "groin"):
        if category == "stretching":
            return result(
                "mobility",
                0.98,
                "S026_ADDUCTOR_MOBILITY",
                "Adductor/groin exercise is categorized as mobility/stretching.",
            )

    # --------------------------------------------------------
    # SMR
    # --------------------------------------------------------

    if text_contains(name, "smr"):
        return result(
            "recovery",
            0.99,
            "S027_SMR",
            "Self-myofascial release.",
        )

    return None


# ============================================================
# LEVEL 3
# CATEGORY RULES
# ============================================================

def classify_category(
    exercise: dict[str, Any],
) -> dict[str, Any] | None:

    category = get_category(exercise)

    if category == "cardio":
        return result(
            "cardio",
            0.98,
            "C001_CARDIO_CATEGORY",
            "Dataset category is cardio.",
        )

    if category == "stretching":
        name = get_name(exercise)

        if text_contains(
            name,
            "smr",
            "foam roll",
            "foam roller",
        ):
            return result(
                "recovery",
                0.98,
                "C002_STRETCHING_RECOVERY",
                "Stretching-category exercise is explicitly recovery/SMR.",
            )

        return result(
            "stretching",
            0.94,
            "C003_STRETCHING_CATEGORY",
            "Dataset category is stretching.",
        )

    if category == "plyometrics":
        return result(
            "plyometric",
            0.98,
            "C004_PLYOMETRIC_CATEGORY",
            "Dataset category is plyometrics.",
        )

    if category == "strongman":
        # Strongman is NOT itself a movement pattern.
        # Try to infer the movement from name/muscles/instructions.
        return None

    if category == "powerlifting":
        # Powerlifting is NOT itself a movement pattern.
        # Specific movement should be inferred below.
        return None

    if category == "strength":
        return None

    return None


# ============================================================
# LEVEL 4
# INSTRUCTION-BASED RULES
# ============================================================

def classify_instructions(
    exercise: dict[str, Any],
) -> dict[str, Any] | None:

    instructions = get_instructions(exercise)

    if not instructions:
        return None

    # --------------------------------------------------------
    # SQUAT
    # --------------------------------------------------------

    if (
        (
            "bend the knees" in instructions
            and "lower your body" in instructions
            and "straighten the legs" in instructions
        )
        or (
            "squat" in instructions
            and "bend" in instructions
            and "knees" in instructions
        )
    ):
        return result(
            "squat",
            0.88,
            "I001_SQUAT_INSTRUCTIONS",
            "Instructions describe repeated knee/hip flexion followed by extension.",
        )

    # --------------------------------------------------------
    # HIP HINGE
    # --------------------------------------------------------

    hinge_signals = [
        "extend your hips",
        "extending your hips",
        "drive through the hips",
        "driving through the hips",
        "bend at the waist",
        "bending at the waist",
        "hips back",
        "drive through with your heels",
        "hip extension",
    ]

    hinge_hits = sum(
        1 for signal in hinge_signals
        if signal in instructions
    )

    if hinge_hits >= 2:
        return result(
            "hinge",
            0.91,
            "I002_HINGE_INSTRUCTIONS",
            "Instructions contain multiple hip-hinge/hip-extension signals.",
        )

    # --------------------------------------------------------
    # HORIZONTAL PULL
    # --------------------------------------------------------

    if (
        (
            "pull the bar" in instructions
            or "pull the dumbbells" in instructions
            or "pull the weight" in instructions
            or "pull the handle" in instructions
        )
        and (
            "chest" in instructions
            or "upper chest" in instructions
            or "torso" in instructions
        )
    ):
        return result(
            "horizontal_pull",
            0.87,
            "I003_HORIZONTAL_PULL_INSTRUCTIONS",
            "Instructions describe pulling resistance toward the torso/chest.",
        )

    # --------------------------------------------------------
    # VERTICAL PULL
    # --------------------------------------------------------

    if (
        (
            "pull yourself up" in instructions
            or "pull the bar down" in instructions
            or "pull the handle down" in instructions
            or "bring the bar down" in instructions
        )
        and (
            "overhead" in instructions
            or "above" in instructions
            or "chin" in instructions
        )
    ):
        return result(
            "vertical_pull",
            0.86,
            "I004_VERTICAL_PULL_INSTRUCTIONS",
            "Instructions describe vertical pulling.",
        )

    # --------------------------------------------------------
    # VERTICAL PUSH
    # --------------------------------------------------------

    if (
        (
            "press" in instructions
            or "extend through the elbow" in instructions
            or "press the weight" in instructions
        )
        and (
            "overhead" in instructions
            or "above your head" in instructions
            or "over your head" in instructions
        )
    ):
        return result(
            "vertical_push",
            0.89,
            "I005_VERTICAL_PUSH_INSTRUCTIONS",
            "Instructions describe pressing overhead.",
        )

    # --------------------------------------------------------
    # HORIZONTAL PUSH
    # --------------------------------------------------------

    if (
        (
            "press the bar" in instructions
            or "press the weight" in instructions
            or "push the weight" in instructions
            or "push the bar" in instructions
        )
        and (
            "chest" in instructions
            or "bench" in instructions
        )
    ):
        return result(
            "horizontal_push",
            0.86,
            "I006_HORIZONTAL_PUSH_INSTRUCTIONS",
            "Instructions describe pressing from a bench/chest position.",
        )

    # --------------------------------------------------------
    # ELBOW FLEXION
    # --------------------------------------------------------

    if (
        "curl" in instructions
        and (
            "elbow" in instructions
            or "forearm" in instructions
        )
    ):
        return result(
            "elbow_flexion",
            0.90,
            "I007_ELBOW_FLEXION_INSTRUCTIONS",
            "Instructions describe elbow flexion/curling.",
        )

    # --------------------------------------------------------
    # ELBOW EXTENSION
    # --------------------------------------------------------

    if (
        "extend through the elbow" in instructions
        or "extending the elbow" in instructions
        or "straighten your arm" in instructions
    ):
        return result(
            "elbow_extension",
            0.82,
            "I008_ELBOW_EXTENSION_INSTRUCTIONS",
            "Instructions describe elbow extension.",
        )

    # --------------------------------------------------------
    # SHOULDER ELEVATION
    # --------------------------------------------------------

    if (
        "raise your shoulders" in instructions
        or "raise the shoulders" in instructions
        or "shrug" in instructions
    ):
        return result(
            "shoulder_elevation",
            0.96,
            "I009_SHOULDER_ELEVATION",
            "Instructions explicitly describe shoulder elevation.",
        )

    # --------------------------------------------------------
    # LATERAL FLEXION
    # --------------------------------------------------------

    if (
        "bend only at the waist" in instructions
        and (
            "to the right" in instructions
            or "to the left" in instructions
            or "to the side" in instructions
        )
    ):
        return result(
            "lateral_flexion",
            0.97,
            "I010_LATERAL_FLEXION",
            "Instructions explicitly describe lateral trunk flexion.",
        )

    # --------------------------------------------------------
    # ANTI EXTENSION
    # --------------------------------------------------------

    if (
        "keep your abs tight" in instructions
        and (
            "pushup position" in instructions
            or "push up position" in instructions
        )
    ):
        return result(
            "anti_extension",
            0.78,
            "I011_ANTI_EXTENSION",
            "Trunk stabilization in an extended-body position.",
        )

    # --------------------------------------------------------
    # MOBILITY
    # --------------------------------------------------------

    if (
        "stretch" in instructions
        or "range of motion" in instructions
        or "mobility" in instructions
    ):
        return result(
            "mobility",
            0.78,
            "I012_MOBILITY_INSTRUCTIONS",
            "Instructions emphasize stretching/range of motion.",
        )

    # --------------------------------------------------------
    # CONDITIONING
    # --------------------------------------------------------

    if (
        "sled" in instructions
        and (
            "drag" in instructions
            or "pull" in instructions
        )
    ):
        return result(
            "conditioning",
            0.90,
            "I013_SLED_CONDITIONING",
            "Instructions describe loaded sled conditioning.",
        )

    return None


# ============================================================
# LEVEL 5
# MUSCLE-BASED RULES
# ============================================================

def classify_muscles(
    exercise: dict[str, Any],
) -> dict[str, Any] | None:

    name = get_name(exercise)

    primary = get_primary_muscles(exercise)
    secondary = get_secondary_muscles(exercise)

    muscles = primary | secondary

    # --------------------------------------------------------
    # TRAPS -> SHRUG / SHOULDER ELEVATION
    # --------------------------------------------------------

    if (
        "traps" in muscles
        and text_contains(name, "shrug")
    ):
        return result(
            "shoulder_elevation",
            0.97,
            "M001_TRAPS_SHRUG",
            "Trap-focused shrug.",
        )

    # --------------------------------------------------------
    # BICEPS + CURL
    # --------------------------------------------------------

    if (
        "biceps" in primary
        and text_contains(
            name,
            "curl",
        )
    ):
        return result(
            "elbow_flexion",
            0.96,
            "M002_BICEPS_CURL",
            "Biceps-primary curl movement.",
        )

    # --------------------------------------------------------
    # TRICEPS
    # --------------------------------------------------------

    if (
        "triceps" in primary
        and text_contains(
            name,
            "extension",
            "skull crusher",
            "pushdown",
            "pressdown",
        )
    ):
        return result(
            "elbow_extension",
            0.96,
            "M003_TRICEPS_EXTENSION",
            "Triceps-primary elbow extension.",
        )

    # --------------------------------------------------------
    # ADDUCTORS
    # --------------------------------------------------------

    if "adductors" in primary:
        if text_contains(
            name,
            "adductor",
            "groin",
        ):
            return result(
                "mobility",
                0.90,
                "M004_ADDUCTOR_MOBILITY",
                "Adductor/groin mobility exercise.",
            )

    # --------------------------------------------------------
    # SHOULDERS
    # --------------------------------------------------------

    if "shoulders" in primary:
        if text_contains(
            name,
            "raise",
            "lateral raise",
            "front raise",
            "deltoid",
        ):
            return result(
                "shoulder_abduction",
                0.88,
                "M005_SHOULDER_RAISE",
                "Shoulder isolation raise.",
            )

    # --------------------------------------------------------
    # ABDOMINALS
    # --------------------------------------------------------

    if "abdominals" in primary:
        if text_contains(
            name,
            "crunch",
            "sit up",
            "heel toucher",
            "heel touchers",
        ):
            return result(
                "core_flexion",
                0.94,
                "M006_ABDOMINAL_FLEXION",
                "Abdominal-primary flexion movement.",
            )

        if text_contains(
            name,
            "rollout",
            "ab roller",
        ):
            return result(
                "anti_extension",
                0.97,
                "M007_ABDOMINAL_ROLLOUT",
                "Abdominal-primary rollout.",
            )

    return None


# ============================================================
# LEVEL 6
# GENERAL FALLBACK
# ============================================================

def classify_fallback(
    exercise: dict[str, Any],
) -> dict[str, Any]:

    category = get_category(exercise)
    name = get_name(exercise)
    force = get_force(exercise)
    mechanic = get_mechanic(exercise)

    # --------------------------------------------------------
    # STRETCHING
    # --------------------------------------------------------

    if category == "stretching":
        return result(
            "stretching",
            0.75,
            "F001_STRETCHING",
            "Fallback for stretching-category exercise.",
        )

    # --------------------------------------------------------
    # PLYOMETRICS
    # --------------------------------------------------------

    if category == "plyometrics":
        return result(
            "plyometric",
            0.80,
            "F002_PLYOMETRIC",
            "Fallback for plyometric-category exercise.",
        )

    # --------------------------------------------------------
    # CARDIO
    # --------------------------------------------------------

    if category == "cardio":
        return result(
            "cardio",
            0.80,
            "F003_CARDIO",
            "Fallback for cardio-category exercise.",
        )

    # --------------------------------------------------------
    # STRONGMAN
    # --------------------------------------------------------

    if category == "strongman":
        return result(
            "conditioning",
            0.55,
            "F004_STRONGMAN_CONDITIONING",
            "Generic strongman fallback.",
        )

    # --------------------------------------------------------
    # DO NOT USE FORCE ALONE TO INFER PUSH/PULL
    #
    # This is intentionally conservative.
    # --------------------------------------------------------

    if category in {
        "strength",
        "powerlifting",
    }:
        if mechanic == "isolation":
            return result(
                "unknown",
                0.25,
                "F005_ISOLATION_UNKNOWN",
                "Isolation exercise without enough evidence for a specific movement pattern.",
            )

        if mechanic == "compound":
            return result(
                "unknown",
                0.30,
                "F006_COMPOUND_UNKNOWN",
                "Compound exercise without enough evidence for a specific movement pattern.",
            )

    return result(
        "unknown",
        0.0,
        "U01_UNKNOWN",
        "No reliable movement-pattern evidence found.",
    )


# ============================================================
# MAIN CLASSIFIER
# ============================================================

def classify_exercise(
    exercise: dict[str, Any],
) -> dict[str, Any]:

    classifiers = [
        classify_explicit_name,
        classify_special_cases,
        classify_category,
        classify_instructions,
        classify_muscles,
    ]

    for classifier in classifiers:
        classification = classifier(exercise)

        if classification is not None:
            return classification

    return classify_fallback(exercise)


# ============================================================
# QUALITY
# ============================================================

def confidence_bucket(confidence: float) -> str:

    if confidence >= 0.85:
        return "high"

    if confidence >= 0.70:
        return "medium"

    return "low"


def needs_review(
    classification: dict[str, Any],
) -> bool:

    pattern = classification["movement_pattern"]
    confidence = classification["confidence"]

    if pattern == "unknown":
        return True

    return confidence < 0.80


# ============================================================
# VALIDATION
# ============================================================

def validate_classification(
    exercise: dict[str, Any],
    classification: dict[str, Any],
) -> list[str]:

    warnings: list[str] = []

    name = get_name(exercise)
    pattern = classification["movement_pattern"]

    # --------------------------------------------------------
    # Obviously bad mappings
    # --------------------------------------------------------

    if (
        "shrug" in name
        and pattern != "shoulder_elevation"
    ):
        warnings.append(
            f"{exercise.get('name')} -> shrug should be shoulder_elevation"
        )

    if (
        "curl" in name
        and pattern != "elbow_flexion"
    ):
        warnings.append(
            f"{exercise.get('name')} -> curl should be elbow_flexion"
        )

    if (
        "skull crusher" in name
        and pattern != "elbow_extension"
    ):
        warnings.append(
            f"{exercise.get('name')} -> skull crusher should be elbow_extension"
        )

    if (
        "hip thrust" in name
        and pattern != "hinge"
    ):
        warnings.append(
            f"{exercise.get('name')} -> hip thrust should be hinge"
        )

    if (
        "glute bridge" in name
        and pattern != "hinge"
    ):
        warnings.append(
            f"{exercise.get('name')} -> glute bridge should be hinge"
        )

    if (
        "deadlift" in name
        and pattern != "hinge"
    ):
        warnings.append(
            f"{exercise.get('name')} -> deadlift should be hinge"
        )

    if (
        "side bend" in name
        and pattern != "lateral_flexion"
    ):
        warnings.append(
            f"{exercise.get('name')} -> side bend should be lateral_flexion"
        )

    if (
        "ab rollout" in name
        and pattern != "anti_extension"
    ):
        warnings.append(
            f"{exercise.get('name')} -> rollout should be anti_extension"
        )

    if (
        "box jump" in name
        and pattern != "plyometric"
    ):
        warnings.append(
            f"{exercise.get('name')} -> box jump should be plyometric"
        )

    if (
            "calf raise" in name
            and pattern != "plantar_flexion"
    ):
        warnings.append(
            f"{exercise.get('name')} -> calf raise should be plantar_flexion"
        )

    if (
            "bodyweight squat" in name
            and pattern != "squat"
    ):
        warnings.append(
            f"{exercise.get('name')} -> bodyweight squat should be squat"
        )

    if (
            "bodyweight fly" in name
            and pattern != "horizontal_push"
    ):
        warnings.append(
            f"{exercise.get('name')} -> bodyweight fly should be horizontal_push"
        )

    if (
            "side lateral" in name
            and pattern != "shoulder_abduction"
    ):
        warnings.append(
            f"{exercise.get('name')} -> side lateral should be shoulder_abduction"
        )

    if (
            "hip adductions" in name
            and pattern != "hip_abduction"
    ):
        warnings.append(
            f"{exercise.get('name')} -> dataset movement is hip_abduction"
        )

    if (
            "hang clean" in name
            and pattern != "hinge"
    ):
        warnings.append(
            f"{exercise.get('name')} -> hang clean should be hinge"
        )

    if (
            "butterfly" in name
            and pattern != "horizontal_push"
    ):
        warnings.append(
            f"{exercise.get('name')} -> butterfly should be horizontal_push"
        )

    return warnings

def validate_exercise_type(
    exercise: dict[str, Any],
    exercise_type: str,
    movement_pattern: str,
) -> list[str]:

    warnings: list[str] = []

    name = get_name(exercise)
    category = get_category(exercise)
    mechanic = get_mechanic(exercise)

    # --------------------------------------------------------
    # CORE
    # --------------------------------------------------------

    if movement_pattern in {
        "anti_extension",
        "anti_flexion",
        "anti_rotation",
        "lateral_flexion",
        "core_flexion",
    }:
        if exercise_type != "core":
            warnings.append(
                f"{exercise.get('name')} -> "
                f"{movement_pattern} should normally be exercise_type=core"
            )

    # --------------------------------------------------------
    # CARDIO
    # --------------------------------------------------------

    if category == "cardio":
        if exercise_type != "cardio":
            warnings.append(
                f"{exercise.get('name')} -> "
                f"cardio category should be exercise_type=cardio"
            )

    # --------------------------------------------------------
    # PLYOMETRIC
    # --------------------------------------------------------

    if category == "plyometrics":
        if exercise_type != "plyometric":
            warnings.append(
                f"{exercise.get('name')} -> "
                f"plyometrics category should be exercise_type=plyometric"
            )

    # --------------------------------------------------------
    # STRETCHING
    # --------------------------------------------------------

    if category == "stretching":
        if text_contains(
            name,
            "smr",
            "foam roll",
            "foam roller",
            "self myofascial",
        ):
            if exercise_type != "recovery":
                warnings.append(
                    f"{exercise.get('name')} -> "
                    f"SMR should be exercise_type=recovery"
                )
        elif exercise_type not in {
            "stretching",
            "recovery",
            "mobility",
        }:
            warnings.append(
                f"{exercise.get('name')} -> "
                f"stretching category has suspicious exercise_type="
                f"{exercise_type}"
            )

    # --------------------------------------------------------
    # MECHANIC
    # --------------------------------------------------------

    if (
        mechanic == "compound"
        and exercise_type == "isolation"
    ):
        warnings.append(
            f"{exercise.get('name')} -> "
            f"mechanic=compound but exercise_type=isolation"
        )

    if (
        mechanic == "isolation"
        and exercise_type == "compound"
    ):
        warnings.append(
            f"{exercise.get('name')} -> "
            f"mechanic=isolation but exercise_type=compound"
        )

    return warnings
# ============================================================
# PRINTING
# ============================================================

def print_header(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_distribution(
    title: str,
    counter: Counter,
    total: int,
) -> None:

    print_header(title)

    for key, count in counter.most_common():

        percentage = (
            (count / total) * 100
            if total
            else 0
        )

        print(
            f"{key:<30}"
            f"{count:>5} "
            f"({percentage:>6.2f}%)"
        )


# ============================================================
# ANALYSIS
# ============================================================

def analyze(
    exercises: list[dict[str, Any]],
) -> list[dict[str, Any]]:

    classified: list[dict[str, Any]] = []
    exercise_type_warnings: list[str] = []

    category_distribution = Counter()
    exercise_type_distribution = Counter()
    movement_distribution = Counter()
    rule_distribution = Counter()

    quality_distribution = Counter()

    type_pattern_distribution = Counter()

    unknown_exercises: list[dict[str, Any]] = []
    review_exercises: list[dict[str, Any]] = []
    low_confidence_exercises: list[dict[str, Any]] = []

    validation_warnings: list[str] = []

    for exercise in exercises:

        classification = classify_exercise(exercise)

        exercise_type = classify_exercise_type(
            exercise,
            classification,
        )
        type_warnings = validate_exercise_type(
            exercise,
            exercise_type,
            classification["movement_pattern"],
        )

        exercise_type_warnings.extend(
            type_warnings
        )

        enriched = dict(exercise)

        enriched["exercise_type"] = exercise_type

        enriched["movement_pattern"] = (
            classification["movement_pattern"]
        )

        enriched["confidence"] = (
            classification["confidence"]
        )

        enriched["rule_id"] = (
            classification["rule_id"]
        )

        enriched["classification_reason"] = (
            classification["reason"]
        )

        classified.append(enriched)

        category = (
                exercise.get("category")
                or "unknown"
        )

        pattern = classification["movement_pattern"]

        confidence = classification["confidence"]

        category_distribution[category] += 1
        exercise_type_distribution[exercise_type] += 1
        movement_distribution[pattern] += 1
        rule_distribution[
            classification["rule_id"]
        ] += 1

        quality_distribution[
            confidence_bucket(confidence)
        ] += 1

        type_pattern_distribution[
            (category, pattern)
        ] += 1

        if pattern == "unknown":
            unknown_exercises.append(enriched)

        if needs_review(classification):
            review_exercises.append(enriched)

        if confidence < 0.80:
            low_confidence_exercises.append(enriched)

        warnings = validate_classification(
            exercise,
            classification,
        )

        validation_warnings.extend(warnings)

    # --------------------------------------------------------
    # REPORT
    # --------------------------------------------------------

    total = len(exercises)

    classified_count = total - len(unknown_exercises)

    coverage = (
        classified_count / total * 100
        if total
        else 0
    )

    print_header(
        "WORKOUT EXERCISE DATASET ANALYSIS"
    )

    print(
        f"Dataset path : {DATASET_PATH}"
    )

    print(
        f"Total        : {total}"
    )

    print_distribution(
        "EXERCISE CATEGORY DISTRIBUTION",
        category_distribution,
        total,
    )
    print_distribution(
        "EXERCISE TYPE DISTRIBUTION",
        exercise_type_distribution,
        total,
    )

    print_distribution(
        "MOVEMENT PATTERN DISTRIBUTION",
        movement_distribution,
        total,
    )

    print_distribution(
        "RULE DISTRIBUTION",
        rule_distribution,
        total,
    )

    # --------------------------------------------------------
    # QUALITY
    # --------------------------------------------------------

    print_header("QUALITY")

    print(
        f"Total exercises       : {total}"
    )

    print(
        f"Classified            : {classified_count}"
    )

    print(
        f"Unknown               : {len(unknown_exercises)}"
    )

    print(
        f"Needs review          : {len(review_exercises)}"
    )

    print(
        f"High confidence       : "
        f"{quality_distribution['high']}"
    )

    print(
        f"Medium confidence     : "
        f"{quality_distribution['medium']}"
    )

    print(
        f"Low confidence        : "
        f"{quality_distribution['low']}"
    )

    print(
        f"Coverage              : "
        f"{coverage:.2f}%"
    )

    # --------------------------------------------------------
    # CATEGORY / PATTERN
    # --------------------------------------------------------

    print_header(
        "EXERCISE CATEGORY / MOVEMENT PATTERN"
    )

    for (category, pattern), count in sorted(
        type_pattern_distribution.items(),
        key=lambda item: (
            item[0][0],
            item[0][1],
        ),
    ):

        print(
            f"{category:<20}"
            f" -> "
            f"{pattern:<22}"
            f"{count:>5}"
        )

    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    print_header(
        "UNKNOWN MOVEMENT PATTERN"
    )

    if not unknown_exercises:

        print("None")

    else:

        for exercise in unknown_exercises:

            print(
                f"{exercise.get('name')} "
                f"| category={exercise.get('category')} "
                f"| confidence={exercise.get('confidence')} "
                f"| rule={exercise.get('rule_id')}"
            )

    # --------------------------------------------------------
    # REVIEW
    # --------------------------------------------------------

    print_header("NEEDS REVIEW")

    if not review_exercises:

        print("None")

    else:

        for exercise in review_exercises:

            print(
                f"{exercise.get('name')} "
                f"| pattern={exercise.get('movement_pattern')} "
                f"| confidence={exercise.get('confidence')} "
                f"| rule={exercise.get('rule_id')}"
            )

    # --------------------------------------------------------
    # LOW CONFIDENCE
    # --------------------------------------------------------

    print_header(
        "LOW CONFIDENCE (< 0.80)"
    )

    if not low_confidence_exercises:

        print("None")

    else:

        for exercise in low_confidence_exercises:

            print(
                f"{exercise.get('name')} "
                f"| pattern={exercise.get('movement_pattern')} "
                f"| confidence={exercise.get('confidence')} "
                f"| rule={exercise.get('rule_id')}"
            )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    print_header(
        "VALIDATION WARNINGS"
    )

    if not validation_warnings:

        print("No obvious mapping problems detected.")

    else:

        for warning in validation_warnings:

            print(
                f"WARNING: {warning}"
            )

    return classified


# ============================================================
# MAIN
# ============================================================

def load_dataset() -> list[dict[str, Any]]:

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"Exercise dataset not found:\n"
            f"{DATASET_PATH}"
        )

    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    if not isinstance(data, list):

        raise ValueError(
            "exercise.json must contain a JSON array."
        )

    return data


def save_dataset(
    exercises: list[dict[str, Any]],
) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            exercises,
            file,
            ensure_ascii=False,
            indent=2,
        )


def main() -> None:

    print()
    print("Loading exercise dataset...")

    exercises = load_dataset()

    print(
        f"Loaded {len(exercises)} exercises."
    )

    classified = analyze(exercises)

    save_dataset(classified)

    print_header("OUTPUT")

    print(
        "Classified dataset saved to:"
    )

    print(
        OUTPUT_PATH
    )

    print_header(
        "ANALYSIS COMPLETED"
    )


if __name__ == "__main__":
    main()