from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas import WorkoutDaySchema
from app.services.workout_day_service import WorkoutDayService

workout_days_bp = Blueprint("workout_days", __name__, url_prefix="/workout-days")

@workout_days_bp.route("/plan/<int:plan_id>", methods=["GET"])
def get_days_by_plan(plan_id):
    days = WorkoutDayService.get_by_plan(plan_id)
    return jsonify(WorkoutDaySchema(many=True).dump(days)), 200

@workout_days_bp.route("/<int:day_id>", methods=["GET"])
def get_day(day_id):
    day = WorkoutDayService.get_by_id(day_id)
    return jsonify(WorkoutDaySchema().dump(day)), 200

@workout_days_bp.route("/", methods=["POST"])
def create_day():
    schema = WorkoutDaySchema()
    try:
        data = schema.load(request.get_json() or {})
        day = WorkoutDayService.create(data)
        return jsonify(schema.dump(day)), 201
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

@workout_days_bp.route("/<int:day_id>", methods=["PUT"])
def update_day(day_id):
    schema = WorkoutDaySchema(partial=True)
    try:
        data = schema.load(request.get_json() or {})
        day = WorkoutDayService.update(day_id, data)
        return jsonify(schema.dump(day)), 200
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

@workout_days_bp.route("/<int:day_id>", methods=["DELETE"])
def delete_day(day_id):
    day = WorkoutDayService.delete(day_id)
    return jsonify({"message": f"WorkoutDay {day.id} deleted"}), 200