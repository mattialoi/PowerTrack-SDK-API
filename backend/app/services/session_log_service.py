from app.database import db
from app.models.session_log import SessionLog
from app.models.plan_exercise import PlanExercise

class SessionLogService:
    @staticmethod
    def get_by_plan_exercise(plan_exercise_id):
        PlanExercise.query.get_or_404(plan_exercise_id)
        return SessionLog.query.filter_by(
            plan_exercise_id=plan_exercise_id
        ).order_by(SessionLog.week_number).all()

    @staticmethod
    def get_by_id(log_id):
        return SessionLog.query.get_or_404(log_id)

    @staticmethod
    def create(data):
        PlanExercise.query.get_or_404(data["plan_exercise_id"])

        log = SessionLog(
            plan_exercise_id=data["plan_exercise_id"],
            week_number=data["week_number"],
            sets=data["sets"],
            reps=data["reps"],
            weight=data["weight"],
            rpe=data.get("rpe"),
            user_feedback=data.get("user_feedback"),
            pain_discomfort=data.get("pain_discomfort", False)
        )
        db.session.add(log)
        db.session.commit()
        return log

    @staticmethod
    def update(log_id, data):
        log = SessionLog.query.get_or_404(log_id)

        if "sets" in data:
            log.sets = data["sets"]
        if "reps" in data:
            log.reps = data["reps"]
        if "weight" in data:
            log.weight = data["weight"]
        if "rpe" in data:
            log.rpe = data["rpe"]
        if "user_feedback" in data:
            log.user_feedback = data["user_feedback"]
        if "pain_discomfort" in data:
            log.pain_discomfort = data["pain_discomfort"]

        db.session.commit()
        return log

    @staticmethod
    def delete(log_id):
        log = SessionLog.query.get_or_404(log_id)
        db.session.delete(log)
        db.session.commit()
        return log