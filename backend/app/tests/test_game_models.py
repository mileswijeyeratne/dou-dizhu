import unittest
from app.game.models import Card, Joker, CardSuit, HandType, Hand

class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card("A", CardSuit.SPADES)
        self.assertEqual(card.rank, "A")
        self.assertEqual(card.suit, CardSuit.SPADES)
        self.assertFalse(card.is_joker)
        self.assertEqual(repr(card), "A of S")

    def test_joker_creation(self):
        small_joker = Joker(is_big=False)
        big_joker = Joker(is_big=True)
        self.assertTrue(small_joker.is_joker)
        self.assertTrue(big_joker.is_joker)
        self.assertEqual(repr(small_joker), "Small Joker")
        self.assertEqual(repr(big_joker), "Big Joker")

# Hand creation not implemented yet
# class TestHand(unittest.TestCase):
#     def test_hand_creation_pair(self):
#         card1 = Card("5", CardSuit.HEARTS)
#         card2 = Card("5", CardSuit.SPADES)
#         hand = Hand([card1, card2])
#         self.assertEqual(hand.rank, "5")
#         self.assertEqual(hand.type, HandType.PAIR)

#     def test_hand_creation_rocket(self):
#         card1 = Joker(is_big=True)
#         card2 = Joker(is_big=False)
#         hand = Hand([card1, card2])
#         self.assertEqual(hand.type, HandType.ROCKET)

if __name__ == "__main__":
    unittest.main()
