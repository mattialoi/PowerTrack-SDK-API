import matplotlib
matplotlib.use("Agg")
from unittest.mock import MagicMock
import pytest
import requests
from client.client import PowerTrackClient

@pytest.fixture
def mock_response():
    """Fixture to create a mock HTTP response."""
    response = MagicMock(spec=requests.Response)
    response.status_code = 200
    response.url = "http://127.0.0.1:8000"
    return response

@pytest.fixture
def client():
    """Fixture to initialize a client instance."""
    return PowerTrackClient("http://127.0.0.1:8000")