from fastapi import APIRouter
from uuid import UUID

from ..database import database, database_models
from ..game.game import Game

router = APIRouter()

@router.get("/player/{player_id}")
async def get_player(player_id: UUID):
    res = await database.fetchone(
        "SELECT public_player_id, running_total, username FROM players WHERE public_player_id = %s",
        # "SELECT * FROM players WHERE public_player_id = %s",
        (player_id.hex,),
        database_models.PlayerPublic
    )
    
    return {"data": res}

@router.get("/game/{room_id}")
async def get_games(room_id: UUID):
    res = await database.fetchall(
        "SELECT room_id, highest_bid, stake, landlord_id, player_1_id, player_2_id, landlord_won FROM games WHERE room_id = %s",
        # "SELECT * FROM games WHERE room_id = %s",
        (room_id.hex,),
        database_models.GamePublic
    )

    return {"data": res}

get_history_query = ""
# with open("./queries/history.sql") as f:
#     get_history_query = f.read()

async def _get_history(player_1: UUID, player_2: UUID, player_3: UUID) -> list[database_models.GamePublic]:
    return await database.fetchall(
        get_history_query,
        (player_1, player_2, player_3),
        database_models.GamePublic
    )

@router.get("/history/{player_1}/{player_2}/{player_3}")
async def get_history(player_1: UUID, player_2: UUID, player_3: UUID):
    res = await _get_history(player_1, player_2, player_3)

    return {"data": res}

@router.get("/total/{player_1}/{player_2}/{player_3}")
async def get_total(player_1: UUID, player_2: UUID, player_3: UUID):
    games = await _get_history(player_1, player_2, player_3)
    
    res = {player_1: 0, player_2: 0, player_3: 0}

    for game in games:
        for player in res:
            res[player] += Game.calculate_payout(game.landlord_id == player, game.landlord_won, game.stake)

    return {"data": res}
