from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class SessionLog:
    id: int
    plan_exercise_id: int
    week_number: int
    sets: int
    reps: int
    weight: float
    rpe: Optional[int] = None
    user_feedback: Optional[str] = None
    pain_discomfort: bool = False
    _client: Optional[Any] = field(default=None, repr=False, compare=False, hash=False)

    @classmethod
    def from_dict(cls, data: dict, client: Optional[Any] = None) -> "SessionLog":
        return cls(
            id=data["id"],
            plan_exercise_id=data["plan_exercise_id"],
            week_number=data["week_number"],
            sets=data["sets"],
            reps=data["reps"],
            weight=data["weight"],
            rpe=data.get("rpe"),
            user_feedback=data.get("user_feedback"),
            pain_discomfort=data.get("pain_discomfort", False),
            _client=client
        )