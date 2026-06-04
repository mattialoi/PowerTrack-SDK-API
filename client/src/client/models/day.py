from dataclasses import dataclass, field
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from client.models.plan_exercise import PlanExercise


@dataclass
class WorkoutDay:
    id: int
    plan_id: int
    name: str
    day_order: int
    _client: Optional[Any] = field(default=None, repr=False, compare=False, hash=False)

    @classmethod
    def from_dict(cls, data: dict, client: Optional[Any] = None) -> "WorkoutDay":
        return cls(
            id=data["id"],
            plan_id=data["plan_id"],
            name=data["name"],
            day_order=data["day_order"],
            _client=client
        )

    def get_exercises(self) -> list["PlanExercise"]:
        """Retrieve scheduled exercises for this day."""
        if not self._client:
            raise RuntimeError("Client not bound to this model instance")
        return self._client.plan_exercises.get_by_day(self.id)