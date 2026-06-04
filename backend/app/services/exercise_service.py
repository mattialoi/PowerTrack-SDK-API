from app.database import db
from app.models.exercise import Exercise
from marshmallow import ValidationError

class ExerciseService:
    @staticmethod
    def get_all(target_muscle=None, mechanics_type=None):
        query = Exercise.query
        if target_muscle:
            query = query.filter_by(target_muscle=target_muscle)
        if mechanics_type:
            query = query.filter_by(mechanics_type=mechanics_type)
        return query.all()

    @staticmethod
    def get_by_id(exercise_id):
        return Exercise.query.get_or_404(exercise_id)

    @staticmethod
    def create(data):
        existing = Exercise.query.filter_by(name=data["name"]).first()
        if existing:
            raise ValidationError({"name": ["Exercise already exists in catalog"]})

        exercise = Exercise(
            name=data["name"],
            mechanics_type=data["mechanics_type"],
            target_muscle=data["target_muscle"]
        )
        db.session.add(exercise)
        db.session.commit()
        return exercise

    @staticmethod
    def delete(exercise_id):
        exercise = Exercise.query.get_or_404(exercise_id)
        db.session.delete(exercise)
        db.session.commit()
        return exercise