from ..database import db

class SessionLog(db.Model):
    __tablename__ = 'session_logs'

    id = db.Column(db.Integer, primary_key=True)
    # Foreign Key: exercise of reference
    plan_exercise_id = db.Column(db.Integer, db.ForeignKey('plan_exercises.id'), nullable=False)
    
    # Data Training (for a specific week of the plan)
    week_number = db.Column(db.Integer, nullable=False) # week number in the plan (1, 2, 3...)
    sets = db.Column(db.Integer, nullable=False) # number of sets 
    reps = db.Column(db.Integer, nullable=False) # number of reps 
    weight = db.Column(db.Float, nullable=False) # load in kg 
    
    # Feedback of the user for a specific week
    rpe = db.Column(db.Integer, nullable=True) # rpe perceived exertion (1-10)
    user_feedback = db.Column(db.Text, nullable=True) # User note feedback
    pain_discomfort = db.Column(db.Boolean, default=False) # Flag for pain/discomfort during the exercise (True/False)
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "plan_exercise_id": self.plan_exercise_id,
    #         "week_number": self.week_number,
    #         "sets": self.sets,
    #         "reps": self.reps,
    #         "weight": self.weight,
    #         "rpe": self.rpe,
    #         "user_feedback": self.user_feedback,
    #         "pain_discomfort": self.pain_discomfort
    #     }