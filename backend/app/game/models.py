from __future__ import annotations

from enum import Enum

class CardSuit(Enum):
    HEARTS = "H"
    DIAMONDS = "D"
    CLUBS = "C"
    SPADES = "S"

CARD_RANK_ORDER = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2"]

class Card:
    def __init__(self, rank: str, suit: CardSuit):
        self.rank: str = rank
        self.suit: CardSuit = suit
        self.is_joker: bool = False

    def __repr__(self):
        return f"{self.rank} of {self.suit.value}"

class Joker(Card):
    def __init__(self, *, is_big: bool):
        super().__init__("2", CardSuit.HEARTS)
        self.is_joker = True
        self.is_big: bool = is_big

    def __repr__(self):
        return f"{"Big" if self.is_big else "Small"} Joker"

class HandType(Enum):
    SINGLE = 0
    PAIR = 1
    TRIPLET = 2
    TRIPLET_WITH_SINGLE = 3
    TRIPLET_WITH_PAIR = 4
    SEQUENCE = 5
    SEQUENCE_OF_PAIRS = 6
    SEQUENCE_OF_TRIPLETS = 7
    SEQUENCE_OF_TRIPLETS_WITH_SINGLES = 8
    SEQUENCE_OF_TRIPLETS_WITH_PAIRS = 9
    QUADPLEX_WITH_SINGLES = 10
    QUADPLEX_WITH_PAIRS = 11
    BOMB = 12
    ROCKET = 13

class Hand:
    def __init__(self, cards: list[Card]):
        self.rank: str = "3"
        self.type: HandType = HandType.SINGLE
        self._score_hand(cards)
    
    def _score_hand(self, cards: list[Card]) -> None:
        raise NotImplementedError

    def beats(self, other: Hand) -> bool:
        raise NotImplementedError