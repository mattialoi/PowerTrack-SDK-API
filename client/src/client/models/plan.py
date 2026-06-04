from dataclasses import dataclass, field
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from client.models.day import WorkoutDay


@dataclass
class TrainingPlan:
    id: int
    user_id: int
    name: str
    total_weeks: int
    start_date: Optional[str] = None
    _client: Optional[Any] = field(default=None, repr=False, compare=False, hash=False)

    @classmethod
    def from_dict(cls, data: dict, client: Optional[Any] = None) -> "TrainingPlan":
        return cls(
            id=data["id"],
            user_id=data["user_id"],
            name=data["name"],
            total_weeks=data["total_weeks"],
            start_date=data.get("start_date"),
            _client=client
        )

    def get_days(self) -> list["WorkoutDay"]:
        """Retrieve all workout days scheduled in this plan."""
        if not self._client:
            raise RuntimeError("Client not bound to this model instance")
        return self._client.workout_days.get_by_plan(self.id)

    def get_total_volume(self) -> dict:
        """Get the week-by-week total volume report for this plan."""
        if not self._client:
            raise RuntimeError("Client not bound to this model instance")
        return self._client.stats.get_total_volume(self.id)

    def get_avg_rpe(self) -> dict:
        """Get the week-by-week average RPE report for this plan."""
        if not self._client:
            raise RuntimeError("Client not bound to this model instance")
        return self._client.stats.get_avg_rpe(self.id)

    def get_pain_report(self) -> dict:
        """Get the pain/discomfort incidents report for this plan."""
        if not self._client:
            raise RuntimeError("Client not bound to this model instance")
        return self._client.stats.get_pain_report(self.id)

    def get_muscle_balance(self) -> dict:
        """Get the muscle group volume distribution report for this plan."""
        if not self._client:
            raise RuntimeError("Client not bound to this model instance")
        return self._client.stats.get_muscle_balance(self.id)