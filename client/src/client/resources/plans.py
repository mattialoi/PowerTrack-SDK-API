from __future__ import annotations
from typing import Optional
from client.models import TrainingPlan

class PlansAPI:
    """Sub-client for managing training plans."""

    def __init__(self, client):
        self.client = client

    def list(self) -> list[TrainingPlan]:
        """Return a list of all training plans."""
        return [TrainingPlan.from_dict(p, self.client) for p in self.client._get("/plans/")]

    def get(self, plan_id: int) -> TrainingPlan:
        """Return a single training plan by ID."""
        return TrainingPlan.from_dict(self.client._get(f"/plans/{plan_id}"), self.client)

    def get_by_user(self, user_id: int) -> list[TrainingPlan]:
        """Return all training plans for a specific user."""
        return [TrainingPlan.from_dict(p, self.client) for p in self.client._get(f"/plans/user/{user_id}")]

    def create(self, user_id: int, name: str, total_weeks: int) -> TrainingPlan:
        """Create a new training plan for a user."""
        return TrainingPlan.from_dict(self.client._post("/plans/", {
            "user_id": user_id,
            "name": name,
            "total_weeks": total_weeks
        }), self.client)

    def update(self, plan_id: int, name: Optional[str] = None, total_weeks: Optional[int] = None) -> TrainingPlan:
        """Update an existing training plan."""
        data = {}
        if name is not None:
            data["name"] = name
        if total_weeks is not None:
            data["total_weeks"] = total_weeks
        return TrainingPlan.from_dict(self.client._put(f"/plans/{plan_id}", data), self.client)

    def delete(self, plan_id: int) -> dict:
        """Delete a training plan and all associated data."""
        return self.client._delete(f"/plans/{plan_id}")