from minimax import MinimaxAI
import random, time, os

class Game(object):
    """Game object that holds state of Connect 4 board and game values"""

    finished = None
    board = None
    winner = None
    turn = None
    round = None
    game_name = "Connect Four"
    colors = ["x", "o"]
    players = [None, None]

    def __init__(self):
        self.winner = None
        self.finished = False
        self.round = 1

        # Cross-platform command to clear the terminal screen
        
        # Determine the operating system type
        is_windows = os.name == 'nt'

        # Choose the command based on the operating system
        clear_command = "cls" if is_windows else "clear"

        # Execute the command to clear the terminal screen
        os.system(clear_command)

        # Initial greeting
        greeting = "Welcome to {0}!".format(self.game_name)
        print(greeting)

        # Configuration for Player 1
        print("Configure Player 1: Human or Computer?")
        while self.players[0] is None:
            # Prompt for player type selection, stripping any leading/trailing whitespace
            choice_input = input("Choose 'H' for Human or 'C' for Computer: ")
            choice = choice_input.strip()
            
            # Normalize the choice to lowercase for comparison
            choice = choice.lower()
            
            # Check if the choice is for a human player
            if choice in ["h", "human"]:
                # Input for human player's name
                name_input = input("Enter Player 1's name: ")
                name = name_input.strip()

                # Set the human player in the first position
                self.players[0] = Player(name, self.colors[0])
            
            # Check if the choice is for a computer player
            elif choice in ["c", "computer"]:
                # Input for computer player's name
                name_input = input("Enter Player 1's name: ")
                name = name_input.strip()

                # Input for setting AI difficulty level, with parsing to integer
                difficulty_input = input("Set AI difficulty (1-4): ")
                difficulty = int(difficulty_input.strip())

                # Adjust difficulty level for implementation specifics (add 1 as in original)
                difficulty_adjusted = difficulty + 1

                # Set the AI player in the first position
                self.players[0] = AIPlayer(name, self.colors[0], difficulty_adjusted)
            
            # Handle invalid input
            else:
                # Notify the user of the invalid input
                print("Sorry, that's not a valid option. Please try again.")

        print(f"Player 1, {self.players[0].name}, will use color {self.colors[0]}.")

        # Configuration for Player 2
        print("Configure Player 2: Human or Computer?")
        while self.players[1] is None:
            choice = input("Choose 'H' for Human or 'C' for Computer: ").strip()
            if choice.lower() in ["h", "human"]:
                name = input("Enter Player 2's name: ")
                self.players[1] = Player(name, self.colors[1])
            elif choice.lower() in ["c", "computer"]:
                name = input("Enter Player 2's name: ")
                difficulty = int(input("Set AI difficulty (1-4): "))
                self.players[1] = AIPlayer(name, self.colors[1], difficulty + 1)
            else:
                print("Sorry, that's not a valid option. Please try again.")

        print(f"Player 2, {self.players[1].name}, will use color {self.colors[1]}.")

        # Player 1 begins the game
        self.turn = self.players[0]

        # Initialize the game board
        self.board = [[" " for _ in range(7)] for _ in range(6)]

    def new_game(self):
        """
        Restart the game to its starting state, player names and colors remain the same.
        """
        self.winner = None
        self.finished = False
        self.round = 1

        # Player 1 should always start first
        self.turn = self.players[0]

        # Clear out the board for a new game
        self.board = [[" " for _ in range(7)] for _ in range(6)]

    def switch_turn(self):
        """
        Switch the current player's turn to the next player.
        Also increments the round number.
        """
        # Toggle between player 1 and player 2
        self.turn = self.players[0] if not self.turn == self.players[0] else self.players[1]

        # Move to the next round
        self.round += 1

    def next_move(self):
        """
        Handle the player's move. Check for game end conditions,
        update the board, and switch turns.
        """
        player = self.turn if self.turn is not None else self.players[0]

        # Check if the game should end due to reaching the max rounds possible
        if self.round > 42:
            self.finished = True
            print("Game ended in a draw (stalemate).")
            return None

        # Get the player's chosen column for their move
        current_move = player.move(self.board)
        
        move = current_move

        # Place the player's piece in the chosen column if possible
        for i in range(6):
            if self.board[i][move] == " ":
                self.board[i][move] = player.color
                self.switch_turn()
                self.check_for_fours()
                self.print_state()
                return  # Successful move ends the function

        # If no spaces were found in the column, the column is full
        print("Invalid move: column is full.")

    def check_for_fours(self):
        """
        Check the board for any sequence of four consecutive pieces
        in vertical, horizontal, or diagonal lines. Ends the game
        if a sequence is found.
        """
        # Scan every position on the board
        for i in range(6):
            for j in range(7):
                if self.board[i][j] == " ":
                    continue  # Skip empty slots

                # Check for vertical sequences starting from the current position
                if self.vertical_check(i, j):
                    self.finished = True
                    print("Vertical win detected.")
                    return

                # Check for horizontal sequences
                if self.horizontal_check(i, j):
                    self.finished = True
                    print("Horizontal win detected.")
                    return

                # Check for diagonal sequences and retrieve any slope information
                diagonal_win, slope = self.diagonal_check(i, j)
                if diagonal_win:
                    print(f"Diagonal win detected with slope {slope}.")
                    self.finished = True
                    return

    def vertical_check(self, row, col):
        """
        Check vertically from the given position to see if there are four
        consecutive pieces belonging to the same player. Also assigns the winner.
        """
        consecutive_count = 0  # Counter for consecutive pieces

        # Start from the current row and check downwards
        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break

        # If four or more pieces are consecutive, declare a winner
        if consecutive_count >= 4:
            winner_color = self.board[row][col].lower()
            self.winner = (
                self.players[0]
                if self.players[0].color.lower() == winner_color
                else self.players[1]
            )
            return True

        return False

    def horizontal_check(self, row, col):
        """
        Check horizontally from the given position to see if there are four
        consecutive pieces belonging to the same player. Also assigns the winner.
        """
        consecutive_count = 0  # Counter for consecutive pieces

        # Start from the current column and check to the right
        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break

        # If four or more pieces are consecutive, declare a winner
        if consecutive_count >= 4:
            winner_color = self.board[row][col].lower()
            self.winner = (
                self.players[0]
                if self.players[0].color.lower() == winner_color
                else self.players[1]
            )
            return True

        return False

    def diagonal_check(self, row, col):
        """
        Check for four consecutive pieces in both diagonal directions from
        a given starting point, identifying if the sequence has a positive or negative slope.
        """
        four_in_a_row = False
        slope = None
        diagonals = {"positive": 0, "negative": 0}

        # Positive slope diagonal check
        for i, j in zip(range(row, 6), range(col, 7)):
            if self.board[i][j].lower() != self.board[row][col].lower():
                break
            diagonals["positive"] += 1

        # Assign winner if positive slope diagonal has four or more
        if diagonals["positive"] >= 4:
            slope = "positive"
            self.winner = (
                self.players[0]
                if self.players[0].color.lower() == self.board[row][col].lower()
                else self.players[1]
            )
            four_in_a_row = True

        # Negative slope diagonal check
        for i, j in zip(range(row, -1, -1), range(col, 7)):
            if self.board[i][j].lower() != self.board[row][col].lower():
                break
            diagonals["negative"] += 1

        # Assign winner if negative slope diagonal has four or more
        if diagonals["negative"] >= 4:
            slope = "negative" if slope is None else "both"
            self.winner = (
                self.players[0]
                if self.players[0].color.lower() == self.board[row][col].lower()
                else self.players[1]
            )
            four_in_a_row = True

        return four_in_a_row, slope

    def find_fours(self):
        """
        Search the board for any sequence of four consecutive pieces
        and highlight them using a specified method.
        """
        for i in range(6):
            for j in range(7):
                if self.board[i][j] == " ":
                    continue

                # Check and highlight vertical, horizontal, and diagonal sequences
                if self.vertical_check(i, j):
                    self.highlight_four(i, j, "vertical")
                if self.horizontal_check(i, j):
                    self.highlight_four(i, j, "horizontal")
                diag_fours, slope = self.diagonal_check(i, j)
                if diag_fours:
                    self.highlight_four(i, j, "diagonal", slope)

    def highlight_four(self, row, col, direction, slope=None):
        """
        Highlight a sequence of four consecutive pieces by capitalizing them.
        Direction specifies vertical, horizontal, or diagonal alignment.
        """
        if direction == "vertical":
            for i in range(4):
                self.board[row + i][col] = self.board[row + i][col].upper()
        elif direction == "horizontal":
            for i in range(4):
                self.board[row][col + i] = self.board[row][col + i].upper()
        elif direction == "diagonal":
            if slope in ["positive", "both"]:
                for i in range(4):
                    self.board[row + i][col + i] = self.board[row + i][col + i].upper()
            if slope in ["negative", "both"]:
                for i in range(4):
                    self.board[row - i][col + i] = self.board[row - i][col + i].upper()
        else:
            print("Error - Cannot enunciate four-of-a-kind")

    def print_state(self):
        """
        Display the current state of the game board, round number, and
        end game conditions if the game has finished.
        """
        # Clear the console based on the operating system
        os.system("cls" if os.name == "nt" else "clear")

        # Print game name and current round
        print(f"{self.game_name}! Round: {self.round}")

        # Print the game board starting from the top row
        for i in range(5, -1, -1):  # Loop backwards to display the top row first
            print("\t", end="")
            for j in range(7):
                print(
                    f"| {self.board[i][j]} ", end=""
                )  # Print each cell bordered by pipes
            print("|")  # Newline after each row

        # Print column numbers for reference
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        # Print game over message and winner if the game is finished
        if self.finished:
            print("Game Over!")
            if self.winner is not None:
                print(f"{self.winner.name} is the winner!")
            else:
                print("Game was a draw.")


