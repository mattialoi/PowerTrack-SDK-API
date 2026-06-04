from app.models.session_log import SessionLog
from app.models.plan_exercise import PlanExercise
from app.models.workout_day import WorkoutDay
from app.models.exercise import Exercise
from app.models.training_plan import TrainingPlan

class VolumeService:
    @staticmethod
    def get_logs_for_plan(plan_id, mechanics_type_filter=None):
        """
        Fetch all session logs for a given training plan, with optional mechanics type filter.
        """
        # Ensure the training plan exists, otherwise raise 404
        TrainingPlan.query.get_or_404(plan_id)

        # Get all workout days associated with the plan
        days = WorkoutDay.query.filter_by(plan_id=plan_id).all()
        if not days:
            return []

        day_ids = [day.id for day in days]

        # Query planned exercises that belong to those workout days
        query = PlanExercise.query.join(
            Exercise,
            PlanExercise.exercise_id == Exercise.id
        ).filter(
            PlanExercise.workout_day_id.in_(day_ids)
        )

        # Apply mechanics type filter if provided (e.g. "Multi-joint")
        if mechanics_type_filter:
            query = query.filter(Exercise.mechanics_type == mechanics_type_filter)

        plan_exercises = query.all()
        if not plan_exercises:
            return []

        plan_exercise_ids = [pe.id for pe in plan_exercises]

        # Return all session logs belonging to the plan exercises
        return SessionLog.query.filter(
            SessionLog.plan_exercise_id.in_(plan_exercise_ids)
        ).all()

    @staticmethod
    def volume_by_exercise(plan_exercise_id):
        """
        Calculate volume progression week-by-week for a single scheduled exercise.
        """
        # Ensure the plan exercise exists
        plan_exercise = PlanExercise.query.get_or_404(plan_exercise_id)

        # Fetch all logged sessions for the exercise ordered by week number
        logs = SessionLog.query.filter_by(
            plan_exercise_id=plan_exercise_id
        ).order_by(
            SessionLog.week_number
        ).all()

        # Compute volume (sets * reps * weight) for each week
        return {
            "plan_exercise_id": plan_exercise_id,
            "exercise": plan_exercise.exercise.name,
            "data": [
                {
                    "week_number": log.week_number,
                    "sets": log.sets,
                    "reps": log.reps,
                    "weight": log.weight,
                    "volume": round(log.sets * log.reps * log.weight, 2),
                    "rpe": log.rpe
                }
                for log in logs
            ]
        }

    @staticmethod
    def total_volume_by_week(plan_id, mechanics_type_filter=None):
        """
        Calculate the sum of all training volume per week for a plan.
        """
        logs = VolumeService.get_logs_for_plan(plan_id, mechanics_type_filter)

        week_totals = {}

        # Aggregate volume per week number
        for log in logs:
            volume = log.sets * log.reps * log.weight
            week_totals[log.week_number] = round(
                week_totals.get(log.week_number, 0) + volume,
                2
            )

        return [
            {"week_number": week, "total_volume": total}
            for week, total in sorted(week_totals.items())
        ]

    @staticmethod
    def muscle_balance(plan_id):
        """
        Calculate target muscle volume breakdown and percentages.
        """
        # Ensure the training plan exists
        TrainingPlan.query.get_or_404(plan_id)

        # Fetch workout days
        days = WorkoutDay.query.filter_by(plan_id=plan_id).all()
        if not days:
            return {
                "total_volume": 0,
                "data": []
            }

        day_ids = [day.id for day in days]

        # Get plan exercises to map their target muscle group
        plan_exercises = PlanExercise.query.join(
            Exercise,
            PlanExercise.exercise_id == Exercise.id
        ).filter(
            PlanExercise.workout_day_id.in_(day_ids)
        ).all()

        if not plan_exercises:
            return {
                "total_volume": 0,
                "data": []
            }

        # Create a dictionary to map each plan exercise ID to its target muscle
        muscle_map = {
            plan_exercise.id: plan_exercise.exercise.target_muscle
            for plan_exercise in plan_exercises
        }

        # Fetch all session logs for these exercises
        logs = SessionLog.query.filter(
            SessionLog.plan_exercise_id.in_(muscle_map.keys())
        ).all()

        muscle_totals = {}

        # Aggregate total volume per muscle group
        for log in logs:
            muscle = muscle_map.get(log.plan_exercise_id, "Unknown")
            volume = log.sets * log.reps * log.weight
            muscle_totals[muscle] = round(
                muscle_totals.get(muscle, 0) + volume,
                2
            )

        total = sum(muscle_totals.values())

        if total == 0:
            return {
                "total_volume": 0,
                "data": []
            }

        # Prepare the list of muscle volume breakdown with percentages
        data = [
            {
                "target_muscle": muscle,
                "total_volume": volume,
                "percentage": round((volume / total) * 100, 1)
            }
            for muscle, volume in sorted(
                muscle_totals.items(),
                key=lambda item: item[1],
                reverse=True
            )
        ]

        return {
            "total_volume": round(total, 2),
            "data": data
        }