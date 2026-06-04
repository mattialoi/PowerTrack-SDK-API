class PowerTrackAPIError(Exception):
    """Base exception for all PowerTrack API errors."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")


class PowerTrackValidationError(PowerTrackAPIError):
    """Raised when the API returns a 400 Bad Request."""
    pass


class PowerTrackNotFoundError(PowerTrackAPIError):
    """Raised when the API returns a 404 Not Found."""
    pass


class PowerTrackConflictError(PowerTrackAPIError):
    """Raised when the API returns a 409 Conflict."""
    pass


class PowerTrackServerError(PowerTrackAPIError):
    """Raised when the API returns a 5xx Server Error."""
    pass