from TicTacToe.GameImplementation.Game import TicTacToe

tictactoe = TicTacToe()
player = 1

board = tictactoe.get_init_board()

while True:
    print(board)
    valid_moves = tictactoe.get_valid_moves(board)
    print("valid_moves", [i for i in range(tictactoe.get_action_size()) if valid_moves[i] == 1])
    action = int(input(f"{player}:"))

    if valid_moves[action] == 0:
        print("action not valid")
        continue

    board = tictactoe.get_next_state(board, player, action)

    value = tictactoe.get_game_ended(board, player)

    if value:
        print(board)
        if value == 1:
            print(player, "won")
        elif value == -1:
            print(-player, "won")
        else:
            print("draw")
        break

    player = tictactoe.get_opponent(player)
