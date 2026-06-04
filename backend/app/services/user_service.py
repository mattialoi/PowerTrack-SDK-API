from app.database import db
from app.models.user import User
from marshmallow import ValidationError

class UserService:
    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get_or_404(user_id)

    @staticmethod
    def create(data):
        existing = User.query.filter_by(username=data["username"]).first()
        if existing:
            raise ValidationError({"username": ["username already taken"]})

        user = User(username=data["username"])
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return user