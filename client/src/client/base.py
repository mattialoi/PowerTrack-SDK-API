import logging
import requests
from client.exceptions import (
    PowerTrackAPIError,
    PowerTrackValidationError,
    PowerTrackNotFoundError,
    PowerTrackConflictError,
    PowerTrackServerError
)

# log configuration for the client library
logger = logging.getLogger("powertrack_client")
logger.addHandler(logging.NullHandler())


class BaseClient:
    """Base client handling HTTP connection, validation, and Context Manager lifecycle."""

    def __init__(self, base_url: str, timeout: int = 10):
        # pre validate the base URL to catch common mistakes early
        sanitized_url = base_url.strip()
        if not (sanitized_url.startswith("http://") or sanitized_url.startswith("https://")):
            logger.error(f"Initialization failed: Invalid URL scheme in '{base_url}'")
            raise ValueError("Base URL must start with 'http://' or 'https://'")

        self.base_url = sanitized_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        logger.info(f"Initialized PowerTrackClient with base URL: {self.base_url}")

    # support for Context Manager (with statement)
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self) -> None:
        """Close the underlying requests session to release system resources."""
        logger.info("Closing PowerTrackClient requests session")
        self.session.close()

    def _get(self, endpoint: str) -> dict | list:
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Sending GET request to {url}")
        try:
            response = self.session.get(url, timeout=self.timeout)
            logger.debug(f"Received GET response from {url} - Status: {response.status_code}")
            self._raise_for_error(response)
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Network error during GET request to {url}: {str(e)}")
            raise

    def _post(self, endpoint: str, data: dict) -> dict:
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Sending POST request to {url} with body: {data}")
        try:
            response = self.session.post(url, json=data, timeout=self.timeout)
            logger.debug(f"Received POST response from {url} - Status: {response.status_code}")
            self._raise_for_error(response)
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Network error during POST request to {url}: {str(e)}")
            raise

    def _put(self, endpoint: str, data: dict) -> dict:
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Sending PUT request to {url} with body: {data}")
        try:
            response = self.session.put(url, json=data, timeout=self.timeout)
            logger.debug(f"Received PUT response from {url} - Status: {response.status_code}")
            self._raise_for_error(response)
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Network error during PUT request to {url}: {str(e)}")
            raise

    def _delete(self, endpoint: str) -> dict:
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Sending DELETE request to {url}")
        try:
            response = self.session.delete(url, timeout=self.timeout)
            logger.debug(f"Received DELETE response from {url} - Status: {response.status_code}")
            self._raise_for_error(response)
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Network error during DELETE request to {url}: {str(e)}")
            raise

    def _raise_for_error(self, response: requests.Response) -> None:
        """Map HTTP status codes to specialized PowerTrack exception classes."""
        if response.status_code >= 400:
            try:
                message = response.json().get("error", response.text)
            except Exception:
                message = response.text

            logger.warning(f"Request failed - URL: {response.url} | Status: {response.status_code} | Error: {message}")

            if response.status_code == 400:
                raise PowerTrackValidationError(response.status_code, message)
            elif response.status_code == 404:
                raise PowerTrackNotFoundError(response.status_code, message)
            elif response.status_code == 409:
                raise PowerTrackConflictError(response.status_code, message)
            elif response.status_code >= 500:
                raise PowerTrackServerError(response.status_code, message)
            else:
                raise PowerTrackAPIError(response.status_code, message)

    def ping(self) -> bool:
        """Check if the PowerTrack backend is reachable."""
        try:
            self._get("/")
            return True
        except Exception:
            return False