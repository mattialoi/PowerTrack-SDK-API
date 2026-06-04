from unittest.mock import patch
from client.models import WorkoutDay

def test_workout_days_get_by_plan(client, mock_response):
    """Verify workout days by plan retrieval."""
    mock_response.json.return_value = [{"id": 5, "plan_id": 10, "name": "Push", "day_order": 1}]
    with patch("requests.Session.get", return_value=mock_response):
        days = client.workout_days.get_by_plan(10)
        assert len(days) == 1
        assert isinstance(days[0], WorkoutDay)
        assert days[0].name == "Push"

def test_workout_days_get(client, mock_response):
    """Verify get single day."""
    mock_response.json.return_value = {"id": 5, "plan_id": 10, "name": "Push", "day_order": 1}
    with patch("requests.Session.get", return_value=mock_response):
        day = client.workout_days.get(5)
        assert isinstance(day, WorkoutDay)
        assert day.id == 5

def test_workout_days_create(client, mock_response):
    """Verify day creation."""
    mock_response.json.return_value = {"id": 5, "plan_id": 10, "name": "Push", "day_order": 1}
    with patch("requests.Session.post", return_value=mock_response):
        day = client.workout_days.create(plan_id=10, name="Push", day_order=1)
        assert isinstance(day, WorkoutDay)
        assert day.name == "Push"

def test_workout_days_update(client, mock_response):
    """Verify day update."""
    mock_response.json.return_value = {"id": 5, "plan_id": 10, "name": "Pull", "day_order": 2}
    with patch("requests.Session.put", return_value=mock_response):
        day = client.workout_days.update(day_id=5, name="Pull", day_order=2)
        assert day.name == "Pull"
        assert day.day_order == 2

def test_workout_days_delete(client, mock_response):
    """Verify day deletion."""
    mock_response.json.return_value = {"message": "Day deleted"}
    with patch("requests.Session.delete", return_value=mock_response):
        res = client.workout_days.delete(5)
        assert res["message"] == "Day deleted"