import unittest
from app.game.models import Card, Joker, CardSuit, ComboType, Combo, InvalidComboError

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

class TestHandCreation(unittest.TestCase):
    def test_hand_creation_single(self):
        cards = [Joker(is_big=True)]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "BJ")
        self.assertEqual(hand.type, ComboType.SINGLE)
        self.assertEqual(hand.sequence_length, None)

    def test_hand_creation_pair(self):
        cards = [Card("5", CardSuit.HEARTS), Card("5", CardSuit.SPADES)]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "5")
        self.assertEqual(hand.type, ComboType.PAIR)
        self.assertEqual(hand.sequence_length, None)

    def test_hand_creation_triplet(self):
        cards = [Card("7", CardSuit.HEARTS), Card("7", CardSuit.DIAMONDS), Card("7", CardSuit.SPADES)]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "7")
        self.assertEqual(hand.type, ComboType.TRIPLET)
        self.assertEqual(hand.sequence_length, None)

    def test_hand_creation_triplet_with_single(self):
        cards = [
            Card("Q", CardSuit.HEARTS), 
            Card("Q", CardSuit.DIAMONDS), 
            Card("Q", CardSuit.SPADES), 
            Card("3", CardSuit.CLUBS)
        ]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "Q")
        self.assertEqual(hand.type, ComboType.TRIPLET_WITH_SINGLE)
        self.assertEqual(hand.sequence_length, None)

    def test_hand_creation_triplet_with_pair(self):
        cards = [
            Card("K", CardSuit.HEARTS), 
            Card("K", CardSuit.DIAMONDS), 
            Card("K", CardSuit.SPADES), 
            Card("5", CardSuit.HEARTS), 
            Card("5", CardSuit.SPADES)
        ]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "K")
        self.assertEqual(hand.type, ComboType.TRIPLET_WITH_PAIR)
        self.assertEqual(hand.sequence_length, None)

    def test_hand_creation_sequence(self):
        cards = [
            Card("6", CardSuit.HEARTS), 
            Card("7", CardSuit.DIAMONDS), 
            Card("8", CardSuit.SPADES), 
            Card("9", CardSuit.CLUBS), 
            Card("10", CardSuit.HEARTS)
        ]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "10")
        self.assertEqual(hand.type, ComboType.SEQUENCE)
        self.assertEqual(hand.sequence_length, 5)

    def test_hand_creation_sequence_of_pairs(self):
        cards = [
            Card("4", CardSuit.HEARTS), Card("4", CardSuit.DIAMONDS),
            Card("5", CardSuit.SPADES), Card("5", CardSuit.CLUBS),
            Card("6", CardSuit.HEARTS), Card("6", CardSuit.DIAMONDS)
        ]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "6")
        self.assertEqual(hand.type, ComboType.SEQUENCE_OF_PAIRS)
        self.assertEqual(hand.sequence_length, 6)

    def test_hand_creation_sequence_of_triplets(self):
        cards = [
            Card("7", CardSuit.HEARTS), Card("7", CardSuit.DIAMONDS), Card("7", CardSuit.SPADES),
            Card("8", CardSuit.HEARTS), Card("8", CardSuit.DIAMONDS), Card("8", CardSuit.SPADES)
        ]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "8")
        self.assertEqual(hand.type, ComboType.SEQUENCE_OF_TRIPLETS)
        self.assertEqual(hand.sequence_length, 6)

    def test_hand_creation_quadplex_with_singles(self):
        cards = [
            Card("J", CardSuit.HEARTS), Card("J", CardSuit.DIAMONDS), 
            Card("J", CardSuit.SPADES), Card("J", CardSuit.CLUBS), 
            Card("3", CardSuit.HEARTS), Card("4", CardSuit.SPADES)
        ]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "J")
        self.assertEqual(hand.type, ComboType.QUADPLEX_WITH_SINGLES)

    def test_hand_creation_quadplex_with_pairs(self):
        cards = [
            Card("A", CardSuit.HEARTS), Card("A", CardSuit.DIAMONDS), 
            Card("A", CardSuit.SPADES), Card("A", CardSuit.CLUBS), 
            Card("5", CardSuit.HEARTS), Card("5", CardSuit.SPADES),
            Card("6", CardSuit.DIAMONDS), Card("6", CardSuit.CLUBS)
        ]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "A")
        self.assertEqual(hand.type, ComboType.QUADPLEX_WITH_PAIRS)

    def test_hand_creation_bomb(self):
        cards = [Card("9", CardSuit.HEARTS), Card("9", CardSuit.DIAMONDS), Card("9", CardSuit.SPADES), Card("9", CardSuit.CLUBS)]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "9")
        self.assertEqual(hand.type, ComboType.BOMB)

    def test_hand_creation_rocket(self):
        cards = [Joker(is_big=True), Joker(is_big=False)]
        hand = Combo(cards)
        self.assertEqual(hand.rank, "")
        self.assertEqual(hand.type, ComboType.ROCKET)
        self.assertEqual(hand.sequence_length, None)

    def test_invalid_hand(self):
        cards = [Card("5", CardSuit.HEARTS), Card("6", CardSuit.SPADES), Card("5", CardSuit.CLUBS), Card("7", CardSuit.HEARTS)]
        with self.assertRaises(InvalidComboError):
            Combo(cards)

    def test_invalid_straight(self):
        cards = [Card("10", CardSuit.HEARTS), Card("Q", CardSuit.HEARTS), Card("K", CardSuit.SPADES), Card("A", CardSuit.CLUBS), Card("2", CardSuit.HEARTS)]
        with self.assertRaises(InvalidComboError):
            Combo(cards)

