import numpy as np

from TicTacToe.Game.Game import TicTacToe
from MCTS.TreeSearch.task import MCTS

tictactoe = TicTacToe()
player = 1

args = {
    'C': 1.41,
    'num_searches': 1000
}

mcts = MCTS(tictactoe, args)

board = tictactoe.get_init_board()

while True:
    print(board)

    if player == 1:
        valid_moves = tictactoe.get_valid_moves(board)
        print("valid_moves", [i for i in range(tictactoe.get_action_size()) if valid_moves[i] == 1])
        action = int(input(f"{player}:"))

        if valid_moves[action] == 0:
            print("action not valid")
            continue

    else:
        neutral_state = tictactoe.change_perspective(board, player)
        mcts_probs = mcts.search(neutral_state)
        action = np.argmax(mcts_probs)

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
