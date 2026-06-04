import pytest
from app.models.workout_day import WorkoutDay
from app.models.training_plan import TrainingPlan
from app.models.user import User

@pytest.fixture
def test_plan(db_session):
    user = User(username="mario")
    db_session.add(user)
    db_session.commit()
    
    plan = TrainingPlan(user_id=user.id, name="Forza", total_weeks=4)
    db_session.add(plan)
    db_session.commit()
    return plan

def test_create_day_success(client, test_plan):
    payload = {
        "plan_id": test_plan.id,
        "name": "Day A - Push",
        "day_order": 1
    }
    response = client.post("/workout-days/", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == "Day A - Push"
    assert data["day_order"] == 1
    assert data["plan_id"] == test_plan.id

def test_create_day_invalid_order(client, test_plan):
    payload = {
        "plan_id": test_plan.id,
        "name": "Day A",
        "day_order": 0
    }
    response = client.post("/workout-days/", json=payload)
    assert response.status_code == 400
    assert "day_order" in response.get_json()["errors"]

def test_get_days_by_plan(client, test_plan):
    client.post("/workout-days/", json={"plan_id": test_plan.id, "name": "Day A", "day_order": 1})
    client.post("/workout-days/", json={"plan_id": test_plan.id, "name": "Day B", "day_order": 2})

    response = client.get(f"/workout-days/plan/{test_plan.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["name"] == "Day A"
    assert data[1]["name"] == "Day B"

def test_update_workout_day(client, test_plan):
    res_create = client.post("/workout-days/", json={"plan_id": test_plan.id, "name": "Day A", "day_order": 1})
    day_id = res_create.get_json()["id"]

    response = client.put(f"/workout-days/{day_id}", json={"name": "Push Day", "day_order": 3})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Push Day"
    assert data["day_order"] == 3

def test_delete_workout_day(client, test_plan):
    res_create = client.post("/workout-days/", json={"plan_id": test_plan.id, "name": "Day A", "day_order": 1})
    day_id = res_create.get_json()["id"]

    response = client.delete(f"/workout-days/{day_id}")
    assert response.status_code == 200
    assert WorkoutDay.query.get(day_id) is None