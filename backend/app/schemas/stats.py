from marshmallow import Schema, fields

# --- 1. Schemi per volume per singolo esercizio ---
class ExerciseVolumeDataSchema(Schema):
    week_number = fields.Int(dump_only=True)
    sets = fields.Int(dump_only=True)
    reps = fields.Int(dump_only=True)
    weight = fields.Float(dump_only=True)
    volume = fields.Float(dump_only=True)
    rpe = fields.Int(dump_only=True, allow_none=True)

class ExerciseVolumeReportSchema(Schema):
    plan_exercise_id = fields.Int(dump_only=True)
    exercise = fields.Str(dump_only=True)
    data = fields.Nested(ExerciseVolumeDataSchema, many=True, dump_only=True)
    message = fields.Str(dump_only=True)


# --- 2. Schemi per volume totale e multi-articolare ---
class WeeklyVolumeDataSchema(Schema):
    week_number = fields.Int(dump_only=True)
    total_volume = fields.Float(dump_only=True)

class WeeklyVolumeReportSchema(Schema):
    plan_id = fields.Int(dump_only=True)
    mechanics_type = fields.Str(dump_only=True)  # Opzionale
    data = fields.Nested(WeeklyVolumeDataSchema, many=True, dump_only=True)
    message = fields.Str(dump_only=True)


# --- 3. Schemi per RPE medio ---
class WeeklyRpeDataSchema(Schema):
    week_number = fields.Int(dump_only=True)
    avg_rpe = fields.Float(dump_only=True)
    sessions_logged = fields.Int(dump_only=True)

class WeeklyRpeReportSchema(Schema):
    plan_id = fields.Int(dump_only=True)
    data = fields.Nested(WeeklyRpeDataSchema, many=True, dump_only=True)
    message = fields.Str(dump_only=True)


# --- 4. Schemi per report del dolore ---
class PainLogSchema(Schema):
    week_number = fields.Int(dump_only=True)
    exercise = fields.Str(dump_only=True)
    rpe = fields.Int(dump_only=True, allow_none=True)
    user_feedback = fields.Str(dump_only=True, allow_none=True)

class PainReportSchema(Schema):
    plan_id = fields.Int(dump_only=True)
    total_pain_flags = fields.Int(dump_only=True)
    data = fields.Nested(PainLogSchema, many=True, dump_only=True)
    message = fields.Str(dump_only=True)


# --- 5. Schemi per bilanciamento muscolare ---
class MuscleBalanceDataSchema(Schema):
    target_muscle = fields.Str(dump_only=True)
    total_volume = fields.Float(dump_only=True)
    percentage = fields.Float(dump_only=True)

class MuscleBalanceReportSchema(Schema):
    plan_id = fields.Int(dump_only=True)
    total_volume = fields.Float(dump_only=True)
    data = fields.Nested(MuscleBalanceDataSchema, many=True, dump_only=True)
    message = fields.Str(dump_only=True)