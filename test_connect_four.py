import unittest
from connect_four import *


class TestConnectFourGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(test_mode=True)
        self.game.players[0] = Player("Test Player 1", "x")
        self.game.players[1] = Player("Test Player 2", "o")
        self.game.turn = self.game.players[0]

    def test_vertical_win(self):
        # Manually set the board for a vertical win
        for i in range(4):
            self.game.board[i][0] = "x"
        self.assertTrue(self.game.vertical_check(0, 0))
        self.assertEqual(self.game.winner.name, "Test Player 1")

        # Reset for negative test
        self.game.new_game()
        # Set the board for a vertical no-win (interrupted by another player's token)
        for i in range(3):
            self.game.board[i][0] = "x"
        self.game.board[3][0] = "o"
        self.assertFalse(self.game.vertical_check(0, 0))

    def test_horizontal_win(self):
        # Set the board for a horizontal win
        for i in range(4):
            self.game.board[0][i] = "x"
        self.assertTrue(self.game.horizontal_check(0, 0))
        self.assertEqual(self.game.winner.name, "Test Player 1")

        # Reset for negative test
        self.game.new_game()
        # Set the board for a horizontal no-win (interrupted by another player's token)
        for i in range(3):
            self.game.board[0][i] = "x"
        self.game.board[0][3] = "o"
        self.assertFalse(self.game.horizontal_check(0, 0))

    def test_diagonal_win_positive_slope(self):
        # Set the board for a positive slope diagonal win
        for i in range(4):
            self.game.board[i][i] = "x"
        self.assertTrue(self.game.diagonal_check(0, 0)[0])
        self.assertEqual(self.game.winner.name, "Test Player 1")

        # Reset for negative test
        self.game.new_game()
        # Set the board for a positive slope diagonal no-win (interrupted by another player's token)
        for i in range(3):
            self.game.board[i][i] = "x"
        self.game.board[3][3] = "o"
        self.assertFalse(self.game.diagonal_check(0, 0)[0])

    def test_diagonal_win_negative_slope(self):
        # Set the board for a negative slope diagonal win
        for i in range(4):
            self.game.board[3 - i][i] = "x"
        self.assertTrue(self.game.diagonal_check(3, 0)[0])
        self.assertEqual(self.game.winner.name, "Test Player 1")

        # Reset for negative test
        self.game.new_game()
        # Set the board for a negative slope diagonal no-win (interrupted by another player's token)
        for i in range(3):
            self.game.board[3 - i][i] = "x"
        self.game.board[0][3] = "o"
        self.assertFalse(self.game.diagonal_check(3, 0)[0])


if __name__ == "__main__":
    unittest.main()
