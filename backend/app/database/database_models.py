from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass(slots=True)
class Account:
    account_id: int
    email: str
    password_hash: str
    created_at: datetime
    
@dataclass(slots=True)
class Player:
    player_id: int
    public_player_id: UUID
    account_id: int | None
    running_total: int
    username: str 

@dataclass(slots=True)
class PlayerPublic:
    public_player_id: UUID
    running_total: int
    username: str 

@dataclass(slots=True)
class Game:
    game_id: int
    room_id: UUID
    highest_bid: int
    stake: int
    landlord_id: int
    player_1_id: int
    player_2_id: int
    landlord_won: bool

@dataclass(slots=True)
class GamePublic:
    room_id: UUID
    highest_bid: int
    stake: int
    landlord_id: UUID
    player_1_id: UUID
    player_2_id: UUID
    landlord_won: bool