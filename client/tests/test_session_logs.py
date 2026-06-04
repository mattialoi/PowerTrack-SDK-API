from unittest.mock import patch
from client.models import SessionLog

def test_session_logs_get_by_exercise(client, mock_response):
    """Verify retrieving session logs for a scheduled exercise."""
    mock_response.json.return_value = [{"id": 20, "plan_exercise_id": 1, "week_number": 1, "sets": 3, "reps": 5, "weight": 100.0}]
    with patch("requests.Session.get", return_value=mock_response):
        logs = client.session_logs.get_by_exercise(1)
        assert len(logs) == 1
        assert isinstance(logs[0], SessionLog)

def test_session_logs_get(client, mock_response):
    """Verify retrieving a single log."""
    mock_response.json.return_value = {"id": 20, "plan_exercise_id": 1, "week_number": 1, "sets": 3, "reps": 5, "weight": 100.0}
    with patch("requests.Session.get", return_value=mock_response):
        log = client.session_logs.get(20)
        assert isinstance(log, SessionLog)
        assert log.id == 20

def test_session_logs_create(client, mock_response):
    """Verify logging a workout set."""
    mock_response.json.return_value = {"id": 20, "plan_exercise_id": 1, "week_number": 1, "sets": 3, "reps": 5, "weight": 100.0}
    with patch("requests.Session.post", return_value=mock_response):
        log = client.session_logs.create(plan_exercise_id=1, week_number=1, sets=3, reps=5, weight=100.0)
        assert isinstance(log, SessionLog)
        assert log.weight == 100.0

def test_session_logs_update(client, mock_response):
    """Verify updating a logged set."""
    mock_response.json.return_value = {"id": 20, "plan_exercise_id": 1, "week_number": 1, "sets": 4, "reps": 5, "weight": 102.5}
    with patch("requests.Session.put", return_value=mock_response):
        log = client.session_logs.update(log_id=20, sets=4, weight=102.5)
        assert log.sets == 4
        assert log.weight == 102.5

def test_session_logs_delete(client, mock_response):
    """Verify deleting a log entry."""
    mock_response.json.return_value = {"message": "SessionLog deleted"}
    with patch("requests.Session.delete", return_value=mock_response):
        res = client.session_logs.delete(20)
        assert res["message"] == "SessionLog deleted"