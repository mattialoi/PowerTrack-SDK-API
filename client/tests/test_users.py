from unittest.mock import patch
from client.models import User

def test_users_list(client, mock_response):
    """Verify list users retrieves and parses models."""
    mock_response.json.return_value = [
        {"id": 1, "username": "marco"},
        {"id": 2, "username": "milo"}
    ]
    with patch("requests.Session.get", return_value=mock_response):
        users = client.users.list()
        assert len(users) == 2
        assert all(isinstance(u, User) for u in users)
        assert users[0].username == "marco"
        assert users[1].id == 2

def test_users_get(client, mock_response):
    """Verify get user retrieves a user by id."""
    mock_response.json.return_value = {"id": 1, "username": "marco"}
    with patch("requests.Session.get", return_value=mock_response):
        user = client.users.get(1)
        assert isinstance(user, User)
        assert user.id == 1
        assert user.username == "marco"

def test_users_create(client, mock_response):
    """Verify create user returns a User instance."""
    mock_response.json.return_value = {"id": 1, "username": "marco"}
    with patch("requests.Session.post", return_value=mock_response) as mock_post:
        user = client.users.create(username="marco")
        assert isinstance(user, User)
        assert user.username == "marco"
        mock_post.assert_called_once_with("http://127.0.0.1:8000/users/", json={"username": "marco"}, timeout=10)

def test_users_delete(client, mock_response):
    """Verify delete user sends a delete request."""
    mock_response.json.return_value = {"message": "User deleted"}
    with patch("requests.Session.delete", return_value=mock_response) as mock_delete:
        res = client.users.delete(1)
        assert res["message"] == "User deleted"
        mock_delete.assert_called_once_with("http://127.0.0.1:8000/users/1", timeout=10)