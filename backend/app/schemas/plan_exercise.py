from marshmallow import Schema, fields, validate

class PlanExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_day_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    exercise_order = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)