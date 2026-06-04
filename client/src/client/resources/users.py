from __future__ import annotations
from client.models import User


class UsersAPI:
    """Sub-client for managing users."""

    def __init__(self, client):
        self.client = client

    def list(self) -> list[User]:
        """Return a list of all users."""
        return [User.from_dict(u, self.client) for u in self.client._get("/users/")]

    def get(self, user_id: int) -> User:
        """Return a single user by ID."""
        return User.from_dict(self.client._get(f"/users/{user_id}"), self.client)

    def create(self, username: str) -> User:
        """Create a new user."""
        return User.from_dict(self.client._post("/users/", {"username": username}), self.client)

    def delete(self, user_id: int) -> dict:
        """Delete a user and all associated data."""
        return self.client._delete(f"/users/{user_id}")