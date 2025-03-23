from __future__ import annotations

from typing import Iterable

from enum import Enum
from collections import defaultdict

class CardSuit(Enum):
    HEARTS = "H"
    DIAMONDS = "D"
    CLUBS = "C"
    SPADES = "S"

CARD_RANK_ORDER = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2", "SJ", "BJ"]

class Card:
    def __init__(self, rank: str, suit: CardSuit):
        self.rank: str = rank
        self.suit: CardSuit = suit
        self.is_joker: bool = False

    def __repr__(self):
        return f"{self.rank} of {self.suit.value}"

    def __eq__(self, other: object):
        if not isinstance(other, Card):
            raise NotImplementedError
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other: object):
        if not isinstance(other, Card):
            raise NotImplementedError
        return CARD_RANK_ORDER.index(self.rank) < CARD_RANK_ORDER.index(other.rank)

    def to_object(self) -> dict[str, str]:
        rank = self.rank
        if self.rank == "SJ": rank = "small"
        if self.rank == "BJ": rank = "big"
        return {
            "rank": rank,
            "suit": self.suit.name.lower() if not self.is_joker else "joker"
        }

    @staticmethod
    def from_object(card: dict[str, str]) -> Card:
        suit = card["suit"]
        rank = card["rank"]

        match suit:
            case "joker":
                if rank == "big":
                    return Joker(is_big=True)
                else:
                    return Joker(is_big=False)
            case "hearts":
                return Card(rank, CardSuit.HEARTS)
            case "diamonds":
                return Card(rank, CardSuit.DIAMONDS)
            case "clubs":
                return Card(rank, CardSuit.CLUBS)
            case "spades":
                return Card(rank, CardSuit.SPADES)
            case _:
                raise ValueError(f"Cannot create a card from the object: {card}")
        
class Joker(Card):
    def __init__(self, *, is_big: bool):
        super().__init__("BJ" if is_big else "SJ", CardSuit.HEARTS)
        self.is_joker = True
        self.is_big: bool = is_big

    def __repr__(self):
        return f"{"Big" if self.is_big else "Small"} Joker"

    def __eq__(self, other: object):
        if not isinstance(other, Card):
            raise NotImplementedError
        if not isinstance(other, Joker):
            return False
        return self.is_big == other.is_big
    
    def __lt__(self, other: object):
        if not isinstance(other, Card):
            raise NotImplementedError
        if not isinstance(other, Joker):
            return False
        return self.is_big and not other.is_big

def new_deck() -> list[Card]:
    deck: list[Card] = []

    for suit in [
        CardSuit.HEARTS,
        CardSuit.DIAMONDS,
        CardSuit.CLUBS,
        CardSuit.SPADES,
    ]:
        for rank in CARD_RANK_ORDER:
            if rank in ["SJ", "BJ"]:
                continue
            deck.append(Card(rank, suit))

    deck.append(Joker(is_big=False))
    deck.append(Joker(is_big=True))

    return deck

class ComboType(Enum):
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

class InvalidComboError(Exception):
    """Raised when cards passed to a `Hand` constructor do not form a valid hand"""
    pass

