from ..database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    #password_hash = db.Column(db.String(128), nullable=False)
    #weight = db.Column(db.Float, nullable=True) 
    #height = db.Column(db.Float, nullable=True)

    # Relationship: One user has many training plans
    plans = db.relationship('TrainingPlan', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "username": self.username
    #     }
