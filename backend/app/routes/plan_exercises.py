from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas import PlanExerciseSchema
from app.services.plan_exercise_service import PlanExerciseService

plan_exercises_bp = Blueprint("plan_exercises", __name__, url_prefix="/plan-exercises")

@plan_exercises_bp.route("/day/<int:day_id>", methods=["GET"])
def get_exercises_by_day(day_id):
    exercises = PlanExerciseService.get_by_day(day_id)
    return jsonify(PlanExerciseSchema(many=True).dump(exercises)), 200

@plan_exercises_bp.route("/<int:plan_exercise_id>", methods=["GET"])
def get_plan_exercise(plan_exercise_id):
    plan_exercise = PlanExerciseService.get_by_id(plan_exercise_id)
    return jsonify(PlanExerciseSchema().dump(plan_exercise)), 200

@plan_exercises_bp.route("/", methods=["POST"])
def create_plan_exercise():
    schema = PlanExerciseSchema()
    try:
        data = schema.load(request.get_json() or {})
        plan_exercise = PlanExerciseService.create(data)
        return jsonify(schema.dump(plan_exercise)), 201
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

@plan_exercises_bp.route("/<int:plan_exercise_id>", methods=["PUT"])
def update_plan_exercise(plan_exercise_id):
    schema = PlanExerciseSchema(partial=True)
    try:
        data = schema.load(request.get_json() or {})
        plan_exercise = PlanExerciseService.update(plan_exercise_id, data)
        return jsonify(schema.dump(plan_exercise)), 200
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

@plan_exercises_bp.route("/<int:plan_exercise_id>", methods=["DELETE"])
def delete_plan_exercise(plan_exercise_id):
    plan_exercise = PlanExerciseService.delete(plan_exercise_id)
    return jsonify({"message": f"PlanExercise {plan_exercise.id} deleted"}), 200