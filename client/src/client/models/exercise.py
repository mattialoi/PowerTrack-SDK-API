from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class Exercise:
    id: int
    name: str
    mechanics_type: str
    target_muscle: str
    _client: Optional[Any] = field(default=None, repr=False, compare=False, hash=False)

    @classmethod
    def from_dict(cls, data: dict, client: Optional[Any] = None) -> "Exercise":
        return cls(
            id=data["id"],
            name=data["name"],
            mechanics_type=data["mechanics_type"],
            target_muscle=data["target_muscle"],
            _client=client
        )

    def get_personal_best(self, user_id: int) -> dict:
        """Get a user's personal record weight for this exercise."""
        if not self._client:
            raise RuntimeError("Client not bound to this model instance")
        return self._client.stats.get_personal_best(user_id, self.id)