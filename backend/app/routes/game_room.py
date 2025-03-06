from typing import Any

from ..game.player import Player
from ..game.game import Game

from fastapi import WebSocket, WebSocketDisconnect, APIRouter

class Room:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.connections: dict[Player, WebSocket] = {}
        self.game: Game = Game()

    def is_full(self) -> bool:
        return len(self.connections) >= 3
    
    async def broadcast(self, msg: dict[Any, Any], /, exclude: Player | None = None):
        for player, conn in self.connections.items():
            if player is exclude:
                continue
            await conn.send_json(msg)

    async def player_connection(self, player: Player, websocket: WebSocket) -> None:
        print(f"[ROOM {self.id}] [Player {player.id}] connected")
        self.connections[player] = websocket
        self.game.add_player(player)

        while True:
            try:
                data = await websocket.receive_json()
                await self.handle_message(data, player, websocket)

            except WebSocketDisconnect:
                await self.handle_disconnect(player)

    async def handle_message(self, data: dict[Any, Any], player: Player, websocket: WebSocket) -> None:
        print(f"[ROOM {self.id}] [Player {player.id}] {data}")
        pass

    async def handle_disconnect(self, player: Player) -> None:
        print(f"[ROOM {self.id}] [Player {player.id}] disconnected")
        pass