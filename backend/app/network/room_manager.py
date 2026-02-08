from random import choice

from ..game.player import Player
from .game_room import Room

class RoomManager:
    def __init__(self) -> None:
        self.public_rooms: dict[int, Room] = {}
        self.private_rooms: dict[str, Room] = {}
        self.cur_room_id: int = 0

    def _next_id(self) -> int:
        self.cur_room_id += 1
        return self.cur_room_id

    def _generate_room_code(self) -> str:
        chars = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]

        # check that code isn't in use
        code = ""
        while not code and code not in self.private_rooms.keys():
            code = "".join(choice(chars) for _ in range(6))

        return code

    def create_private_room(self) -> str:  # returns the room code
        code = self._generate_room_code()

        room = Room(self._next_id(), is_private=True, room_code=code)

        self.private_rooms[code] = room

        print("code is", code)

        return code

    def get_private_room(self, room_code: str) -> Room:
        room = self.private_rooms.get(room_code)
        if not room:
            raise ValueError("That room doesn't exist")
        if room.is_full():
            raise ValueError("That room is full")
        return room

    def get_room(self, player: Player) -> Room | None:
        # ts might be tapped bc player is deleted on disconnect
        for room in self.public_rooms.values():
            if player in room.game.players:
                return room
        for room in self.private_rooms.values():
            if player in room.game.players:
                return room
        return None

    def get_free_room(self) -> Room:
        for room in self.public_rooms.values():
            if not room.is_full() and not room.is_active_game():
                return room

        # otherwise no free room so make a new room
        id = self._next_id()
        room = Room(id)
        self.public_rooms[id] = room
        return room
