from dataclasses import dataclass, field
from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from client.models.plan import TrainingPlan


@dataclass
class User:
    id: int
    username: str
    _client: Optional[Any] = field(default=None, repr=False, compare=False, hash=False)

    @classmethod
    def from_dict(cls, data: dict, client: Optional[Any] = None) -> "User":
        return cls(id=data["id"], username=data["username"], _client=client)

    def get_plans(self) -> list["TrainingPlan"]:
        """Retrieve all training plans for this user directly from the model."""
        if not self._client:
            raise RuntimeError("Client not bound to this model instance")
        return self._client.plans.get_by_user(self.id)