import pytest
from app.models.exercise import Exercise

def test_create_exercise_success(client):
    payload = {
        "name": "Squat",
        "mechanics_type": "Multi-joint",
        "target_muscle": "Legs"
    }
    response = client.post("/exercises/", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == "Squat"
    assert data["mechanics_type"] == "Multi-joint"
    assert data["target_muscle"] == "Legs"

    ex = Exercise.query.filter_by(name="Squat").first()
    assert ex is not None
    assert ex.target_muscle == "Legs"

def test_create_exercise_invalid_mechanics(client):
    payload = {
        "name": "Bench Press",
        "mechanics_type": "Compound",  # not valid
        "target_muscle": "Chest"
    }
    response = client.post("/exercises/", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    assert "mechanics_type" in data["errors"]

def test_create_exercise_duplicate_name(client):
    payload = {
        "name": "Squat",
        "mechanics_type": "Multi-joint",
        "target_muscle": "Legs"
    }
    client.post("/exercises/", json=payload)

    response = client.post("/exercises/", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    assert "already exists" in data["errors"]["name"][0]

def test_get_exercises_with_filter(client):
    client.post("/exercises/", json={
        "name": "Deadlift",
        "mechanics_type": "Multi-joint",
        "target_muscle": "Back"
    })
    client.post("/exercises/", json={
        "name": "Bicep Curl",
        "mechanics_type": "Isolation",
        "target_muscle": "Arms"
    })

    response = client.get("/exercises/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

    response = client.get("/exercises/?target_muscle=Back")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Deadlift"

    response = client.get("/exercises/?mechanics_type=Isolation")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Bicep Curl"

def test_delete_exercise(client):
    response = client.post("/exercises/", json={
        "name": "Squat",
        "mechanics_type": "Multi-joint",
        "target_muscle": "Legs"
    })
    exercise_id = response.get_json()["id"]

    response = client.delete(f"/exercises/{exercise_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == f"Exercise {exercise_id} deleted"
    assert Exercise.query.get(exercise_id) is None