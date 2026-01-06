from fastapi import APIRouter, WebSocket
from uuid import UUID, uuid4

from ..game.player import Player
from ..network.room_manager import RoomManager

room_manager = RoomManager()
router = APIRouter()

@router.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await websocket.accept()
    player = Player(UUID(player_id))

    room = room_manager.get_room(player) or room_manager.get_free_room()

    await room.player_connection(player, websocket)

# TODO remove this when adding auth
@router.websocket("/ws")
async def websocket_endpoint_without_id(websocket: WebSocket):
    await websocket.accept()
    print("lmao they tried to connect")
    id = str(uuid4())
    await websocket.send_json({"id": id})
    await websocket.close()
