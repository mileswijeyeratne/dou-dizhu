from typing import Any

from fastapi import APIRouter, WebSocket
from uuid import UUID, uuid4
from contextlib import asynccontextmanager
from random import choice

from ..game.player import Player
from .game_room import Room 
from .database import Database
from . import database_models

database = Database()

@asynccontextmanager
async def lifespan(router: APIRouter):
    await database.open_pool()
    # TODO: put this here when restructuing websocket enpoint
    # room_manager = RoomManager()

    yield

    await database.close_pool()


router = APIRouter(lifespan=lifespan)

class RoomManager:
    def __init__(self) -> None:
        self.public_rooms: dict[int, Room] = {}
        self.private_rooms: dict[str, Room] = {}
        self.cur_room_id: int = 0

    def _next_id(self) -> int:
        self.cur_room_id += 1
        return self.cur_room_id

    def generate_room_code(self) -> str:
        chars = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]

        # check that code isn't in use
        code = ""
        while code and code not in self.private_rooms.keys():
            code = "".join(choice(chars) for _ in range(6))

        return code

    def create_private_room(self) -> str:  # returns the room code
        code = self.generate_room_code()

        room = Room(self._next_id(), is_private=True, room_code=code)

        self.private_rooms[code] = room

        return code

    def get_room(self, player: Player) -> Room | None:
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


room_manager = RoomManager()

@router.websocket("/ws/{player_id}")
async def websocket_endpoint_with_id(websocket: WebSocket, player_id: str):
    await websocket.accept()
    await handle_websocket_endpoint(websocket, player_id)

@router.websocket("/ws")
async def websocket_endpoint_without_id(websocket: WebSocket):
    await websocket.accept()
    id = str(uuid4())
    await websocket.send_json({"id": id})
    await handle_websocket_endpoint(websocket, id)

async def handle_websocket_endpoint(websocket: WebSocket, player_id: str):
    # TODO authenticate
    player = Player(UUID(player_id))

    room = room_manager.get_room(player) or room_manager.get_free_room()

    await room.player_connection(player, websocket)

@router.get("/player/{player_id}")
async def get_player(player_id):
    """Temporary endpoint to test db"""
    id = UUID(player_id)

    res = await database.fetchone(
        "SELECT * FROM users WHERE user_id = %s",
        (id,),
        database_models.User
    )
    
    print(res)

    return {"data": res}