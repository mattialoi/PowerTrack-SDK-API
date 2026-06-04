from __future__ import annotations
from typing import Optional
from client.models import SessionLog

class SessionLogsAPI:
    """Sub-client for logging workout sessions."""

    def __init__(self, client):
        self.client = client

    def get_by_exercise(self, plan_exercise_id: int) -> list[SessionLog]:
        """Return all session logs for a scheduled exercise, ordered by week."""
        return [SessionLog.from_dict(l, self.client) for l in self.client._get(f"/session-logs/plan-exercise/{plan_exercise_id}")]

    def get(self, log_id: int) -> SessionLog:
        """Retrieve a single session log by ID."""
        return SessionLog.from_dict(self.client._get(f"/session-logs/{log_id}"), self.client)

    def create(self, plan_exercise_id: int, week_number: int, sets: int,
               reps: int, weight: float, rpe: Optional[int] = None,
               user_feedback: Optional[str] = None,
               pain_discomfort: bool = False) -> SessionLog:
        """Log a workout session for a specific exercise and week."""
        return SessionLog.from_dict(self.client._post("/session-logs/", {
            "plan_exercise_id": plan_exercise_id,
            "week_number": week_number,
            "sets": sets,
            "reps": reps,
            "weight": weight,
            "rpe": rpe,
            "user_feedback": user_feedback,
            "pain_discomfort": pain_discomfort
        }), self.client)

    def update(self, log_id: int, sets: Optional[int] = None, reps: Optional[int] = None,
               weight: Optional[float] = None, rpe: Optional[int] = None,
               user_feedback: Optional[str] = None,
               pain_discomfort: Optional[bool] = None) -> SessionLog:
        """Update an existing session log."""
        data = {}
        if sets is not None:
            data["sets"] = sets
        if reps is not None:
            data["reps"] = reps
        if weight is not None:
            data["weight"] = weight
        if rpe is not None:
            data["rpe"] = rpe
        if user_feedback is not None:
            data["user_feedback"] = user_feedback
        if pain_discomfort is not None:
            data["pain_discomfort"] = pain_discomfort
        return SessionLog.from_dict(self.client._put(f"/session-logs/{log_id}", data), self.client)

    def delete(self, log_id: int) -> dict:
        """Delete a session log."""
        return self.client._delete(f"/session-logs/{log_id}")