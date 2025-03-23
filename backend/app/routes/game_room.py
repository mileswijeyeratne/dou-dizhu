from typing import Any

from ..game.player import Player
from ..game.game import Game, InvalidStateError, InvalidBidError
from ..game.models import Card, InvalidComboError

from fastapi import WebSocket, WebSocketDisconnect

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

        if player not in self.game.players:
            self.game.add_player(player)

        while True:
            try:
                data = await websocket.receive_json()
                await self.handle_message(data, player, websocket)

            except WebSocketDisconnect:
                await self.handle_disconnect(player)
                return

    async def handle_message(self, data: dict[Any, Any], player: Player, websocket: WebSocket) -> None:
        print(f"[ROOM {self.id}] [Player {player.id}] {data}")

        if name := data.get("name"):
            player.name = name

        if action := data.get("action"):
            if action == "bid":
                amount = data.get("amount", 0)
                try:
                    self.game.make_bid(player, amount)
                except InvalidBidError:
                    await websocket.send_json({"error": "invalid-bid"})

            if action == "play":
                cards = []
                for card in data.get("cards", []):
                   cards.append(Card(card["rank"], card["suit"])) 

                try:
                    self.game.play_combo(player, cards)
                except InvalidComboError:
                    await websocket.send_json({"error": "invalid-combo"})

        # TODO move out of here
        await self.broadcast({
            "action": "update-state",
            "state": self.get_game_state(),
        })
        await self.send_player_hands()

    async def send_player_hands(self):
        for player, conn in self.connections.items():
            try:
                await conn.send_json({
                    "action": "update-hand",
                    "hand": self.cards_to_object(self.game.get_hand(player))
                })
            except InvalidStateError:
                pass

    def cards_to_object(self, cards: list[Card]) -> list[dict[Any, Any]]:
        res = []
        for c in cards:
            res.append(c.to_object())
        return res

    def get_game_state(self) -> dict[Any, Any]:
        state = {
            "gameId": self.id,
            "gamePhase": str(self.game.gamestate),
            "players": list(map(lambda p: {"playerId": str(p.id), "name": p.name}, self.game.players)),
        }

        # needs bidding
        try:
            state.update({
                "currentPlayerTurnId": str(self.game.get_turn().id),
                "bids": {str(p.id): b for p, b in self.game.get_bids().items()}
            })
        except InvalidStateError:
            pass

        # needs game started
        try:
            state.update({
                "stake": self.game.get_stake(),
                "numberOfCards": {str(p.id): self.game.get_num_cards_left(p) for p in self.game.players},
                "landlordId": str(self.game.get_landlord().id),
                "tableCards": self.cards_to_object(self.game.get_table_cards()),
                "lastPlayedCombo": self.cards_to_object(self.game.get_last_combo_cards()),
            })
        except InvalidStateError:
            pass

        return state

    async def handle_disconnect(self, player: Player) -> None:
        print(f"[ROOM {self.id}] [Player {player.id}] disconnected")
        del self.connections[player] 