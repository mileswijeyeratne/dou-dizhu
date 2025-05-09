from typing import Any

from fastapi import APIRouter, WebSocket
from uuid import UUID, uuid4
from contextlib import asynccontextmanager

from ..game.player import Player
from .game_room import Room 
from .database import Database
from . import database_models

database = Database()

@asynccontextmanager
async def lifespan(router: APIRouter):
    await database.open_pool()

    yield

    await database.close_pool()


router = APIRouter(lifespan=lifespan)

class RoomManager:
    def __init__(self) -> None:
        self.rooms: dict[int, Room] = {}
        self.cur_room_id: int = 0
        self.rooms[self.cur_room_id] = Room(self.cur_room_id)

    def get_room(self, player: Player) -> Room | None:
        for room in self.rooms.values():
            if player in room.game.players:
                return room
        return None

    def get_free_room(self) -> Room:
        if self.rooms[self.cur_room_id].is_full():
            self.cur_room_id += 1
            self.rooms[self.cur_room_id] = Room(self.cur_room_id)

        return self.rooms[self.cur_room_id]

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