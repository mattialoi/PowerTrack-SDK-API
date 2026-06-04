from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas import TrainingPlanSchema
from app.services.plan_service import PlanService

plans_bp = Blueprint("plans", __name__, url_prefix="/plans")

@plans_bp.route("/", methods=["GET"])
def get_plans():
    plans = PlanService.get_all()
    return jsonify(TrainingPlanSchema(many=True).dump(plans)), 200

@plans_bp.route("/<int:plan_id>", methods=["GET"])
def get_plan(plan_id):
    plan = PlanService.get_by_id(plan_id)
    return jsonify(TrainingPlanSchema().dump(plan)), 200

@plans_bp.route("/user/<int:user_id>", methods=["GET"])
def get_plans_by_user(user_id):
    plans = PlanService.get_by_user(user_id)
    return jsonify(TrainingPlanSchema(many=True).dump(plans)), 200

@plans_bp.route("/", methods=["POST"])
def create_plan():
    schema = TrainingPlanSchema()
    try:
        data = schema.load(request.get_json() or {})
        plan = PlanService.create(data)
        return jsonify(schema.dump(plan)), 201
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

@plans_bp.route("/<int:plan_id>", methods=["PUT"])
def update_plan(plan_id):
    schema = TrainingPlanSchema(partial=True)
    try:
        data = schema.load(request.get_json() or {})
        plan = PlanService.update(plan_id, data)
        return jsonify(schema.dump(plan)), 200
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

@plans_bp.route("/<int:plan_id>", methods=["DELETE"])
def delete_plan(plan_id):
    plan = PlanService.delete(plan_id)
    return jsonify({"message": f"Plan {plan.id} deleted"}), 200