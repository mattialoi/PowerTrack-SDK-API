from app.database import db
from app.models.workout_day import WorkoutDay
from app.models.training_plan import TrainingPlan

class WorkoutDayService:
    @staticmethod
    def get_by_plan(plan_id):
        TrainingPlan.query.get_or_404(plan_id)
        return WorkoutDay.query.filter_by(
            plan_id=plan_id
        ).order_by(WorkoutDay.day_order).all()

    @staticmethod
    def get_by_id(day_id):
        return WorkoutDay.query.get_or_404(day_id)

    @staticmethod
    def create(data):
        TrainingPlan.query.get_or_404(data["plan_id"])

        day = WorkoutDay(
            plan_id=data["plan_id"],
            name=data["name"],
            day_order=data["day_order"]
        )
        db.session.add(day)
        db.session.commit()
        return day

    @staticmethod
    def update(day_id, data):
        day = WorkoutDay.query.get_or_404(day_id)

        if "name" in data:
            day.name = data["name"]
        if "day_order" in data:
            day.day_order = data["day_order"]

        db.session.commit()
        return day

    @staticmethod
    def delete(day_id):
        day = WorkoutDay.query.get_or_404(day_id)
        db.session.delete(day)
        db.session.commit()
        return day