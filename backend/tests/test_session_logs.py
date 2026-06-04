import pytest
from app.models.session_log import SessionLog
from app.models.plan_exercise import PlanExercise
from app.models.workout_day import WorkoutDay
from app.models.training_plan import TrainingPlan
from app.models.user import User
from app.models.exercise import Exercise

@pytest.fixture
def seed_pe(db_session):
    user = User(username="mario")
    db_session.add(user)
    db_session.commit()
    
    plan = TrainingPlan(user_id=user.id, name="Forza", total_weeks=4)
    db_session.add(plan)
    db_session.commit()
    
    day = WorkoutDay(plan_id=plan.id, name="Day A", day_order=1)
    db_session.add(day)
    db_session.commit()
    
    ex = Exercise(name="Squat", mechanics_type="Multi-joint", target_muscle="Legs")
    db_session.add(ex)
    db_session.commit()
    
    pe = PlanExercise(workout_day_id=day.id, exercise_id=ex.id, exercise_order=1)
    db_session.add(pe)
    db_session.commit()
    
    return pe

def test_create_log_success(client, seed_pe):
    payload = {
        "plan_exercise_id": seed_pe.id,
        "week_number": 1,
        "sets": 3,
        "reps": 10,
        "weight": 85.5,
        "rpe": 8,
        "user_feedback": "Good session",
        "pain_discomfort": False
    }
    response = client.post("/session-logs/", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["sets"] == 3
    assert data["weight"] == 85.5
    assert data["rpe"] == 8

def test_create_log_invalid_rpe(client, seed_pe):
    payload = {
        "plan_exercise_id": seed_pe.id,
        "week_number": 1,
        "sets": 3,
        "reps": 10,
        "weight": 80.0,
        "rpe": 11  # not valid
    }
    response = client.post("/session-logs/", json=payload)
    assert response.status_code == 400
    assert "rpe" in response.get_json()["errors"]

def test_create_log_negative_weight(client, seed_pe):
    payload = {
        "plan_exercise_id": seed_pe.id,
        "week_number": 1,
        "sets": 3,
        "reps": 10,
        "weight": -5.0,  # not valid (negative)
        "rpe": 8
    }
    response = client.post("/session-logs/", json=payload)
    assert response.status_code == 400
    assert "weight" in response.get_json()["errors"]

def test_get_logs_by_plan_exercise(client, seed_pe):
    client.post("/session-logs/", json={
        "plan_exercise_id": seed_pe.id,
        "week_number": 1,
        "sets": 3,
        "reps": 10,
        "weight": 80.0
    })
    
    response = client.get(f"/session-logs/plan-exercise/{seed_pe.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["weight"] == 80.0

def test_update_session_log(client, seed_pe):
    res_create = client.post("/session-logs/", json={
        "plan_exercise_id": seed_pe.id,
        "week_number": 1,
        "sets": 3,
        "reps": 10,
        "weight": 80.0,
        "rpe": 8
    })
    log_id = res_create.get_json()["id"]
    
    response = client.put(f"/session-logs/{log_id}", json={"weight": 85.0, "rpe": 9})
    assert response.status_code == 200
    data = response.get_json()
    assert data["weight"] == 85.0
    assert data["rpe"] == 9

def test_delete_session_log(client, seed_pe):
    res_create = client.post("/session-logs/", json={
        "plan_exercise_id": seed_pe.id,
        "week_number": 1,
        "sets": 3,
        "reps": 10,
        "weight": 80.0
    })
    log_id = res_create.get_json()["id"]
    
    response = client.delete(f"/session-logs/{log_id}")
    assert response.status_code == 200
    assert SessionLog.query.get(log_id) is None