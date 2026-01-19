import unittest

from app.game.game import Game, GameState, InvalidStateError, InvalidTurnError, InvalidBidError, InvalidMoveError
from app.game.player import Player
from app.game.models import Card, CardSuit 

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player1 = Player(1, "p1")
        self.player2 = Player(2, "p2")
        self.player3 = Player(3, "p3")
        self.players = [self.player1, self.player2, self.player3]

    def test_add_players(self):
        self.game.add_player(self.player1)
        self.assertEqual(len(self.game.players), 1)
        
        self.game.add_player(self.player2)
        self.assertEqual(len(self.game.players), 2)

        self.game.add_player(self.player3)
        self.assertEqual(len(self.game.players), 3)
        self.assertEqual(self.game.gamestate, GameState.BIDDING)

        with self.assertRaises(InvalidStateError):
            self.game.add_player(Player(4, "p4"))

    def test_make_bid(self):
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.add_player(self.player3)

        self.assertEqual(self.game.gamestate, GameState.BIDDING)

        turn_ind = self.players.index(self.game.get_turn())

        # First player bids
        self.game.make_bid(self.players[turn_ind], 1)
        self.assertEqual(self.game.bids[self.players[turn_ind]], 1)

        # Invlid player bids
        with self.assertRaises(InvalidTurnError):
            self.game.make_bid(self.players[turn_ind], 2)

        # Second player makes a too low bid
        turn_ind = (turn_ind + 1) % 3
        player2 = self.players[turn_ind]
        with self.assertRaises(InvalidBidError):
            self.game.make_bid(player2, 1)

        # Second player makes a valid bid
        self.game.make_bid(player2, 2)
        self.assertEqual(self.game.bids[player2], 2)

        # Player 3 bids 3, should end bidding
        turn_ind = (turn_ind + 1) % 3
        player3 = self.players[turn_ind]
        self.game.make_bid(player3, 3)
        self.assertEqual(self.game.gamestate, GameState.GAMEPLAY)

    def test_invalid_bid_when_not_bidding(self):
        with self.assertRaises(InvalidStateError):
            self.game.make_bid(self.game.get_turn(), 2)

    def test_play_combo_invalid_state(self):
        with self.assertRaises(InvalidStateError):
            self.game.play_combo(self.game.get_turn(), [Card("3", CardSuit.HEARTS)])

    def test_invalid_move(self):
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.add_player(self.player3)

        self.game.make_bid(self.game.get_turn(), 3)

        with self.assertRaises(InvalidMoveError):
            self.game.skip_play(self.game.get_turn())

    def test_get_payout(self):
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.add_player(self.player3)

        turn_ind = self.players.index(self.game.get_turn())
        player1 = self.players[turn_ind]
        player2 = self.players[(turn_ind + 1) % 3]
        player3 = self.players[(turn_ind + 2) % 3]

        self.game.make_bid(player1, 3)
        self.assertEqual(self.game.landlord, player1)

        self.game.gamestate = GameState.GAMEOVER
        self.game.landlord_won = True

        self.assertEqual(self.game.get_payout(player1), 6)
        self.assertEqual(self.game.get_payout(player2), -3)
        self.assertEqual(self.game.get_payout(player3), -3)

        self.game.landlord_won = False
        self.assertEqual(self.game.get_payout(player1), -6)
        self.assertEqual(self.game.get_payout(player2), 3)
        self.assertEqual(self.game.get_payout(player3), 3)

if __name__ == "__main__":
    unittest.main()