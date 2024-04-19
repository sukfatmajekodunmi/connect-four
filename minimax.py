import random

class MinimaxAI:
    """Minimax AI for Connect Four with enhanced readability and adjusted structure."""

    def __init__(self, board):
        self.board = [row.copy() for row in board]
        self.players = ['x', 'o']

    def optimal_move(self, depth, state, player):
        """Determines the optimal move using Minimax algorithm."""
        opponent = self.players[1] if player == self.players[0] else self.players[0]
        legal_moves = {col: -self.minimax(depth - 1, self.simulate_move(state, col, player), opponent)
                       for col in range(7) if self.valid_move(col, state)}
        
        best_value = -float('inf')
        best_moves = []
        for move, value in legal_moves.items():
            if value > best_value:
                best_value = value
                best_moves = [move]
            elif value == best_value:
                best_moves.append(move)

        return random.choice(best_moves), best_value

    def minimax(self, depth, state, player):
        """Recursive search to explore all possible moves up to a given depth."""
        if depth == 0 or self.is_terminal(state):
            return self.evaluate(state, player)
        
        opponent = self.players[1] if player == self.players[0] else self.players[0]
        values = [-self.minimax(depth - 1, self.simulate_move(state, col, player), opponent)
                  for col in range(7) if self.valid_move(col, state)]

        return max(values) if values else 0

    def valid_move(self, col, state):
        """Check if dropping a piece in the column is a valid move."""
        return any(state[row][col] == " " for row in range(6))

    def is_terminal(self, state):
        """Check if the game is over."""
        return any(self.count_streak(state, player, 4) > 0 for player in self.players)

    def simulate_move(self, state, col, player):
        """Returns a new state after making a move in the specified column."""
        temp_state = [row.copy() for row in state]
        for row in reversed(range(6)):
            if temp_state[row][col] == " ":
                temp_state[row][col] = player
                break
        return temp_state

    def evaluate(self, state, player):
        """Evaluates the board using a simple heuristic based on streak counts."""
        if player == self.players[0]:
            opponent = self.players[1]
        else:
            opponent = self.players[0]

        player_score = sum(self.count_streak(state, player, k) * (10**k) for k in range(2, 5))
        opponent_score = sum(self.count_streak(state, opponent, k) * (10**k) for k in range(2, 5))

        if self.count_streak(state, opponent, 4):
            return -float('inf')
        else:
            return player_score - opponent_score

    def count_streak(self, state, player, streak):
        """Counts all streaks of the specified size for the given player."""
        return sum(
            self.check_streak(state, player, row, col, dx, dy, streak)
            for row in range(6) for col in range(7)
            for dx, dy in [(-1, 1), (0, 1), (1, 1), (1, 0)]
        )

    def check_streak(self, state, player, row, col, dx, dy, streak):
        """Checks how many streaks of a specified length start from a specific cell."""
        end_row = row + (streak - 1) * dx
        end_col = col + (streak - 1) * dy
        if 0 <= end_row < 6 and 0 <= end_col < 7:
            if all(state[row + i * dx][col + i * dy] == player for i in range(streak)):
                return 1
        return 0
