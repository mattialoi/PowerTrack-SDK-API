from __future__ import annotations
from typing import Optional
from client.models import WorkoutDay

class WorkoutDaysAPI:
    """Sub-client for managing workout days."""

    def __init__(self, client):
        self.client = client

    def get_by_plan(self, plan_id: int) -> list[WorkoutDay]:
        """Return all workout days for a training plan, ordered by day_order."""
        return [WorkoutDay.from_dict(d, self.client) for d in self.client._get(f"/workout-days/plan/{plan_id}")]

    def get(self, day_id: int) -> WorkoutDay:
        """Return a single workout day by ID."""
        return WorkoutDay.from_dict(self.client._get(f"/workout-days/{day_id}"), self.client)

    def create(self, plan_id: int, name: str, day_order: int) -> WorkoutDay:
        """Create a new workout day inside a training plan."""
        return WorkoutDay.from_dict(self.client._post("/workout-days/", {
            "plan_id": plan_id,
            "name": name,
            "day_order": day_order
        }), self.client)

    def update(self, day_id: int, name: Optional[str] = None, day_order: Optional[int] = None) -> WorkoutDay:
        """Update an existing workout day."""
        data = {}
        if name is not None:
            data["name"] = name
        if day_order is not None:
            data["day_order"] = day_order
        return WorkoutDay.from_dict(self.client._put(f"/workout-days/{day_id}", data), self.client)

    def delete(self, day_id: int) -> dict:
        """Delete a workout day and all associated exercises."""
        return self.client._delete(f"/workout-days/{day_id}")