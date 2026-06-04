import pytest
from app.models.training_plan import TrainingPlan
from app.models.user import User

@pytest.fixture
def test_user(db_session):
    user = User(username="mario")
    db_session.add(user)
    db_session.commit()
    return user

def test_create_plan_success(client, test_user):
    payload = {
        "user_id": test_user.id,
        "name": "Meso 1 - Ipertrofia",
        "total_weeks": 6
    }
    response = client.post("/plans/", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == "Meso 1 - Ipertrofia"
    assert data["total_weeks"] == 6
    assert data["user_id"] == test_user.id

def test_create_plan_missing_fields(client, test_user):
    payload = {
        "user_id": test_user.id,
        "name": "Meso 1"
    }
    response = client.post("/plans/", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "total_weeks" in data["errors"]

def test_create_plan_invalid_weeks(client, test_user):
    payload = {
        "user_id": test_user.id,
        "name": "Meso 1",
        "total_weeks": 0
    }
    response = client.post("/plans/", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "total_weeks" in data["errors"]

def test_create_plan_user_not_found(client):
    payload = {
        "user_id": 999,
        "name": "Meso 1",
        "total_weeks": 4
    }
    response = client.post("/plans/", json=payload)
    assert response.status_code == 404

def test_get_plans_by_user(client, test_user):
    client.post("/plans/", json={"user_id": test_user.id, "name": "Plan A", "total_weeks": 4})
    client.post("/plans/", json={"user_id": test_user.id, "name": "Plan B", "total_weeks": 5})

    response = client.get(f"/plans/user/{test_user.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["name"] == "Plan A"
    assert data[1]["name"] == "Plan B"

def test_update_plan(client, test_user):
    res_create = client.post("/plans/", json={"user_id": test_user.id, "name": "Plan A", "total_weeks": 4})
    plan_id = res_create.get_json()["id"]

    response = client.put(f"/plans/{plan_id}", json={"name": "Plan A Modificato"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Plan A Modificato"
    assert data["total_weeks"] == 4

def test_delete_plan(client, test_user):
    res_create = client.post("/plans/", json={"user_id": test_user.id, "name": "Plan A", "total_weeks": 4})
    plan_id = res_create.get_json()["id"]

    response = client.delete(f"/plans/{plan_id}")
    assert response.status_code == 200
    assert TrainingPlan.query.get(plan_id) is None