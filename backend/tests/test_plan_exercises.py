import pytest
from app.models.plan_exercise import PlanExercise
from app.models.workout_day import WorkoutDay
from app.models.training_plan import TrainingPlan
from app.models.user import User
from app.models.exercise import Exercise

@pytest.fixture
def seed_structures(db_session):
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
    
    return {"day": day, "exercise": ex}

def test_create_plan_exercise_success(client, seed_structures):
    day_id = seed_structures["day"].id
    ex_id = seed_structures["exercise"].id
    
    payload = {
        "workout_day_id": day_id,
        "exercise_id": ex_id,
        "exercise_order": 1,
        "notes": "Break 90s"
    }
    response = client.post("/plan-exercises/", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["workout_day_id"] == day_id
    assert data["exercise_id"] == ex_id
    assert data["exercise_order"] == 1
    assert data["notes"] == "Break 90s"

def test_get_exercises_by_day(client, seed_structures):
    day_id = seed_structures["day"].id
    ex_id = seed_structures["exercise"].id
    
    client.post("/plan-exercises/", json={
        "workout_day_id": day_id,
        "exercise_id": ex_id,
        "exercise_order": 1,
        "notes": "Notes A"
    })
    
    response = client.get(f"/plan-exercises/day/{day_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["notes"] == "Notes A"

def test_update_plan_exercise(client, seed_structures):
    day_id = seed_structures["day"].id
    ex_id = seed_structures["exercise"].id
    
    res_create = client.post("/plan-exercises/", json={
        "workout_day_id": day_id,
        "exercise_id": ex_id,
        "exercise_order": 1,
        "notes": "Notes A"
    })
    pe_id = res_create.get_json()["id"]
    
    response = client.put(f"/plan-exercises/{pe_id}", json={"exercise_order": 2, "notes": "New notes"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["exercise_order"] == 2
    assert data["notes"] == "New notes"

def test_delete_plan_exercise(client, seed_structures):
    day_id = seed_structures["day"].id
    ex_id = seed_structures["exercise"].id
    
    res_create = client.post("/plan-exercises/", json={
        "workout_day_id": day_id,
        "exercise_id": ex_id,
        "exercise_order": 1
    })
    pe_id = res_create.get_json()["id"]
    
    response = client.delete(f"/plan-exercises/{pe_id}")
    assert response.status_code == 200
    assert PlanExercise.query.get(pe_id) is None