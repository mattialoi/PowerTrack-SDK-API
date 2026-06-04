from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app.schemas import UserSchema
from app.services.user_service import UserService

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET"])
def get_users():
    users = UserService.get_all()
    return jsonify(UserSchema(many=True).dump(users)), 200

@users_bp.route("/", methods=["POST"])
def create_user():
    schema = UserSchema()
    try:
        data = schema.load(request.get_json() or {})
        user = UserService.create(data)
        return jsonify(schema.dump(user)), 201
    except ValidationError as error:
        return jsonify({"errors": error.messages}), 400

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserService.get_by_id(user_id)
    return jsonify(UserSchema().dump(user)), 200

@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = UserService.delete(user_id)
    return jsonify({"message": f"User {user.id} deleted"}), 200