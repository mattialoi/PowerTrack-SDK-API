from unittest.mock import patch
from client.models import (
    ExerciseVolumeReport,
    WeeklyVolumeReport,
    WeeklyRpeReport,
    PainReport,
    MuscleBalanceReport
)

def test_stats_volume_by_exercise(client, mock_response):
    """Verify stats volume returns ExerciseVolumeReport."""
    mock_response.json.return_value = {"plan_exercise_id": 1, "exercise": "Squat", "data": [{"week_number": 1, "sets": 3, "reps": 5, "weight": 100.0, "volume": 1500.0}]}
    with patch("requests.Session.get", return_value=mock_response):
        rep = client.stats.get_volume_by_exercise(1)
        assert isinstance(rep, ExerciseVolumeReport)
        assert rep.exercise == "Squat"

def test_stats_multijoint_volume(client, mock_response):
    """Verify multijoint volume report."""
    mock_response.json.return_value = {"plan_id": 10, "mechanics_type": "Multi-joint", "data": [{"week_number": 1, "total_volume": 3000.0}]}
    with patch("requests.Session.get", return_value=mock_response):
        rep = client.stats.get_multijoint_volume(10)
        assert isinstance(rep, WeeklyVolumeReport)
        assert rep.mechanics_type == "Multi-joint"

def test_stats_total_volume(client, mock_response):
    """Verify total volume report."""
    mock_response.json.return_value = {"plan_id": 10, "data": [{"week_number": 1, "total_volume": 5000.0}]}
    with patch("requests.Session.get", return_value=mock_response):
        rep = client.stats.get_total_volume(10)
        assert isinstance(rep, WeeklyVolumeReport)
        assert rep.data[0].total_volume == 5000.0

def test_stats_avg_rpe(client, mock_response):
    """Verify weekly average RPE report."""
    mock_response.json.return_value = {"plan_id": 10, "data": [{"week_number": 1, "avg_rpe": 7.5, "sessions_logged": 3}]}
    with patch("requests.Session.get", return_value=mock_response):
        rep = client.stats.get_avg_rpe(10)
        assert isinstance(rep, WeeklyRpeReport)
        assert rep.data[0].avg_rpe == 7.5

def test_stats_pain_report(client, mock_response):
    """Verify weekly pain/discomfort flags timeline."""
    mock_response.json.return_value = {"plan_id": 10, "total_pain_flags": 1, "data": [{"week_number": 3, "exercise": "Leg Extensions", "rpe": 6, "user_feedback": "knee"}]}
    with patch("requests.Session.get", return_value=mock_response):
        rep = client.stats.get_pain_report(10)
        assert isinstance(rep, PainReport)
        assert rep.total_pain_flags == 1

def test_stats_muscle_balance(client, mock_response):
    """Verify volume breakdown by muscle group."""
    mock_response.json.return_value = {"plan_id": 10, "total_volume": 10000.0, "data": [{"target_muscle": "Chest", "total_volume": 4000.0, "percentage": 40.0}]}
    with patch("requests.Session.get", return_value=mock_response):
        rep = client.stats.get_muscle_balance(10)
        assert isinstance(rep, MuscleBalanceReport)
        assert rep.total_volume == 10000.0

def test_stats_personal_best(client, mock_response):
    """Verify personal best weight extraction."""
    mock_response.json.return_value = {"user_id": 1, "exercise_id": 3, "max_weight": 140.0, "reps_at_max": 5, "week_achieved": 4}
    with patch("requests.Session.get", return_value=mock_response):
        pb = client.stats.get_personal_best(1, 3)
        assert isinstance(pb, dict)
        assert pb["max_weight"] == 140.0
        assert pb["reps_at_max"] == 5
        assert pb["week_achieved"] == 4