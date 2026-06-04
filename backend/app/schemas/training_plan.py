from marshmallow import Schema, fields, validate

class TrainingPlanSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    name = fields.Str(required=True)
    total_weeks = fields.Int(required=True, validate=validate.Range(min=1))
    start_date = fields.DateTime(dump_only=True)