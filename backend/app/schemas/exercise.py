from marshmallow import Schema, fields, validate
from app.models.exercise import MechanicsType

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    mechanics_type = fields.Enum(MechanicsType, by_value=True, required=True)
    target_muscle = fields.Str(required=True)