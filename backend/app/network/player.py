from uuid import UUID, uuid4

from ..database import database, database_models

async def get_account_by_id(account_id: int) -> database_models.Account:
    account = await database.fetchone(
        "SELECT * FROM accounts WHERE account_id = %s",
        (account_id,),
        database_models.Account
    )

    if not account:
        raise ValueError("That account ID doesn't exist")

    return account


async def _new_player(*, name: str = "anonymous",  account_id: int | None = None) -> database_models.Player:
    public_player_id = uuid4()

    await database.execute(
        "INSERT INTO players (public_player_id, account_id, username) VALUES (%s, %s, %s)",
        (public_player_id, account_id, name)
    )

    return database_models.Player(-1, public_player_id, account_id, 0, name)

async def get_player_or_create(account_id: int) -> database_models.Player:
    player = await database.fetchone(
        "SELECT * FROM players WHERE account_id = %s",
        (account_id,),
        database_models.Player
    )

    if player:
        return player

    return await _new_player(account_id=account_id)

async def create_anonymous_player() -> database_models.Player:
    return await _new_player()
