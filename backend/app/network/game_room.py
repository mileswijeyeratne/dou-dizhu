from typing import Any

from ..game.player import Player
from ..game.game import Game, GameState, InvalidStateError, InvalidBidError, InvalidTurnError, InvalidMoveError
from ..game.models import Card, InvalidComboError

from ..database import database

from fastapi import WebSocket, WebSocketDisconnect

class Room:
    def __init__(self, id: int, *, is_private: bool = False, room_code: str = "") -> None:
        self.is_private: bool = is_private 
        self.room_code: str = room_code

        self.id: int = id
        self.connections: dict[Player, WebSocket] = {}
        self.game: Game = Game()

        print(f"[Room {self.id}] Room created" + (f" with code {self.room_code}" if self.is_private else ""))

    def is_full(self) -> bool:
        return len(self.connections) >= 3

    def is_active_game(self) -> bool:
        return self.game.gamestate != GameState.PREGAME
    
    async def broadcast(self, msg: dict[Any, Any], /, exclude: Player | None = None):
        for player, conn in self.connections.items():
            if player is exclude:
                continue
            await conn.send_json(msg)

    async def player_connection(self, player: Player, websocket: WebSocket) -> None:
        print(f"[ROOM {self.id}] [Player {player.id}] connected")
        self.connections[player] = websocket

        await websocket.send_json({
            "room_type": "public",
        } if not self.is_private else {
            "room_type": "private",
            "room_code": self.room_code
        })

        if player not in self.game.players:
            self.game.add_player(player)

        await self.send_state()

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
            try:
                if action == "bid":
                    amount = data.get("amount", 0)
                    try:
                        self.game.make_bid(player, amount)
                    except InvalidBidError:
                        await websocket.send_json({"error": "invalid-bid"})

                if action == "play":
                    cards = []
                    for card in data.get("cards", []):
                        cards.append(Card.from_object(card))

                    try:
                        self.game.play_combo(player, cards)

                        if self.game.gamestate == GameState.GAMEOVER:
                            await self.handle_gameover()
                            # maybe need to return to stop the state being sent (line 86)

                    except InvalidComboError:
                        await websocket.send_json({"error": "invalid-combo"})
                
                if action == "skip":
                    self.game.skip_play(player)
            
            except InvalidStateError:
                await websocket.send_json({"error": "invalid-state"})
            
            except InvalidTurnError:
                await websocket.send_json({"error": "invalid-turn"})
            
            except InvalidMoveError:
                await websocket.send_json({"error": "invalid-move"})
            
        await self.send_state()

    async def handle_gameover(self):
        # send gameover to clients
        await self.broadcast({
            "action": "update-state",
            "state": {"gamePhase": str(GameState.GAMEOVER)},
        })
        
        # store result in database
        landlord = self.game.landlord
        assert landlord is not None, "something went wrong"
        p1, p2 = [p for p in self.game.players if p is not landlord]
        print(landlord, p1, p2)

        database.execute(
            "INSERT INTO games (room_id, highest_bid, stake, landlord_id, player_1_id, player_2_id, landlowrd_won) VALUES (%s, %s, %s, %s, %s, %s)",
            (self.id, max(self.game.get_bids.values()), self.game.stake, landlord.id, p1.id, p2.id, self.game.landlord_won),
        )

        for player in [landlord, p1, p2]:
            database.execute(
                "UPDATE players SET running_total = running_total + %s WHERE public_player_id = %s",
                (self.game.get_payout(player), player.id)
            )

        # reset room
        # - close ws (client to display a play again option)
        # - just reset room if its private
        if self.is_private:
            self.game.restart_game()

        else:
            for conn in self.connections.values():
                conn.close(reason="gameover")

        print(f"[ROOM {self.id}] gameover")

    async def send_state(self):
        # i.e should prob send diff rather than state every time
        # doesn't seem too slow atm
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
        for c in sorted(cards, reverse=True):
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