from dataclasses import dataclass
from typing import Optional, List


# --- 1. Exercise volume ---
@dataclass
class ExerciseVolumeData:
    week_number: int
    sets: int
    reps: int
    weight: float
    volume: float
    rpe: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ExerciseVolumeData":
        return cls(
            week_number=data["week_number"],
            sets=data["sets"],
            reps=data["reps"],
            weight=data["weight"],
            volume=data["volume"],
            rpe=data.get("rpe")
        )

@dataclass
class ExerciseVolumeReport:
    plan_exercise_id: int
    exercise: str
    data: List[ExerciseVolumeData]
    message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ExerciseVolumeReport":
        items = [ExerciseVolumeData.from_dict(item) for item in data.get("data", [])]
        return cls(
            plan_exercise_id=data["plan_exercise_id"],
            exercise=data["exercise"],
            data=items,
            message=data.get("message")
        )


# --- 2. volume tot and multy-joint ---
@dataclass
class WeeklyVolumeData:
    week_number: int
    total_volume: float

    @classmethod
    def from_dict(cls, data: dict) -> "WeeklyVolumeData":
        return cls(
            week_number=data["week_number"],
            total_volume=data["total_volume"]
        )

@dataclass
class WeeklyVolumeReport:
    plan_id: int
    data: List[WeeklyVolumeData]
    mechanics_type: Optional[str] = None
    message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "WeeklyVolumeReport":
        items = [WeeklyVolumeData.from_dict(item) for item in data.get("data", [])]
        return cls(
            plan_id=data["plan_id"],
            data=items,
            mechanics_type=data.get("mechanics_type"),
            message=data.get("message")
        )


# --- 3. avg RPE ---
@dataclass
class WeeklyRpeData:
    week_number: int
    avg_rpe: float
    sessions_logged: int

    @classmethod
    def from_dict(cls, data: dict) -> "WeeklyRpeData":
        return cls(
            week_number=data["week_number"],
            avg_rpe=data["avg_rpe"],
            sessions_logged=data["sessions_logged"]
        )

@dataclass
class WeeklyRpeReport:
    plan_id: int
    data: List[WeeklyRpeData]
    message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "WeeklyRpeReport":
        items = [WeeklyRpeData.from_dict(item) for item in data.get("data", [])]
        return cls(
            plan_id=data["plan_id"],
            data=items,
            message=data.get("message")
        )


# --- 4. pain report ---
@dataclass
class PainLog:
    week_number: int
    exercise: str
    rpe: Optional[int] = None
    user_feedback: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "PainLog":
        return cls(
            week_number=data["week_number"],
            exercise=data["exercise"],
            rpe=data.get("rpe"),
            user_feedback=data.get("user_feedback")
        )

@dataclass
class PainReport:
    plan_id: int
    total_pain_flags: int
    data: List[PainLog]
    message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "PainReport":
        items = [PainLog.from_dict(item) for item in data.get("data", [])]
        return cls(
            plan_id=data["plan_id"],
            total_pain_flags=data["total_pain_flags"],
            data=items,
            message=data.get("message")
        )


# --- 5. Muscle balance ---
@dataclass
class MuscleBalanceData:
    target_muscle: str
    total_volume: float
    percentage: float

    @classmethod
    def from_dict(cls, data: dict) -> "MuscleBalanceData":
        return cls(
            target_muscle=data["target_muscle"],
            total_volume=data["total_volume"],
            percentage=data["percentage"]
        )

@dataclass
class MuscleBalanceReport:
    plan_id: int
    total_volume: float
    data: List[MuscleBalanceData]
    message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "MuscleBalanceReport":
        items = [MuscleBalanceData.from_dict(item) for item in data.get("data", [])]
        return cls(
            plan_id=data["plan_id"],
            total_volume=data["total_volume"],
            data=items,
            message=data.get("message")
        )