from app.database import db
from app.models.plan_exercise import PlanExercise
from app.models.workout_day import WorkoutDay
from app.models.exercise import Exercise

class PlanExerciseService:
    @staticmethod
    def get_by_day(day_id):
        WorkoutDay.query.get_or_404(day_id)
        return PlanExercise.query.filter_by(
            workout_day_id=day_id
        ).order_by(PlanExercise.exercise_order).all()

    @staticmethod
    def get_by_id(plan_exercise_id):
        return PlanExercise.query.get_or_404(plan_exercise_id)

    @staticmethod
    def create(data):
        WorkoutDay.query.get_or_404(data["workout_day_id"])
        Exercise.query.get_or_404(data["exercise_id"])

        plan_exercise = PlanExercise(
            workout_day_id=data["workout_day_id"],
            exercise_id=data["exercise_id"],
            exercise_order=data["exercise_order"],
            notes=data.get("notes")
        )
        db.session.add(plan_exercise)
        db.session.commit()
        return plan_exercise

    @staticmethod
    def update(plan_exercise_id, data):
        plan_exercise = PlanExercise.query.get_or_404(plan_exercise_id)

        if "exercise_order" in data:
            plan_exercise.exercise_order = data["exercise_order"]
        if "notes" in data:
            plan_exercise.notes = data["notes"]

        db.session.commit()
        return plan_exercise

    @staticmethod
    def delete(plan_exercise_id):
        plan_exercise = PlanExercise.query.get_or_404(plan_exercise_id)
        db.session.delete(plan_exercise)
        db.session.commit()
        return plan_exercise