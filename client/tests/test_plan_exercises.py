from unittest.mock import patch
from client.models import PlanExercise

def test_plan_exercises_get_by_day(client, mock_response):
    """Verify plan exercises by day retrieval."""
    mock_response.json.return_value = [{"id": 1, "workout_day_id": 5, "exercise_id": 3, "exercise_order": 1, "notes": "3x5"}]
    with patch("requests.Session.get", return_value=mock_response):
        pes = client.plan_exercises.get_by_day(5)
        assert len(pes) == 1
        assert isinstance(pes[0], PlanExercise)
        assert pes[0].id == 1

def test_plan_exercises_get(client, mock_response):
    """Verify retrieving single plan exercise."""
    mock_response.json.return_value = {"id": 1, "workout_day_id": 5, "exercise_id": 3, "exercise_order": 1, "notes": "3x5"}
    with patch("requests.Session.get", return_value=mock_response):
        pe = client.plan_exercises.get(1)
        assert isinstance(pe, PlanExercise)
        assert pe.notes == "3x5"

def test_plan_exercises_create(client, mock_response):
    """Verify scheduling an exercise in a day."""
    mock_response.json.return_value = {"id": 1, "workout_day_id": 5, "exercise_id": 3, "exercise_order": 1, "notes": "3x5"}
    with patch("requests.Session.post", return_value=mock_response):
        pe = client.plan_exercises.create(workout_day_id=5, exercise_id=3, exercise_order=1, notes="3x5")
        assert isinstance(pe, PlanExercise)
        assert pe.notes == "3x5"

def test_plan_exercises_update(client, mock_response):
    """Verify updating exercise scheduling."""
    mock_response.json.return_value = {"id": 1, "workout_day_id": 5, "exercise_id": 3, "exercise_order": 2, "notes": "4x5"}
    with patch("requests.Session.put", return_value=mock_response):
        pe = client.plan_exercises.update(plan_exercise_id=1, exercise_order=2, notes="4x5")
        assert pe.exercise_order == 2
        assert pe.notes == "4x5"

def test_plan_exercises_delete(client, mock_response):
    """Verify unscheduling an exercise."""
    mock_response.json.return_value = {"message": "PlanExercise deleted"}
    with patch("requests.Session.delete", return_value=mock_response):
        res = client.plan_exercises.delete(1)
        assert res["message"] == "PlanExercise deleted"