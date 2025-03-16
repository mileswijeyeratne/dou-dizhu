from typing import Any

class Player:
    def __init__(self, name: str, id: int):
        self.name: str = name
        self.id: int = id

    def __eq__(self, other: Any):
        if not isinstance(other, Player):
            raise NotImplementedError()

        return other.id == self.id
