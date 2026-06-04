from app.models.session_log import SessionLog
from app.models.plan_exercise import PlanExercise
from app.models.workout_day import WorkoutDay
from app.models.training_plan import TrainingPlan
from app.models.user import User
from app.models.exercise import Exercise

class PersonalBestsService:
    @staticmethod
    def get_personal_best(user_id, exercise_id):
        """
        Find the personal best (maximum weight lifted) for a specific user and exercise.
        """
        # Ensure the user and exercise exist in the database
        User.query.get_or_404(user_id)
        Exercise.query.get_or_404(exercise_id)

        # Query all logs associated with this user and this exercise
        logs = SessionLog.query.join(
            PlanExercise, SessionLog.plan_exercise_id == PlanExercise.id
        ).join(
            WorkoutDay, PlanExercise.workout_day_id == WorkoutDay.id
        ).join(
            TrainingPlan, WorkoutDay.plan_id == TrainingPlan.id
        ).filter(
            TrainingPlan.user_id == user_id,
            PlanExercise.exercise_id == exercise_id
        ).all()

        if not logs:
            return {
                "user_id": user_id,
                "exercise_id": exercise_id,
                "max_weight": 0.0,
                "reps_at_max": 0,
                "week_achieved": None
            }

        # Find the log entry with the highest weight value
        best_log = max(logs, key=lambda log: log.weight)

        return {
            "user_id": user_id,
            "exercise_id": exercise_id,
            "max_weight": best_log.weight,
            "reps_at_max": best_log.reps,
            "week_achieved": best_log.week_number
        }