import unittest
from minimax import MinimaxAI  # Ensure to import your class appropriately

class TestMinimaxAI(unittest.TestCase):
    def setUp(self):
        # Setup a board that is partly filled to simulate mid-game state
        self.initial_state = [
            [" ", " ", " ", " ", " ", " ", "o"],
            [" ", " ", " ", " ", " ", " ", "x"],
            [" ", " ", " ", "o", " ", " ", "o"],
            [" ", " ", "x", "x", "o", " ", "x"],
            [" ", "x", "o", "x", "o", " ", "o"],
            ["o", "x", "x", "o", "x", "o", "x"]
        ]
        self.ai = MinimaxAI(self.initial_state)

    def test_valid_move(self):
        # Column 3 should be valid since there's space at row 3
        self.assertTrue(self.ai.valid_move(3, self.initial_state))
        # Column 6 should be invalid as it's full
        self.assertFalse(self.ai.valid_move(6, self.initial_state))

    def test_simulate_move(self):
        # Simulate placing "x" in column 3, should go to row 3
        new_state = self.ai.simulate_move(self.initial_state, 3, "x")
        self.assertEqual(new_state[3][3], "x")

    def test_is_terminal(self):
        # The initial state is not a terminal state (game not ended)
        self.assertFalse(self.ai.is_terminal(self.initial_state))
        # State after a winning move
        winning_state = [row[:] for row in self.initial_state]
        winning_state[2][1] = "x"
        winning_state[1][1] = "x"
        self.ai = MinimaxAI(winning_state)
        self.assertTrue(self.ai.is_terminal(winning_state))

    def test_evaluate(self):
        # Evaluation should recognize no immediate win, checks score balance
        score = self.ai.evaluate(self.initial_state, "x")
        self.assertIsInstance(score, int)

    def test_minimax(self):
        # Testing minimax at a shallow depth to ensure it returns a score
        depth = 1
        score = self.ai.minimax(depth, self.initial_state, "x")
        self.assertIsInstance(score, int)

    def test_optimal_move(self):
        # Testing optimal move selection at a shallow depth
        move, score = self.ai.optimal_move(1, self.initial_state, "x")
        self.assertIn(move, range(7))  # Move should be a valid column
        self.assertIsInstance(score, int)

if __name__ == '__main__':
    unittest.main()
