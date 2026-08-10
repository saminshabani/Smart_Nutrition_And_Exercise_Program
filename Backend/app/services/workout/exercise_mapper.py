from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .exercise_type import ExerciseType
from .movement_pattern import MovementPattern


@dataclass
class ExerciseClassification:
    exercise_type: ExerciseType
    movement_pattern: MovementPattern | None
    confidence: float
    rule_id: str
    needs_review: bool


class ExerciseMapper:
    """
    Rule-based classifier for workout exercises.

    Classification is intentionally hierarchical:

        Exercise
            |
            +-- Mobility / Stretching
            +-- Recovery / SMR
            +-- Cardio
            +-- Plyometric
            +-- Balance
            +-- Conditioning
            +-- Core
            +-- Compound
            |      |
            |      +-- Movement Pattern
            |
            +-- Isolation
                   |
                   +-- No movement pattern required
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def classify(self, exercise: dict[str, Any]) -> ExerciseClassification:
        name = self._normalize(exercise.get("name", ""))
        force = self._normalize(exercise.get("force"))
        mechanic = self._normalize(exercise.get("mechanic"))

        primary_muscles = self._normalize_muscles(
            exercise.get("primary_muscles")
        )

        equipment = self._normalize(exercise.get("equipment"))

        # --------------------------------------------------------------
        # 1. Recovery / SMR
        # --------------------------------------------------------------

        if self._is_recovery(name, equipment):
            return ExerciseClassification(
                exercise_type=ExerciseType.RECOVERY,
                movement_pattern=None,
                confidence=0.98,
                rule_id="T01_RECOVERY",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # 2. Mobility / Stretching
        # --------------------------------------------------------------

        if self._is_mobility_or_stretching(name, force):
            exercise_type = (
                ExerciseType.STRETCHING
                if self._looks_like_stretch(name)
                else ExerciseType.MOBILITY
            )

            return ExerciseClassification(
                exercise_type=exercise_type,
                movement_pattern=None,
                confidence=0.97,
                rule_id="T02_MOBILITY",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # 3. Cardio
        # --------------------------------------------------------------

        if self._is_cardio(name):
            return ExerciseClassification(
                exercise_type=ExerciseType.CARDIO,
                movement_pattern=None,
                confidence=0.98,
                rule_id="T03_CARDIO",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # 4. Plyometric
        # --------------------------------------------------------------

        if self._is_plyometric(name):
            return ExerciseClassification(
                exercise_type=ExerciseType.PLYOMETRIC,
                movement_pattern=None,
                confidence=0.96,
                rule_id="T04_PLYOMETRIC",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # 5. Balance
        # --------------------------------------------------------------

        if self._is_balance(name):
            return ExerciseClassification(
                exercise_type=ExerciseType.BALANCE,
                movement_pattern=None,
                confidence=0.96,
                rule_id="T05_BALANCE",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # 6. Conditioning
        # --------------------------------------------------------------

        if self._is_conditioning(name):
            return ExerciseClassification(
                exercise_type=ExerciseType.CONDITIONING,
                movement_pattern=None,
                confidence=0.93,
                rule_id="T06_CONDITIONING",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # 7. Core
        # --------------------------------------------------------------

        core_result = self._classify_core(
            name=name,
            primary_muscles=primary_muscles,
        )

        if core_result is not None:
            return core_result

        # --------------------------------------------------------------
        # 8. Explicit compound exercises
        # --------------------------------------------------------------

        if mechanic == "compound":
            movement_result = self._classify_compound(
                name=name,
                force=force,
                primary_muscles=primary_muscles,
            )

            if movement_result is not None:
                return movement_result

            return ExerciseClassification(
                exercise_type=ExerciseType.COMPOUND,
                movement_pattern=None,
                confidence=0.60,
                rule_id="C99_COMPOUND_UNKNOWN",
                needs_review=True,
            )

        # --------------------------------------------------------------
        # 9. Explicit isolation exercises
        # --------------------------------------------------------------

        if mechanic == "isolation":
            return ExerciseClassification(
                exercise_type=ExerciseType.ISOLATION,
                movement_pattern=None,
                confidence=0.97,
                rule_id="I01_ISOLATION",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # 10. Try compound inference from exercise name
        # --------------------------------------------------------------

        if self._looks_like_compound(name):
            movement_result = self._classify_compound(
                name=name,
                force=force,
                primary_muscles=primary_muscles,
            )

            if movement_result is not None:
                return movement_result

            return ExerciseClassification(
                exercise_type=ExerciseType.COMPOUND,
                movement_pattern=None,
                confidence=0.55,
                rule_id="C98_INFERRED_COMPOUND_UNKNOWN",
                needs_review=True,
            )

        # --------------------------------------------------------------
        # 11. Unknown
        # --------------------------------------------------------------

        return ExerciseClassification(
            exercise_type=ExerciseType.UNKNOWN,
            movement_pattern=None,
            confidence=0.0,
            rule_id="U01_UNKNOWN",
            needs_review=True,
        )

    # ==================================================================
    # TYPE CLASSIFICATION
    # ==================================================================

    def _is_recovery(
        self,
        name: str,
        equipment: str | None,
    ) -> bool:

        recovery_keywords = (
            "smr",
            "self myofascial",
            "foam roll",
            "foam roller",
            "massage",
            "release",
        )

        return any(keyword in name for keyword in recovery_keywords)

    # ------------------------------------------------------------------

    def _is_mobility_or_stretching(
        self,
        name: str,
        force: str | None,
    ) -> bool:

        keywords = (
            "stretch",
            "mobility",
            "flexibility",
            "circles",
            "joint rotation",
            "dynamic stretch",
        )

        if any(keyword in name for keyword in keywords):
            return True

        if force == "static":
            return True

        return False

    # ------------------------------------------------------------------

    def _looks_like_stretch(self, name: str) -> bool:

        keywords = (
            "stretch",
            "flexibility",
            "static",
        )

        return any(keyword in name for keyword in keywords)

    # ------------------------------------------------------------------

    def _is_cardio(self, name: str) -> bool:

        cardio_keywords = (
            "bicycling",
            "cycling",
            "stationary bike",
            "treadmill",
            "elliptical",
            "rowing machine",
            "stair",
            "stepmill",
            "jump rope",
            "jumping rope",
            "running",
            "jogging",
            "walking",
            "sprint",
            "air bike",
        )

        return any(keyword in name for keyword in cardio_keywords)

    # ------------------------------------------------------------------

    def _is_plyometric(self, name: str) -> bool:

        plyometric_keywords = (
            "box jump",
            "bench jump",
            "depth jump",
            "broad jump",
            "tuck jump",
            "jump squat",
            "jump lunge",
            "power skip",
            "bounding",
            "bound",
            "plyometric",
        )

        return any(keyword in name for keyword in plyometric_keywords)

    # ------------------------------------------------------------------

    def _is_balance(self, name: str) -> bool:

        balance_keywords = (
            "balance board",
            "bosu",
            "single leg balance",
            "stability ball",
            "stability",
        )

        return any(keyword in name for keyword in balance_keywords)

    # ------------------------------------------------------------------

    def _is_conditioning(self, name: str) -> bool:

        conditioning_keywords = (
            "battle rope",
            "battling rope",
            "sled drag",
            "sled push",
            "farmer walk",
            "farmer carry",
            "loaded carry",
        )

        return any(keyword in name for keyword in conditioning_keywords)

    # ==================================================================
    # CORE CLASSIFICATION
    # ==================================================================

    def _classify_core(
        self,
        name: str,
        primary_muscles: set[str],
    ) -> ExerciseClassification | None:

        core_keywords = (
            "crunch",
            "sit-up",
            "sit up",
            "ab roller",
            "ab wheel",
            "plank",
            "hollow body",
            "dead bug",
            "bird dog",
            "heel toucher",
            "heel touch",
            "leg raise",
            "knee raise",
            "hip raise",
            "russian twist",
            "wood chop",
            "woodchop",
            "side bend",
            "windmill",
        )

        core_muscles = {
            "abdominals",
            "abs",
            "obliques",
        }

        if not (
            any(keyword in name for keyword in core_keywords)
            or primary_muscles.intersection(core_muscles)
        ):
            return None

        # --------------------------------------------------------------
        # Anti-extension
        # --------------------------------------------------------------

        anti_extension_keywords = (
            "ab roller",
            "ab wheel",
            "rollout",
            "plank",
            "dead bug",
            "hollow body",
        )

        if any(keyword in name for keyword in anti_extension_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.CORE,
                movement_pattern=MovementPattern.ANTI_EXTENSION,
                confidence=0.96,
                rule_id="K01_ANTI_EXTENSION",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # Rotation
        # --------------------------------------------------------------

        rotation_keywords = (
            "russian twist",
            "wood chop",
            "woodchop",
            "rotational",
            "rotation",
        )

        if any(keyword in name for keyword in rotation_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.CORE,
                movement_pattern=MovementPattern.ROTATION,
                confidence=0.95,
                rule_id="K02_ROTATION",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # Anti-rotation
        # --------------------------------------------------------------

        anti_rotation_keywords = (
            "pallof",
            "anti rotation",
            "anti-rotation",
        )

        if any(keyword in name for keyword in anti_rotation_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.CORE,
                movement_pattern=MovementPattern.ANTI_ROTATION,
                confidence=0.97,
                rule_id="K03_ANTI_ROTATION",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # Lateral / anti-flexion
        # --------------------------------------------------------------

        if "side bend" in name:
            return ExerciseClassification(
                exercise_type=ExerciseType.CORE,
                movement_pattern=MovementPattern.ANTI_FLEXION,
                confidence=0.82,
                rule_id="K04_SIDE_BEND",
                needs_review=True,
            )

        # --------------------------------------------------------------
        # Generic core
        # --------------------------------------------------------------

        return ExerciseClassification(
            exercise_type=ExerciseType.CORE,
            movement_pattern=None,
            confidence=0.85,
            rule_id="K99_CORE_OTHER",
            needs_review=True,
        )

    # ==================================================================
    # COMPOUND MOVEMENT PATTERN
    # ==================================================================

    def _classify_compound(
        self,
        name: str,
        force: str | None,
        primary_muscles: set[str],
    ) -> ExerciseClassification | None:

        # --------------------------------------------------------------
        # SQUAT
        # --------------------------------------------------------------

        squat_keywords = (
            "squat",
            "front squat",
            "back squat",
            "goblet squat",
            "hack squat",
            "zercher squat",
            "overhead squat",
        )

        if any(keyword in name for keyword in squat_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.COMPOUND,
                movement_pattern=MovementPattern.SQUAT,
                confidence=0.98,
                rule_id="M01_SQUAT_NAME",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # HINGE
        # --------------------------------------------------------------

        hinge_keywords = (
            "deadlift",
            "romanian deadlift",
            "rdl",
            "stiff leg deadlift",
            "good morning",
            "hip thrust",
            "glute bridge",
            "kettlebell swing",
            "clean",
            "snatch",
        )

        if any(keyword in name for keyword in hinge_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.COMPOUND,
                movement_pattern=MovementPattern.HINGE,
                confidence=0.94,
                rule_id="M02_HINGE_NAME",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # UNILATERAL LEG
        # --------------------------------------------------------------

        unilateral_keywords = (
            "lunge",
            "split squat",
            "bulgarian",
            "step up",
            "step-up",
            "pistol squat",
            "single leg squat",
            "single-leg squat",
        )

        if any(keyword in name for keyword in unilateral_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.COMPOUND,
                movement_pattern=MovementPattern.UNILATERAL_LEG,
                confidence=0.96,
                rule_id="M03_UNILATERAL_LEG_NAME",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # HORIZONTAL PUSH
        # --------------------------------------------------------------

        horizontal_push_keywords = (
            "bench press",
            "floor press",
            "chest press",
            "push up",
            "push-up",
            "pushup",
            "dip",
            "chest fly",
            "chest flye",
            "flyes",
            "flyes",
        )

        if any(keyword in name for keyword in horizontal_push_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.COMPOUND,
                movement_pattern=MovementPattern.HORIZONTAL_PUSH,
                confidence=0.95,
                rule_id="M04_HORIZONTAL_PUSH_NAME",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # HORIZONTAL PULL
        # --------------------------------------------------------------

        horizontal_pull_keywords = (
            "barbell row",
            "dumbbell row",
            "cable row",
            "seated row",
            "machine row",
            "t-bar row",
            "t bar row",
            "chest supported row",
            "inverted row",
        )

        if any(keyword in name for keyword in horizontal_pull_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.COMPOUND,
                movement_pattern=MovementPattern.HORIZONTAL_PULL,
                confidence=0.96,
                rule_id="M05_HORIZONTAL_PULL_NAME",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # VERTICAL PUSH
        # --------------------------------------------------------------

        vertical_push_keywords = (
            "overhead press",
            "military press",
            "shoulder press",
            "arnold press",
            "push press",
            "jerk",
        )

        if any(keyword in name for keyword in vertical_push_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.COMPOUND,
                movement_pattern=MovementPattern.VERTICAL_PUSH,
                confidence=0.96,
                rule_id="M06_VERTICAL_PUSH_NAME",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # VERTICAL PULL
        # --------------------------------------------------------------

        vertical_pull_keywords = (
            "pull up",
            "pull-up",
            "pullup",
            "chin up",
            "chin-up",
            "chinup",
            "lat pulldown",
            "pulldown",
            "pull down",
            "pull-down",
        )

        if any(keyword in name for keyword in vertical_pull_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.COMPOUND,
                movement_pattern=MovementPattern.VERTICAL_PULL,
                confidence=0.97,
                rule_id="M07_VERTICAL_PULL_NAME",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # CARRY
        # --------------------------------------------------------------

        carry_keywords = (
            "farmer walk",
            "farmer's walk",
            "farmer carry",
            "suitcase carry",
            "suitcase walk",
            "waiter walk",
            "loaded carry",
            "carry",
        )

        if any(keyword in name for keyword in carry_keywords):
            return ExerciseClassification(
                exercise_type=ExerciseType.COMPOUND,
                movement_pattern=MovementPattern.CARRY,
                confidence=0.96,
                rule_id="M08_CARRY_NAME",
                needs_review=False,
            )

        # --------------------------------------------------------------
        # Avoid weak muscle-based inference
        # --------------------------------------------------------------

        # We intentionally do NOT do:
        #
        #     chest -> horizontal_push
        #     lats  -> vertical_pull
        #     shoulders -> vertical_push
        #
        # because the dataset contains many exercises where this would
        # produce incorrect classifications.

        return None

    # ==================================================================
    # NAME HELPERS
    # ==================================================================

    def _looks_like_compound(self, name: str) -> bool:

        compound_keywords = (
            "press",
            "row",
            "squat",
            "deadlift",
            "lunge",
            "pull up",
            "pull-up",
            "pullup",
            "chin up",
            "chin-up",
            "chinup",
            "pulldown",
            "push up",
            "push-up",
            "pushup",
            "dip",
            "clean",
            "snatch",
            "jerk",
            "swing",
            "thrust",
            "carry",
            "walk",
        )

        return any(keyword in name for keyword in compound_keywords)

    # ==================================================================
    # NORMALIZATION
    # ==================================================================

    @staticmethod
    def _normalize(value: Any) -> str | None:

        if value is None:
            return None

        value = str(value).strip().lower()

        value = value.replace("_", " ")
        value = re.sub(r"\s+", " ", value)

        return value

    # ------------------------------------------------------------------

    def _normalize_muscles(
        self,
        muscles: Any,
    ) -> set[str]:

        if not muscles:
            return set()

        if isinstance(muscles, str):
            muscles = [muscles]

        return {
            self._normalize(muscle)
            for muscle in muscles
            if muscle
        }