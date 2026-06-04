from __future__ import annotations
from client.models import (
    ExerciseVolumeReport,
    WeeklyVolumeReport,
    WeeklyRpeReport,
    PainReport,
    MuscleBalanceReport
)


class StatsAPI:
    """Sub-client for retrieving training statistics and records."""

    def __init__(self, client):
        self.client = client

    def get_volume_by_exercise(self, plan_exercise_id: int) -> ExerciseVolumeReport:
        """Return week-by-week volume progression for a specific exercise."""
        return ExerciseVolumeReport.from_dict(
            self.client._get(f"/stats/volume/exercise/{plan_exercise_id}")
        )

    def get_multijoint_volume(self, plan_id: int) -> WeeklyVolumeReport:
        """Return week-by-week total volume for multi-joint exercises only."""
        return WeeklyVolumeReport.from_dict(
            self.client._get(f"/stats/volume/multi-joint/{plan_id}")
        )

    def get_total_volume(self, plan_id: int) -> WeeklyVolumeReport:
        """Return week-by-week total volume across all exercises in a plan."""
        return WeeklyVolumeReport.from_dict(
            self.client._get(f"/stats/volume/total/{plan_id}")
        )

    def get_avg_rpe(self, plan_id: int) -> WeeklyRpeReport:
        """Return average RPE per week for a training plan."""
        return WeeklyRpeReport.from_dict(
            self.client._get(f"/stats/rpe/{plan_id}")
        )

    def get_pain_report(self, plan_id: int) -> PainReport:
        """Return a report of all pain/discomfort flags for a training plan."""
        return PainReport.from_dict(
            self.client._get(f"/stats/pain/{plan_id}")
        )

    def get_muscle_balance(self, plan_id: int) -> MuscleBalanceReport:
        """Return volume distribution by muscle group for a training plan."""
        return MuscleBalanceReport.from_dict(
            self.client._get(f"/stats/muscle-balance/{plan_id}")
        )

    def get_personal_best(self, user_id: int, exercise_id: int) -> dict:
        """Retrieve the personal best weight for a specific user and exercise."""
        return self.client._get(f"/stats/personal-bests/{user_id}/{exercise_id}")