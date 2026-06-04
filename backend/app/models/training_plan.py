from ..database import db
from datetime import datetime

class TrainingPlan(db.Model):
    __tablename__ = 'training_plans'

    id = db.Column(db.Integer, primary_key=True)
    # Foreign Key: user of reference
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(100), nullable=False) # es. "Mesocycle 1 - volume"
    total_weeks = db.Column(db.Integer, nullable=False) # number of weeks the plan is designed for (es. 5-6 weeks)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: One plan has many workout days
    days = db.relationship('WorkoutDay', backref='plan', lazy=True, cascade="all, delete-orphan")
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "user_id": self.user_id,
    #         "name": self.name,
    #         "total_weeks": self.total_weeks,
    #         "start_date": self.start_date.isoformat() if self.start_date else None
    #     }