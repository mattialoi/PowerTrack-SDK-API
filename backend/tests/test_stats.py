import pytest
from app.models.user import User
from app.models.exercise import Exercise
from app.models.training_plan import TrainingPlan
from app.models.workout_day import WorkoutDay
from app.models.plan_exercise import PlanExercise
from app.models.session_log import SessionLog

@pytest.fixture
def seed_data(db_session):
    user = User(username="mario")
    db_session.add(user)
    db_session.commit()

    plan = TrainingPlan(user_id=user.id, name="Forza 1", total_weeks=4)
    db_session.add(plan)
    db_session.commit()

    day = WorkoutDay(plan_id=plan.id, name="Upper/Lower", day_order=1)
    db_session.add(day)
    db_session.commit()

    squat = Exercise(name="Squat", mechanics_type="Multi-joint", target_muscle="Legs")
    curl = Exercise(name="Bicep Curl", mechanics_type="Isolation", target_muscle="Arms")
    db_session.add_all([squat, curl])
    db_session.commit()

    pe_squat = PlanExercise(workout_day_id=day.id, exercise_id=squat.id, exercise_order=1, notes="Squat pesante")
    pe_curl = PlanExercise(workout_day_id=day.id, exercise_id=curl.id, exercise_order=2, notes="Bicipiti")
    db_session.add_all([pe_squat, pe_curl])
    db_session.commit()

    # Log - Settimana 1
    log_squat_w1 = SessionLog(
        plan_exercise_id=pe_squat.id,
        week_number=1,
        sets=3,
        reps=10,
        weight=100.0,  # Vol = 3000
        rpe=8,
        pain_discomfort=False
    )
    log_curl_w1 = SessionLog(
        plan_exercise_id=pe_curl.id,
        week_number=1,
        sets=3,
        reps=12,
        weight=15.0,  # Vol = 540
        rpe=7,
        pain_discomfort=False
    )

    # Log - Settimana 2
    log_squat_w2 = SessionLog(
        plan_exercise_id=pe_squat.id,
        week_number=2,
        sets=3,
        reps=10,
        weight=110.0,  # Vol = 3300
        rpe=9,
        pain_discomfort=True,
        user_feedback="Fastidio leggero al ginocchio sinistro"
    )

    db_session.add_all([log_squat_w1, log_curl_w1, log_squat_w2])
    db_session.commit()

    return {
        "user": user,
        "plan": plan,
        "day": day,
        "squat": squat,
        "curl": curl,
        "pe_squat": pe_squat,
        "pe_curl": pe_curl
    }

def test_volume_by_exercise(client, seed_data):
    pe_squat_id = seed_data["pe_squat"].id
    response = client.get(f"/stats/volume/exercise/{pe_squat_id}")
    assert response.status_code == 200
    data = response.get_json()

    assert data["plan_exercise_id"] == pe_squat_id
    assert data["exercise"] == "Squat"
    assert len(data["data"]) == 2
    assert data["data"][0]["week_number"] == 1
    assert data["data"][0]["volume"] == 3000.0
    assert data["data"][1]["week_number"] == 2
    assert data["data"][1]["volume"] == 3300.0

def test_total_volume_by_week(client, seed_data):
    plan_id = seed_data["plan"].id
    response = client.get(f"/stats/volume/total/{plan_id}")
    assert response.status_code == 200
    res = response.get_json()

    assert res["plan_id"] == plan_id
    assert len(res["data"]) == 2
    assert res["data"][0]["week_number"] == 1
    assert res["data"][0]["total_volume"] == 3540.0
    assert res["data"][1]["week_number"] == 2
    assert res["data"][1]["total_volume"] == 3300.0

def test_volume_multijoint_by_week(client, seed_data):
    plan_id = seed_data["plan"].id
    response = client.get(f"/stats/volume/multi-joint/{plan_id}")
    assert response.status_code == 200
    res = response.get_json()

    assert res["plan_id"] == plan_id
    assert res["mechanics_type"] == "Multi-joint"
    assert len(res["data"]) == 2
    assert res["data"][0]["week_number"] == 1
    assert res["data"][0]["total_volume"] == 3000.0
    assert res["data"][1]["week_number"] == 2
    assert res["data"][1]["total_volume"] == 3300.0

def test_avg_rpe_by_week(client, seed_data):
    plan_id = seed_data["plan"].id
    response = client.get(f"/stats/rpe/{plan_id}")
    assert response.status_code == 200
    res = response.get_json()

    assert res["plan_id"] == plan_id
    assert len(res["data"]) == 2
    assert res["data"][0]["week_number"] == 1
    assert res["data"][0]["avg_rpe"] == 7.5
    assert res["data"][1]["week_number"] == 2
    assert res["data"][1]["avg_rpe"] == 9.0

def test_pain_report(client, seed_data):
    plan_id = seed_data["plan"].id
    response = client.get(f"/stats/pain/{plan_id}")
    assert response.status_code == 200
    res = response.get_json()

    assert res["plan_id"] == plan_id
    assert res["total_pain_flags"] == 1
    assert len(res["data"]) == 1
    assert res["data"][0]["week_number"] == 2
    assert res["data"][0]["exercise"] == "Squat"
    assert res["data"][0]["user_feedback"] == "Fastidio leggero al ginocchio sinistro"

def test_muscle_balance(client, seed_data):
    plan_id = seed_data["plan"].id
    response = client.get(f"/stats/muscle-balance/{plan_id}")
    assert response.status_code == 200
    res = response.get_json()

    assert res["plan_id"] == plan_id
    assert res["total_volume"] == 6840.0
    assert len(res["data"]) == 2
    assert res["data"][0]["target_muscle"] == "Legs"
    assert res["data"][0]["total_volume"] == 6300.0
    assert res["data"][0]["percentage"] == round((6300 / 6840) * 100, 1)
    assert res["data"][1]["target_muscle"] == "Arms"
    assert res["data"][1]["total_volume"] == 540.0
    assert res["data"][1]["percentage"] == round((540 / 6840) * 100, 1)