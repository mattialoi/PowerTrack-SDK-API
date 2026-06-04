from dataclasses import dataclass, field
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from client.models.session_log import SessionLog


@dataclass
class PlanExercise:
    id: int
    workout_day_id: int
    exercise_id: int
    exercise_order: int
    notes: Optional[str] = None
    _client: Optional[Any] = field(default=None, repr=False, compare=False, hash=False)

    @classmethod
    def from_dict(cls, data: dict, client: Optional[Any] = None) -> "PlanExercise":
        return cls(
            id=data["id"],
            workout_day_id=data["workout_day_id"],
            exercise_id=data["exercise_id"],
            exercise_order=data["exercise_order"],
            notes=data.get("notes"),
            _client=client
        )

    def get_logs(self) -> list["SessionLog"]:
        """Retrieve week-by-week logged session entries for this scheduled exercise."""
        if not self._client:
            raise RuntimeError("Client not bound to this model instance")
        return self._client.session_logs.get_by_exercise(self.id)

    def get_volume_progression(self) -> dict:
        """Get week-by-week volume progression data for this exercise."""
        if not self._client:
            raise RuntimeError("Client not bound to this model instance")
        return self._client.stats.get_volume_by_exercise(self.id)