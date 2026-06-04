from ..database import db

class WorkoutDay(db.Model):
    __tablename__ = 'workout_days'

    id = db.Column(db.Integer, primary_key=True)
    # Foreign Key: Training plan of reference
    plan_id = db.Column(db.Integer, db.ForeignKey('training_plans.id'), nullable=False)
    
    name = db.Column(db.String(50), nullable=False) # es. "Day 1" "Day A", "Lower Body"
    day_order = db.Column(db.Integer, nullable=False) # 1,2,3.. for ordering days within the plan

    # Relationship One workout day has many exercises
    exercises = db.relationship('PlanExercise', backref='day', lazy=True, cascade="all, delete-orphan")
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "plan_id": self.plan_id,
    #         "name": self.name,
    #         "day_order": self.day_order
    #     }