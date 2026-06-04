from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas import ExerciseSchema
from app.services.exercise_service import ExerciseService

exercises_bp = Blueprint("exercises", __name__, url_prefix="/exercises")

@exercises_bp.route("/", methods=["GET"])
def get_exercises():
    exercises = ExerciseService.get_all(
        target_muscle=request.args.get("target_muscle"),
        mechanics_type=request.args.get("mechanics_type")
    )
    return jsonify(ExerciseSchema(many=True).dump(exercises)), 200

@exercises_bp.route("/<int:exercise_id>", methods=["GET"])
def get_exercise(exercise_id):
    exercise = ExerciseService.get_by_id(exercise_id)
    return jsonify(ExerciseSchema().dump(exercise)), 200

@exercises_bp.route("/", methods=["POST"])
def create_exercise():
    schema = ExerciseSchema()
    try:
        data = schema.load(request.get_json() or {})
        exercise = ExerciseService.create(data)
        return jsonify(schema.dump(exercise)), 201
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

@exercises_bp.route("/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    exercise = ExerciseService.delete(exercise_id)
    return jsonify({"message": f"Exercise {exercise.id} deleted"}), 200