class TestHandBeats(unittest.TestCase):
    def test_rocket_beats_everything(self):
        rocket = Combo([Joker(is_big=True), Joker(is_big=False)])
        bomb = Combo([Card("5", CardSuit.HEARTS), Card("5", CardSuit.SPADES), Card("5", CardSuit.CLUBS), Card("5", CardSuit.DIAMONDS)])
        pair = Combo([Card("K", CardSuit.HEARTS), Card("K", CardSuit.SPADES)])

        self.assertTrue(rocket.beats(bomb))
        self.assertTrue(rocket.beats(pair))

    def test_bomb_beats_non_bomb(self):
        bomb = Combo([Card("6", CardSuit.HEARTS), Card("6", CardSuit.SPADES), Card("6", CardSuit.CLUBS), Card("6", CardSuit.DIAMONDS)])
        triplet = Combo([Card("7", CardSuit.HEARTS), Card("7", CardSuit.SPADES), Card("7", CardSuit.CLUBS)])

        self.assertTrue(bomb.beats(triplet))
        self.assertFalse(triplet.beats(bomb))

    def test_bomb_beats_lower_bomb(self):
        bomb6 = Combo([Card("6", CardSuit.HEARTS), Card("6", CardSuit.SPADES), Card("6", CardSuit.CLUBS), Card("6", CardSuit.DIAMONDS)])
        bomb7 = Combo([Card("7", CardSuit.HEARTS), Card("7", CardSuit.SPADES), Card("7", CardSuit.CLUBS), Card("7", CardSuit.DIAMONDS)])

        self.assertTrue(bomb7.beats(bomb6))
        self.assertFalse(bomb6.beats(bomb7))

    def test_higher_rank_beats_lower_rank_same_type(self):
        higher_pair = Combo([Card("A", CardSuit.HEARTS), Card("A", CardSuit.SPADES)])
        lower_pair = Combo([Card("10", CardSuit.HEARTS), Card("10", CardSuit.SPADES)])

        self.assertTrue(higher_pair.beats(lower_pair))
        self.assertFalse(lower_pair.beats(higher_pair))

    def test_mismatched_hand_types_dont_beat_each_other(self):
        pair = Combo([Card("J", CardSuit.HEARTS), Card("J", CardSuit.SPADES)])
        triplet = Combo([Card("Q", CardSuit.HEARTS), Card("Q", CardSuit.SPADES), Card("Q", CardSuit.CLUBS)])

        self.assertFalse(pair.beats(triplet))
        self.assertFalse(triplet.beats(pair))

    def test_mismatched_sequence_lengths_dont_beat_each_other(self):
        sequence_5 = Combo([
            Card("7", CardSuit.HEARTS), Card("8", CardSuit.SPADES), Card("9", CardSuit.CLUBS),
            Card("10", CardSuit.DIAMONDS), Card("J", CardSuit.HEARTS)
        ])
        sequence_6 = Combo([
            Card("6", CardSuit.HEARTS), Card("7", CardSuit.SPADES), Card("8", CardSuit.CLUBS),
            Card("9", CardSuit.DIAMONDS), Card("10", CardSuit.HEARTS), Card("J", CardSuit.SPADES)
        ])

        self.assertFalse(sequence_5.beats(sequence_6))
        self.assertFalse(sequence_6.beats(sequence_5))


if __name__ == "__main__":
    unittest.main()
