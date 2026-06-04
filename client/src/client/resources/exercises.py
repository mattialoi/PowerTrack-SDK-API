from __future__ import annotations
from typing import Optional
from client.models import Exercise

class ExercisesAPI:
    """Sub-client for managing exercise catalog."""

    def __init__(self, client):
        self.client = client

    def list(self, target_muscle: Optional[str] = None, mechanics_type: Optional[str] = None) -> list[Exercise]:
        """Return all exercises from the catalog, with optional filters."""
        params = []
        if target_muscle:
            params.append(f"target_muscle={target_muscle}")
        if mechanics_type:
            params.append(f"mechanics_type={mechanics_type}")
        query = "?" + "&".join(params) if params else ""
        return [Exercise.from_dict(e, self.client) for e in self.client._get(f"/exercises/{query}")]

    def get(self, exercise_id: int) -> Exercise:
        """Return a single exercise by ID."""
        return Exercise.from_dict(self.client._get(f"/exercises/{exercise_id}"), self.client)

    def create(self, name: str, mechanics_type: str, target_muscle: str) -> Exercise:
        """Add a new exercise to the global catalog."""
        return Exercise.from_dict(self.client._post("/exercises/", {
            "name": name,
            "mechanics_type": mechanics_type,
            "target_muscle": target_muscle
        }), self.client)

    def delete(self, exercise_id: int) -> dict:
        """Delete an exercise from the catalog."""
        return self.client._delete(f"/exercises/{exercise_id}")