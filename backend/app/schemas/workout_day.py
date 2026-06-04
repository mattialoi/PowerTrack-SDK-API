from marshmallow import Schema, fields, validate

class WorkoutDaySchema(Schema):
    id = fields.Int(dump_only=True)
    plan_id = fields.Int(required=True)
    name = fields.Str(required=True)
    day_order = fields.Int(required=True, validate=validate.Range(min=1))