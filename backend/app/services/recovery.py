from app.services.volume import VolumeService
from app.models.plan_exercise import PlanExercise

class RecoveryService:
    @staticmethod
    def pain_report(plan_id):
        """
        Retrieve all logged training session entries where pain or discomfort was reported.
        """
        # Get logs and filter to keep only those flagged with pain/discomfort
        logs = VolumeService.get_logs_for_plan(plan_id)
        pain_logs = [log for log in logs if log.pain_discomfort is True]

        data = []

        # Build detailed report containing exercise names and user feedback
        for log in pain_logs:
            plan_exercise = PlanExercise.query.get(log.plan_exercise_id)
            exercise_name = plan_exercise.exercise.name if plan_exercise else "Unknown"

            data.append({
                "week_number": log.week_number,
                "exercise": exercise_name,
                "rpe": log.rpe,
                "user_feedback": log.user_feedback
            })

        return sorted(data, key=lambda item: item["week_number"])