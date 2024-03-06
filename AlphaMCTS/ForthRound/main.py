import numpy as np

from AlphaMCTS.TreeSearch.task import AlphaMCTS
from ResNetEstimator.Model.task import ResNet
from TicTacToe.Round.task import Round


def mcts_init(round):
    args = {
        'C': 2,
        'num_searches': 1000
    }
    model = ResNet(round.tictactoe, 4, 64)
    model.eval()

    return AlphaMCTS(round.tictactoe, args, model)


if __name__ == "__main__":
    fourth_round = Round()
    mcts = mcts_init(fourth_round)

    player = fourth_round.player
    board = fourth_round.tictactoe.get_board()

    is_playing = True
    while is_playing:
        if player == 1:
            fourth_round.print_game_layout()
            action = int(input())
        else:
            neutral_state = fourth_round.tictactoe.change_perspective(board, player)
            mcts_probs = mcts.search(neutral_state)
            action = np.argmax(mcts_probs)

        is_playing = fourth_round.play_game(action)
        player = fourth_round.tictactoe.get_opponent(player)
