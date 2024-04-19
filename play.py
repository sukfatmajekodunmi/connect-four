from connect_four import Game


def play_game():
    """Start and play a game of Connect4."""
    game_instance = Game()
    game_instance.print_state()

    player1, player2 = game_instance.players[:2]
    score_board = [0, 0, 0]  # [player1 wins, player2 wins, ties]

    game_active = True
    while game_active:
        while not game_instance.finished:
            game_instance.next_move()

        game_instance.find_fours()
        game_instance.print_state()

        update_scoreboard(game_instance, player1, player2, score_board)
        display_stats(player1, player2, score_board)

        game_active = ask_for_rematch(game_instance)


def update_scoreboard(game_instance, player1, player2, score_board):
    """Update the scoreboard based on the game outcome."""
    if game_instance.winner is None:
        score_board[2] += 1
    elif game_instance.winner == player1:
        score_board[0] += 1
    elif game_instance.winner == player2:
        score_board[1] += 1


def display_stats(player1, player2, score_board):
    """Display the current game statistics."""
    print(
        f"{player1.name}: {score_board[0]} wins, {player2.name}: {score_board[1]} wins, {score_board[2]} ties"
    )


def ask_for_rematch(game_instance):
    """Ask the players if they want to play again and handle their response."""
    while True:
        player_response = input("Would you like to play again? (yes/no): ").lower()
        if player_response in ["y", "yes"]:
            game_instance.new_game()
            game_instance.print_state()
            return True
        elif player_response in ["n", "no"]:
            print("Thanks for playing!")
            return False
        else:
            print("Please enter 'yes' or 'no'. ")


if __name__ == "__main__":
    play_game()
