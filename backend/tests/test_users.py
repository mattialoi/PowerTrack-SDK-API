import pytest
from app.models.user import User

def test_create_user_success(client):
    response = client.post("/users/", json={"username": "mario"})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["username"] == "mario"

    user = User.query.filter_by(username="mario").first()
    assert user is not None
    assert user.username == "mario"

def test_create_user_missing_username(client):
    response = client.post("/users/", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    assert "username" in data["errors"]

def test_create_user_duplicate_username(client):
    client.post("/users/", json={"username": "mario"})

    response = client.post("/users/", json={"username": "mario"})
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data
    assert "username" in data["errors"]
    assert "already taken" in data["errors"]["username"][0]

def test_get_users(client):
    client.post("/users/", json={"username": "mario"})
    client.post("/users/", json={"username": "luigi"})

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["username"] == "mario"
    assert data[1]["username"] == "luigi"

def test_get_user_by_id(client):
    response = client.post("/users/", json={"username": "mario"})
    user_id = response.get_json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == user_id
    assert data["username"] == "mario"

def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404

def test_delete_user(client):
    response = client.post("/users/", json={"username": "mario"})
    user_id = response.get_json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == f"User {user_id} deleted"
    assert User.query.get(user_id) is None