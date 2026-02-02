from fastapi import APIRouter, WebSocket

from ..game.player import Player
from ..network.game_room import Room
from ..network.room_manager import RoomManager
from ..network.player import get_player_or_create, create_anonymous_player, get_account_by_id
from ..database import database_models
from .auth import verify_jwt_token

room_manager = RoomManager()
router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    print(websocket.cookies)

    # get jwt token
    token = websocket.cookies.get("jwt_token")
    account: database_models.Account | None = None

    # verify jwt token
    if token:
        account_id = verify_jwt_token(token)
        if account_id:
            account = await get_account_by_id(account_id)
        # else there was no valid jwt token

    # handshake includes guest and private room info
    handshake = await websocket.receive_json()
    is_guest = handshake.get("is_guest", False)
    room_code = handshake.get("room_code")

    if not account and not is_guest:
        # this is not allowed (cannot have anonymous non-guest) TODO
        print("no account")
        await websocket.close()
        return

    # create player
    player_model: database_models.Player = await get_player_or_create(account.account_id) if account else await create_anonymous_player()
    player = Player(player_model.public_player_id, player_model.username)

    # find a room
    room: Room | None = None
    if room_code:
        try:
            room = room_manager.get_private_room(room_code)
        except ValueError as e:
            print("no code")
            # TODO send error to client
            await websocket.close()
            return
    else: 
        room = room_manager.get_room(player) or room_manager.get_free_room()

    await room.player_connection(player, websocket)