class Player:
    """
    Represents a human player in the game with a specified name and color.
    """

    def __init__(self, name, color):
        self.type = "Human"  # Designates the type of player
        self.name = name  # Name of the player
        self.color = color  # Color assigned to the player

    def move(self, state):
        """
        Prompt the human player for a column number to place their piece.
        Validates the input to ensure it's within the acceptable range.
        """
        print(f"{self.name}'s turn. {self.name} is {self.color}")
        column = None
        while column is None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
                if 0 <= choice <= 6:
                    column = choice
                else:
                    print("Invalid choice, try again.")
            except ValueError:
                print("Invalid input; please enter a number.")
        return column


class AIPlayer(Player):
    """
    AI Player that extends Player. It uses a minimax algorithm to determine
    the best move based on the current state of the game.
    """

    def __init__(self, name, color, difficulty=5):
        super().__init__(name, color)  # Initialize base class attributes
        self.type = "AI"  # Designates the type of player as AI
        self.difficulty = (
            difficulty  # Difficulty level for the AI's decision-making process
        )

    def move(self, state):
        """
        Calculate the AI's move using the minimax algorithm with a set difficulty level.
        This simulates a thoughtful decision-making process by the AI.
        """
        print(f"{self.name}'s turn. {self.name} is {self.color}")

        # Delay to simulate thinking 
        # time.sleep(random.uniform(0.8, 1.6))

        # Instantiate minimax and get the best move
        minimax = MinimaxAI(state)
        best_move, _ = minimax.optimal_move(self.difficulty, state, self.color)
        return best_move
