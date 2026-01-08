from typing import Any

from uuid import UUID

class Player:
    def __init__(self, id: UUID, name: str):
        self.name: str = name 
        self.id: UUID = id

    def __eq__(self, other: Any):
        if not isinstance(other, Player):
            raise NotImplementedError()

        return other.id == self.id

    def __str__(self):
        return f"Player<name: {self.name} id: {self.id}>"

    def __hash__(self):
        return hash(self.id)
