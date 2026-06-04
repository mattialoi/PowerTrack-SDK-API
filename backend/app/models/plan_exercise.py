from ..database import db

class PlanExercise(db.Model):
    __tablename__ = 'plan_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_day_id = db.Column(db.Integer, db.ForeignKey('workout_days.id'), nullable=False)
    
    # Foreign Key: exercise of reference
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    
    exercise_order = db.Column(db.Integer, nullable=False) # 1° exercise, 2° exercise...
    notes = db.Column(db.String(255), nullable=True) # es. "Break 90s""

    # Relationship: for retrieving info faster
    exercise = db.relationship('Exercise')
    
    # Relationship: This exercise has many progressions (one per week)
    progressions = db.relationship('SessionLog', backref='plan_exercise', lazy=True, cascade="all, delete-orphan")
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "workout_day_id": self.workout_day_id,
    #         "exercise_id": self.exercise_id,
    #         "exercise_order": self.exercise_order,
    #         "notes": self.notes
    #     }