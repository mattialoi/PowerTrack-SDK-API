from enum import Enum
from ..database import db

# inheritance from (str, Enum) allows the instances to behave both as strings and as Enums
class MechanicsType(str, Enum):
    MULTI_JOINT = "Multi-joint"
    ISOLATION = "Isolation"
    CARDIO = "Cardio"

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Exercise mechanics type (Multi-joint, Isolation, Cardio)
    mechanics_type = db.Column(db.Enum(MechanicsType), nullable=False) 
    
    target_muscle = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f'<Exercise {self.name} - {self.target_muscle}>'
    
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "mechanics_type": self.mechanics_type,
    #         "target_muscle": self.target_muscle
    #     }