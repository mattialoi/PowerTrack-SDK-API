from unittest.mock import patch
from client.models import TrainingPlan

def test_plans_list(client, mock_response):
    """Verify plans list."""
    mock_response.json.return_value = [
        {"id": 10, "user_id": 1, "name": "Plan A", "total_weeks": 6, "start_date": "2026-05-29"}
    ]
    with patch("requests.Session.get", return_value=mock_response):
        plans = client.plans.list()
        assert len(plans) == 1
        assert isinstance(plans[0], TrainingPlan)
        assert plans[0].name == "Plan A"

def test_plans_get(client, mock_response):
    """Verify get single plan."""
    mock_response.json.return_value = {"id": 10, "user_id": 1, "name": "Plan A", "total_weeks": 6}
    with patch("requests.Session.get", return_value=mock_response):
        plan = client.plans.get(10)
        assert isinstance(plan, TrainingPlan)
        assert plan.id == 10

def test_plans_get_by_user(client, mock_response):
    """Verify get plans by user ID."""
    mock_response.json.return_value = [{"id": 10, "user_id": 1, "name": "Plan A", "total_weeks": 6}]
    with patch("requests.Session.get", return_value=mock_response):
        plans = client.plans.get_by_user(1)
        assert len(plans) == 1
        assert plans[0].user_id == 1

def test_plans_create(client, mock_response):
    """Verify plan creation."""
    mock_response.json.return_value = {"id": 10, "user_id": 1, "name": "Plan A", "total_weeks": 6}
    with patch("requests.Session.post", return_value=mock_response):
        plan = client.plans.create(user_id=1, name="Plan A", total_weeks=6)
        assert isinstance(plan, TrainingPlan)
        assert plan.name == "Plan A"

def test_plans_update(client, mock_response):
    """Verify plan update."""
    mock_response.json.return_value = {"id": 10, "user_id": 1, "name": "Updated Plan", "total_weeks": 8}
    with patch("requests.Session.put", return_value=mock_response):
        plan = client.plans.update(plan_id=10, name="Updated Plan", total_weeks=8)
        assert plan.name == "Updated Plan"
        assert plan.total_weeks == 8

def test_plans_delete(client, mock_response):
    """Verify plan deletion."""
    mock_response.json.return_value = {"message": "Plan deleted"}
    with patch("requests.Session.delete", return_value=mock_response):
        res = client.plans.delete(10)
        assert res["message"] == "Plan deleted"