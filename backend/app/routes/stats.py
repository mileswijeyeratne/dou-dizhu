from fastapi import APIRouter
from uuid import UUID

from ..database import database, database_models

router = APIRouter()

@router.get("/player/{player_id}")
async def get_player(player_id):
    """Temporary endpoint to test db"""
    id = UUID(player_id)

    res = await database.fetchone(
        "SELECT * FROM players WHERE public_player_id = %s",
        (id.hex,),
        database_models.Player
    )
    
    print(res)

    return {"data": res}