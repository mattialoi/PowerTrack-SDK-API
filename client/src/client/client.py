"""
PowerTrack Fitness Client Library
==================================
A Python client library for interacting with the PowerTrack REST API.

Usage:
    from client.client import PowerTrackClient

    client = PowerTrackClient("http://127.0.0.1:8000")
    user = client.users.create(username="marco")
    plan = client.plans.create(user.id, "Mesocycle 1", 6)
"""

from client.base import BaseClient, PowerTrackAPIError
from client.resources import (
    UsersAPI,
    PlansAPI,
    WorkoutDaysAPI,
    ExercisesAPI,
    PlanExercisesAPI,
    SessionLogsAPI,
    StatsAPI
)

__all__ = ["PowerTrackClient", "PowerTrackAPIError"]


class PowerTrackClient(BaseClient):
    """
    Client for the PowerTrack REST API structured with sub-clients.

    Args:
        base_url: Base URL of the PowerTrack backend (e.g. "http://127.0.0.1:8000")
        timeout: Request timeout in seconds (default: 10)
    """

    def __init__(self, base_url: str, timeout: int = 10):
        super().__init__(base_url, timeout)
        
        # Initialize specialized sub-clients (managers)
        self.users = UsersAPI(self)
        self.plans = PlansAPI(self)
        self.workout_days = WorkoutDaysAPI(self)
        self.exercises = ExercisesAPI(self)
        self.plan_exercises = PlanExercisesAPI(self)
        self.session_logs = SessionLogsAPI(self)
        self.stats = StatsAPI(self)