from unittest.mock import patch
import pytest
from client.models import User, TrainingPlan, WorkoutDay, Exercise, PlanExercise, SessionLog

def test_active_record_user(client, mock_response):
    """Test user active record methods."""
    user = User(id=1, username="marco", _client=client)
    mock_response.json.return_value = [{"id": 10, "user_id": 1, "name": "Plan A", "total_weeks": 6}]
    with patch("requests.Session.get", return_value=mock_response):
        plans = user.get_plans()
        assert len(plans) == 1
        assert plans[0].id == 10

def test_active_record_plan(client, mock_response):
    """Test training plan active record methods."""
    plan = TrainingPlan(id=10, user_id=1, name="Plan A", total_weeks=6, _client=client)
    
    mock_response.json.return_value = [{"id": 5, "plan_id": 10, "name": "Push", "day_order": 1}]
    with patch("requests.Session.get", return_value=mock_response):
        days = plan.get_days()
        assert len(days) == 1
        assert days[0].name == "Push"

def test_active_record_day(client, mock_response):
    """Test workout day active record methods."""
    day = WorkoutDay(id=5, plan_id=10, name="Push", day_order=1, _client=client)
    mock_response.json.return_value = [{"id": 1, "workout_day_id": 5, "exercise_id": 3, "exercise_order": 1}]
    with patch("requests.Session.get", return_value=mock_response):
        exs = day.get_exercises()
        assert len(exs) == 1

def test_active_record_exercise(client, mock_response):
    """Test exercise active record methods."""
    ex = Exercise(id=3, name="Squat", mechanics_type="Multi-joint", target_muscle="Legs", _client=client)
    mock_response.json.return_value = {"user_id": 1, "exercise_id": 3, "max_weight": 140.0, "reps_at_max": 5}
    with patch("requests.Session.get", return_value=mock_response):
        pb = ex.get_personal_best(1)
        assert pb["max_weight"] == 140.0

def test_active_record_plan_exercise(client, mock_response):
    """Test plan exercise active record methods."""
    pe = PlanExercise(id=1, workout_day_id=5, exercise_id=3, exercise_order=1, _client=client)
    
    mock_response.json.return_value = [{"id": 20, "plan_exercise_id": 1, "week_number": 1, "sets": 3, "reps": 5, "weight": 100.0}]
    with patch("requests.Session.get", return_value=mock_response):
        logs = pe.get_logs()
        assert len(logs) == 1

    mock_response.json.return_value = {"plan_exercise_id": 1, "exercise": "Squat", "data": []}
    with patch("requests.Session.get", return_value=mock_response):
        vol = pe.get_volume_progression()
        assert vol.exercise == "Squat"