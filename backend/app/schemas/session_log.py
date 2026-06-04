from marshmallow import Schema, fields, validate

class SessionLogSchema(Schema):
    id = fields.Int(dump_only=True)
    plan_exercise_id = fields.Int(required=True)
    week_number = fields.Int(required=True, validate=validate.Range(min=1))
    sets = fields.Int(required=True, validate=validate.Range(min=1))
    reps = fields.Int(required=True, validate=validate.Range(min=1))
    weight = fields.Float(required=True, validate=validate.Range(min=0))
    rpe = fields.Int(allow_none=True, validate=validate.Range(min=1, max=10))
    user_feedback = fields.Str(allow_none=True)
    pain_discomfort = fields.Bool(load_default=False)