from __future__ import annotations
from typing import Optional
from client.models import PlanExercise

class PlanExercisesAPI:
    """Sub-client for managing scheduled exercises in workout days."""

    def __init__(self, client):
        self.client = client

    def get_by_day(self, day_id: int) -> list[PlanExercise]:
        """Return all scheduled exercises for a workout day, ordered by exercise_order."""
        return [PlanExercise.from_dict(pe, self.client) for pe in self.client._get(f"/plan-exercises/day/{day_id}")]

    def get(self, plan_exercise_id: int) -> PlanExercise:
        """Retrieve a single scheduled exercise by ID."""
        return PlanExercise.from_dict(self.client._get(f"/plan-exercises/{plan_exercise_id}"), self.client)

    def create(self, workout_day_id: int, exercise_id: int,
               exercise_order: int, notes: Optional[str] = None) -> PlanExercise:
        """Schedule an exercise in a workout day."""
        data = {
            "workout_day_id": workout_day_id,
            "exercise_id": exercise_id,
            "exercise_order": exercise_order
        }
        if notes:
            data["notes"] = notes
        return PlanExercise.from_dict(self.client._post("/plan-exercises/", data), self.client)

    def update(self, plan_exercise_id: int,
               workout_day_id: Optional[int] = None,
               exercise_id: Optional[int] = None,
               exercise_order: Optional[int] = None,
               notes: Optional[str] = None) -> PlanExercise:
        """Update scheduling details for a plan exercise."""
        data = {}
        if workout_day_id is not None:
            data["workout_day_id"] = workout_day_id
        if exercise_id is not None:
            data["exercise_id"] = exercise_id
        if exercise_order is not None:
            data["exercise_order"] = exercise_order
        if notes is not None:
            data["notes"] = notes
        return PlanExercise.from_dict(self.client._put(f"/plan-exercises/{plan_exercise_id}", data), self.client)

    def delete(self, plan_exercise_id: int) -> dict:
        """Remove a scheduled exercise from a workout day."""
        return self.client._delete(f"/plan-exercises/{plan_exercise_id}")