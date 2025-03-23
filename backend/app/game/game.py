from enum import Enum, auto
from random import shuffle

from .player import Player
from .models import Card, new_deck, CardSuit, Combo, ComboType

class GameState(Enum):
    PREGAME = auto()
    BIDDING = auto()
    GAMEPLAY = auto()
    GAMEOVER = auto()

    def __str__(self):
        return self.name.lower()

class InvalidStateError(Exception):
    pass

class InvalidTurnError(Exception):
    pass

class InvalidBidError(Exception):
    pass

class InvalidMoveError(Exception):
    pass

class Game:
    def __init__(self) -> None:
        self.gamestate: GameState = GameState.PREGAME
        self.players: list[Player] = []
        self.turn_ind: int = 0

        self.hands: dict[Player, list[Card]] = {}
        self.table_cards: list[Card] = []
        self.bids: dict[Player, int] = {}

        self.landlord: Player | None = None
        self.stake: int = 1

        self.last_turn: tuple[Player, Combo] | None = None
        self.last_played_combo_cards: list[Card] = []

        self.landlord_won: bool = False

    def add_player(self, player: Player) -> None:
        if self.gamestate != GameState.PREGAME:
            raise InvalidStateError("Cannot add a player when not in the pregame phase") 

        self.players.append(player)

        if len(self.players) == 3:
            self._start_bidding()

    def _start_bidding(self) -> None:
        self.gamestate = GameState.BIDDING

        self.bids.clear()
        
        self._deal_cards()
        self._set_starting_player()

    def _deal_cards(self) -> None:
        deck: list[Card] = new_deck()
        shuffle(deck)

        for player in self.players:
            hand = [deck.pop() for _ in range(17)]
            self.hands[player] = hand
        
        self.table_cards = deck  # last 3 cards for landlord

    def _set_starting_player(self) -> None:
        target_card: Card = Card("3", CardSuit.HEARTS)

        for alternate_card in [
            Card("3", CardSuit.DIAMONDS),
            Card("3", CardSuit.SPADES),
            Card("3", CardSuit.CLUBS),
        ]:
            if target_card in self.table_cards:
                target_card = alternate_card

        for player, hand in self.hands.items():
            if target_card in hand:
                self.turn_ind = self.players.index(player)
                return
    
    def _advance_turn(self) -> None:
        self.turn_ind += 1
        self.turn_ind %= 3

    def make_bid(self, player: Player, amount: int) -> None:
        if self.gamestate != GameState.BIDDING:
            raise InvalidStateError("Cannot make a bid when not in the bidding phase")

        if self.players[self.turn_ind] is not player:
            raise InvalidTurnError("It is not that players turn to bid")
        
        if not (0 <= amount <= 3):
            raise InvalidBidError("Must bid between 0 and 3. (0 to skip)")

        largest_bid = max(self.bids.values(), default=0)
        
        if amount > 0 and amount <= largest_bid:
            raise InvalidBidError("Must bid more than the max bid so far (or 0 to skip)")
        
        if amount > 0:
            self.bids[player] = amount

        self._advance_turn()

        self._check_bidding_finished()

    def _check_bidding_finished(self) -> None:
        largest_bidder, largest_bid = max(self.bids.items(), key=lambda item: item[1], default=(None, 0))

        if largest_bid == 3 or (
            largest_bidder is not None and self.players[self.turn_ind] == largest_bidder
        ):
            if largest_bid == 0:
                # restart bidding if nobody bid
                self.stake *= 2
                self._start_bidding()
            
            else:
                assert largest_bidder is not None
                self._start_gameplay(largest_bidder, largest_bid)

    def _start_gameplay(self, landlord: Player, stake: int) -> None:
        self.gamestate = GameState.GAMEPLAY

        self.landlord = landlord
        self.turn_ind = self.players.index(landlord)
        self.stake *= stake
    
        self.hands[self.landlord].extend(self.table_cards)
    
    def play_combo(self, player: Player, cards: list[Card]) -> None:
        if self.gamestate != GameState.GAMEPLAY:
            raise InvalidStateError("Cannot play a combo when not in the gameplay phase")

        if self.players[self.turn_ind] != player:
            raise InvalidTurnError("It is not that players turn to play")

        combo = Combo(cards)  # will propogate an error if invalid hand

        if self.last_turn:
            last_player, last_combo = self.last_turn
            if last_player != self.players[self.turn_ind] and not combo.beats(last_combo):
                raise InvalidMoveError("That is not a valid combo in this position")
        
        self.last_turn = player, combo
        self.last_played_combo_cards = cards

        if combo.type in [ComboType.BOMB, ComboType.ROCKET]:
            self.stake *= 2

        for card in cards:
            self.hands[player].remove(card)
        
        if not self.hands[player]:
            self._start_gameover(player)
            return

        self._advance_turn()

    def skip_play(self, player: Player) -> None:
        if self.gamestate != GameState.GAMEPLAY:
            raise InvalidStateError("Cannot play a combo when not in the gameplay phase")

        if self.players[self.turn_ind] != player:
            raise InvalidTurnError("It is not that players turn to play")

        if self.last_turn is None:
            raise InvalidMoveError("Cannot skip when it is that players turn to start the round")

        self._advance_turn()

        last_player, _ = self.last_turn

        if last_player == self.players[self.turn_ind]:
            # everyone else has skipped
            self.last_turn = None
            self.last_played_combo_cards = []

    def _assert_bidding_started(self, msg):
        if self.gamestate == GameState.PREGAME:
            raise InvalidStateError(msg)

    def _assert_gameplay_started(self, msg):
        if self.gamestate in [GameState.PREGAME, GameState.BIDDING]:
            raise InvalidStateError(msg)

    def get_hand(self, player: Player) -> list[Card]:
        self._assert_bidding_started("Bidding must have started for hands to have been dealt")
        return self.hands[player]

    def get_turn(self) -> Player:
        self._assert_bidding_started("Bidding must have started for turn to exist")
        return self.players[self.turn_ind]

    def get_landlord(self) -> Player:
        self._assert_gameplay_started("Landlord isn't selected before gameplay phase")
        assert self.landlord is not None
        return self.landlord

    def get_num_cards_left(self, player: Player) -> int:
        self._assert_gameplay_started("Can't query hand size until after game started")
        return len(self.hands[player])

    def get_table_cards(self) -> list[Card]:
        self._assert_gameplay_started("Can't query table cards until after game started")
        return self.table_cards

    def get_last_combo_cards(self) -> list[Card]:
        self._assert_gameplay_started("Can't query last combo until after game started")
        return self.last_played_combo_cards

    def get_bids(self) -> dict[Player, int]:
        self._assert_bidding_started("Can't query bids until after bidding started")
        return self.bids

    def get_stake(self) -> int:
        self._assert_gameplay_started("Can't query stake until after gameplay started")
        return self.stake

    def _start_gameover(self, winning_player: Player) -> None:
        self.gamestate = GameState.GAMEOVER

        if winning_player == self.landlord:
            self.landlord_won = True

    def get_payout(self, player: Player) -> int:
        if self.gamestate != GameState.GAMEOVER:
            raise InvalidStateError("Game hasn't ended so can't get payout")

        if player == self.landlord:
            if self.landlord_won:
                return 2 * self.stake
            else:
                return -2 * self.stake
        else:
            if self.landlord_won:
                return -1 * self.stake
            else:
                return self.stake
            