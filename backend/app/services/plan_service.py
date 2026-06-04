from app.database import db
from app.models.training_plan import TrainingPlan
from app.models.user import User

class PlanService:
    @staticmethod
    def get_all():
        return TrainingPlan.query.all()

    @staticmethod
    def get_by_id(plan_id):
        return TrainingPlan.query.get_or_404(plan_id)

    @staticmethod
    def get_by_user(user_id):
        User.query.get_or_404(user_id)
        return TrainingPlan.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create(data):
        User.query.get_or_404(data["user_id"])

        plan = TrainingPlan(
            user_id=data["user_id"],
            name=data["name"],
            total_weeks=data["total_weeks"]
        )
        db.session.add(plan)
        db.session.commit()
        return plan

    @staticmethod
    def update(plan_id, data):
        plan = TrainingPlan.query.get_or_404(plan_id)

        if "name" in data:
            plan.name = data["name"]
        if "total_weeks" in data:
            plan.total_weeks = data["total_weeks"]

        db.session.commit()
        return plan

    @staticmethod
    def delete(plan_id):
        plan = TrainingPlan.query.get_or_404(plan_id)
        db.session.delete(plan)
        db.session.commit()
        return plan