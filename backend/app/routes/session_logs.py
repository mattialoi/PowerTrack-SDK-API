from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas import SessionLogSchema
from app.services.session_log_service import SessionLogService

session_logs_bp = Blueprint("session_logs", __name__, url_prefix="/session-logs")

@session_logs_bp.route("/plan-exercise/<int:plan_exercise_id>", methods=["GET"])
def get_logs_by_plan_exercise(plan_exercise_id):
    logs = SessionLogService.get_by_plan_exercise(plan_exercise_id)
    return jsonify(SessionLogSchema(many=True).dump(logs)), 200

@session_logs_bp.route("/<int:log_id>", methods=["GET"])
def get_log(log_id):
    log = SessionLogService.get_by_id(log_id)
    return jsonify(SessionLogSchema().dump(log)), 200

@session_logs_bp.route("/", methods=["POST"])
def create_log():
    schema = SessionLogSchema()
    try:
        data = schema.load(request.get_json() or {})
        log = SessionLogService.create(data)
        return jsonify(schema.dump(log)), 201
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

@session_logs_bp.route("/<int:log_id>", methods=["PUT"])
def update_log(log_id):
    schema = SessionLogSchema(partial=True)
    try:
        data = schema.load(request.get_json() or {})
        log = SessionLogService.update(log_id, data)
        return jsonify(schema.dump(log)), 200
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

@session_logs_bp.route("/<int:log_id>", methods=["DELETE"])
def delete_log(log_id):
    log = SessionLogService.delete(log_id)
    return jsonify({"message": f"SessionLog {log.id} deleted"}), 200