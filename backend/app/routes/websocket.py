from typing import Any

from fastapi import APIRouter, WebSocket
from ..game.player import Player

from .game_room import Room 

router = APIRouter()

class RoomManager:
    def __init__(self) -> None:
        self.rooms: dict[int, Room] = {}
        self.cur_room_id: int = 0
        self.rooms[self.cur_room_id] = Room(self.cur_room_id)

    def get_free_room(self) -> Room:
        if self.rooms[self.cur_room_id].is_full():
            self.cur_room_id += 1
            self.rooms[self.cur_room_id] = Room(self.cur_room_id)

        return self.rooms[self.cur_room_id]

room_manager = RoomManager()

# TODO validate player_id and generate if no id provided
@router.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await websocket.accept()

    # TODO get player name and authenticate
    player = Player("placeholder", int(player_id))

    room = room_manager.get_free_room()

    await room.player_connection(player, websocket)
