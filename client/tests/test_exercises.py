from unittest.mock import patch
from client.models import Exercise

def test_exercises_list(client, mock_response):
    """Verify list exercises with query filtering."""
    mock_response.json.return_value = [{"id": 3, "name": "Squat", "mechanics_type": "Multi-joint", "target_muscle": "Legs"}]
    with patch("requests.Session.get", return_value=mock_response):
        exs = client.exercises.list(target_muscle="Legs", mechanics_type="Multi-joint")
        assert len(exs) == 1
        assert isinstance(exs[0], Exercise)
        assert exs[0].name == "Squat"

def test_exercises_get(client, mock_response):
    """Verify get single exercise."""
    mock_response.json.return_value = {"id": 3, "name": "Squat", "mechanics_type": "Multi-joint", "target_muscle": "Legs"}
    with patch("requests.Session.get", return_value=mock_response):
        ex = client.exercises.get(3)
        assert isinstance(ex, Exercise)
        assert ex.id == 3

def test_exercises_create(client, mock_response):
    """Verify catalog exercise creation."""
    mock_response.json.return_value = {"id": 3, "name": "Squat", "mechanics_type": "Multi-joint", "target_muscle": "Legs"}
    with patch("requests.Session.post", return_value=mock_response):
        ex = client.exercises.create(name="Squat", mechanics_type="Multi-joint", target_muscle="Legs")
        assert isinstance(ex, Exercise)
        assert ex.name == "Squat"

def test_exercises_delete(client, mock_response):
    """Verify exercise deletion from catalog."""
    mock_response.json.return_value = {"message": "Exercise deleted"}
    with patch("requests.Session.delete", return_value=mock_response):
        res = client.exercises.delete(3)
        assert res["message"] == "Exercise deleted"