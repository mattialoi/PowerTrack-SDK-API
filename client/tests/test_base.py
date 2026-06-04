from unittest.mock import patch
import pytest
import requests
from client.client import PowerTrackClient
from client.exceptions import (
    PowerTrackValidationError,
    PowerTrackNotFoundError,
    PowerTrackConflictError,
    PowerTrackServerError,
    PowerTrackAPIError
)

def test_invalid_url_schema():
    """Verify that initialization fails with invalid schemes."""
    with pytest.raises(ValueError, match="Base URL must start with"):
        PowerTrackClient("127.0.0.1:8000")

def test_context_manager():
    """Verify context manager correctly closes session."""
    with patch("requests.Session.close") as mock_close:
        with PowerTrackClient("http://127.0.0.1:8000") as pt_client:
            assert pt_client.base_url == "http://127.0.0.1:8000"
        mock_close.assert_called_once()

def test_ping_success(client, mock_response):
    """Verify ping returns True on success."""
    mock_response.json.return_value = {"message": "online"}
    with patch("requests.Session.get", return_value=mock_response):
        assert client.ping() is True

def test_ping_failure(client):
    """Verify ping returns False on connection errors."""
    with patch("requests.Session.get", side_effect=requests.RequestException()):
        assert client.ping() is False

@pytest.mark.parametrize(
    "status_code,exception_cls",
    [
        (400, PowerTrackValidationError),
        (404, PowerTrackNotFoundError),
        (409, PowerTrackConflictError),
        (500, PowerTrackServerError),
        (418, PowerTrackAPIError),
    ],
)
def test_exception_mapping(client, mock_response, status_code, exception_cls):
    """Verify HTTP status codes map to the correct custom exceptions."""
    mock_response.status_code = status_code
    mock_response.json.return_value = {"error": "Test error message"}
    
    with patch("requests.Session.get", return_value=mock_response):
        with pytest.raises(exception_cls) as exc_info:
            client.users.list()
        assert exc_info.value.status_code == status_code
        assert "Test error message" in str(exc_info.value)