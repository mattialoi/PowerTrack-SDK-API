from flask import Blueprint, jsonify
from app.services.volume import VolumeService
from app.services.intensity import IntensityService
from app.services.recovery import RecoveryService
from app.services.personal_bests import PersonalBestsService
from app.schemas import (
    ExerciseVolumeReportSchema,
    WeeklyVolumeReportSchema,
    WeeklyRpeReportSchema,
    PainReportSchema,
    MuscleBalanceReportSchema
)

# Initialize the blueprint for stats routes
stats_bp = Blueprint("stats", __name__, url_prefix="/stats")


@stats_bp.route("/volume/exercise/<int:plan_exercise_id>", methods=["GET"])
def volume_by_exercise(plan_exercise_id):
    # Fetch weekly volume progression for a single exercise using VolumeService
    result = VolumeService.volume_by_exercise(plan_exercise_id)

    if not result["data"]:
        result["message"] = "No session logs found for this exercise"

    return jsonify(ExerciseVolumeReportSchema().dump(result)), 200


@stats_bp.route("/volume/multi-joint/<int:plan_id>", methods=["GET"])
def volume_multijoint_by_week(plan_id):
    # Fetch weekly volume for multi-joint exercises using VolumeService
    data = VolumeService.total_volume_by_week(
        plan_id,
        mechanics_type_filter="Multi-joint"
    )

    response = {
        "plan_id": plan_id,
        "mechanics_type": "Multi-joint",
        "data": data
    }

    if not data:
        response["message"] = "No multi-joint session logs found"

    return jsonify(WeeklyVolumeReportSchema().dump(response)), 200


@stats_bp.route("/volume/total/<int:plan_id>", methods=["GET"])
def total_volume_by_week(plan_id):
    # Fetch total weekly volume across all exercises using VolumeService
    data = VolumeService.total_volume_by_week(plan_id)

    response = {
        "plan_id": plan_id,
        "data": data
    }

    if not data:
        response["message"] = "No session logs found for this plan"

    return jsonify(WeeklyVolumeReportSchema().dump(response)), 200


@stats_bp.route("/rpe/<int:plan_id>", methods=["GET"])
def avg_rpe_by_week(plan_id):
    # Calculate average RPE per week using IntensityService
    data = IntensityService.avg_rpe_by_week(plan_id)

    response = {
        "plan_id": plan_id,
        "data": data
    }

    if not data:
        response["message"] = "No RPE data found for this plan"

    return jsonify(WeeklyRpeReportSchema().dump(response)), 200


@stats_bp.route("/pain/<int:plan_id>", methods=["GET"])
def pain_report(plan_id):
    # Retrieve all logged sessions with pain flags using RecoveryService
    data = RecoveryService.pain_report(plan_id)

    response = {
        "plan_id": plan_id,
        "total_pain_flags": len(data),
        "data": data
    }

    if not data:
        response["message"] = "No pain or discomfort reported for this plan"

    return jsonify(PainReportSchema().dump(response)), 200


@stats_bp.route("/muscle-balance/<int:plan_id>", methods=["GET"])
def muscle_balance(plan_id):
    # Compute the training volume percentage per target muscle using VolumeService
    result = VolumeService.muscle_balance(plan_id)

    response = {
        "plan_id": plan_id,
        "total_volume": result["total_volume"],
        "data": result["data"]
    }

    if not result["data"]:
        response["message"] = "No session logs found"

    return jsonify(MuscleBalanceReportSchema().dump(response)), 200


# NEW ENDPOINT: Retrieve personal best weight for a specific user and exercise
@stats_bp.route("/personal-bests/<int:user_id>/<int:exercise_id>", methods=["GET"])
def get_personal_best(user_id, exercise_id):
    # Fetch personal record using PersonalBestsService
    result = PersonalBestsService.get_personal_best(user_id, exercise_id)
    return jsonify(result), 200