class Combo:
    def __init__(self, cards: list[Card]):
        self.rank: str = ""
        self.type: ComboType = ComboType.SINGLE
        self.sequence_length: int | None = None
        self._score_hand(cards)

    @staticmethod
    def is_straight(ranks: Iterable[str]):
        rank_order_indicies: list[int] = sorted(map(lambda rank: CARD_RANK_ORDER.index(rank), ranks))

        if rank_order_indicies[-1] >= CARD_RANK_ORDER.index("2"):
            # 2 and Joker cannot be used in a straight
            return False
        
        for i in range(len(rank_order_indicies) - 1):
            if rank_order_indicies[i+1] - rank_order_indicies[i] != 1:
                return False
        
        return True

    @staticmethod
    def max_rank(ranks: Iterable[str]):
        rank_order_indicies: list[int] = sorted(map(lambda rank: CARD_RANK_ORDER.index(rank), ranks))

        return CARD_RANK_ORDER[rank_order_indicies[-1]]
    
    def _score_hand(self, cards: list[Card]) -> None:
        rank_to_freq: dict[str, int] = defaultdict(int)
        for card in cards:
            rank_to_freq[card.rank] += 1

        sorted_frequencies: list[int] = sorted(rank_to_freq.values(), reverse=True)

        freq_to_rank: dict[int, set[str]] = defaultdict(set)
        for rank, freq in rank_to_freq.items():
            freq_to_rank[freq].add(rank)

        if len(cards) == 1:
            self.type = ComboType.SINGLE
            self.rank = cards[0].rank
            return

        elif len(cards) == 2:
            if cards[0].is_joker and cards[1].is_joker:
                self.type = ComboType.ROCKET
                return
            
            if sorted_frequencies[0] == 2:
                self.type = ComboType.PAIR
                self.rank = cards[0].rank
                return
        
        elif len(cards) == 3:
            if sorted_frequencies[0] == 3:
                self.type = ComboType.TRIPLET
                self.rank = cards[0].rank
                return

        elif len(cards) == 4:
            if sorted_frequencies[0] == 4:
                self.type = ComboType.BOMB
                self.rank = cards[0].rank
                return

            if sorted_frequencies[0] == 3:
                self.type = ComboType.TRIPLET_WITH_SINGLE
                self.rank = self.max_rank(freq_to_rank[3])
                return
        
        elif len(cards) == 5:
            if sorted_frequencies == [3, 2]:
                self.type = ComboType.TRIPLET_WITH_PAIR
                self.rank = self.max_rank(freq_to_rank[3])
                return
            
        elif len(cards) == 6:
            if sorted_frequencies == [4, 1, 1]:
                self.type = ComboType.QUADPLEX_WITH_SINGLES
                self.rank = self.max_rank(freq_to_rank[4])
                return

        elif len(cards) == 8:
            if sorted_frequencies == [4, 2, 2]:
                self.type = ComboType.QUADPLEX_WITH_PAIRS
                self.rank = self.max_rank(freq_to_rank[4])
                return

        if len(cards) >= 5:
            if all([freq == 1 for freq in sorted_frequencies]) and self.is_straight(freq_to_rank[1]):
                self.type = ComboType.SEQUENCE
                self.rank = self.max_rank(freq_to_rank[1])
                self.sequence_length = len(cards)
                return

            if all([freq == 2 for freq in sorted_frequencies]) and self.is_straight(freq_to_rank[2]):
                self.type = ComboType.SEQUENCE_OF_PAIRS
                self.rank = self.max_rank(freq_to_rank[2])
                self.sequence_length = len(cards)
                return

            if all([freq == 3 for freq in sorted_frequencies]) and self.is_straight(freq_to_rank[3]):
                self.type = ComboType.SEQUENCE_OF_TRIPLETS
                self.rank = self.max_rank(freq_to_rank[3])
                self.sequence_length = len(cards)
                return

            if all([freq in [1, 3] for freq in sorted_frequencies]) and sorted_frequencies.count(3) >= 2 and self.is_straight(freq_to_rank[3]):
                self.type = ComboType.SEQUENCE_OF_TRIPLETS_WITH_SINGLES
                self.rank = self.max_rank(freq_to_rank[3])
                self.sequence_length = len(cards)
                return

            if all([freq in [2, 3] for freq in sorted_frequencies]) and sorted_frequencies.count(3) >= 2 and self.is_straight(freq_to_rank[3]):
                self.type = ComboType.SEQUENCE_OF_TRIPLETS_WITH_PAIRS
                self.rank = self.max_rank(freq_to_rank[3])
                self.sequence_length = len(cards)
                return

        raise InvalidComboError

    def beats(self, other: Combo) -> bool:
        if self.type == ComboType.ROCKET:
            return True

        if other.type == ComboType.ROCKET:
            return False

        if self.type == ComboType.BOMB and other.type != ComboType.BOMB:
            return True

        if self.type != other.type:
            return False

        # if not a sequence both should be `None`
        if self.sequence_length != other.sequence_length:
            return False
                
        return CARD_RANK_ORDER.index(self.rank) > CARD_RANK_ORDER.index(other.rank)