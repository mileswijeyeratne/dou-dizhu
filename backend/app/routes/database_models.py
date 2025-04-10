from dataclasses import dataclass
from uuid import UUID

@dataclass
class User:
    user_id: UUID
    running_total: int
    username: str | None