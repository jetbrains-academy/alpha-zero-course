import numpy as np

from AlphaMCTS.TreeSearch.task import AlphaMCTS
from ResNetEstimator.Model.task import ResNet
from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe
from TicTacToe.Round.task import Round


def mcts_init(round):
    args = {
        'C': 2,
        'num_searches': 1000
    }
    device = 'cpu'
    model = ResNet(round.instance_of_game, 4, 64, device)
    model.eval()

    return AlphaMCTS(round.instance_of_game, args, model)


def main():
    fourth_round = Round(TicTacToe(Board()))
    mcts = mcts_init(fourth_round)
    player = fourth_round.player
    board = fourth_round.instance_of_game.get_board()
    is_playing = True
    while is_playing:
        if player == 1:
            fourth_round.print_game_layout()
            action = int(input())
        else:
            neutral_state = fourth_round.instance_of_game.change_perspective(board, player)
            mcts_probs = mcts.search(neutral_state)
            action = np.argmax(mcts_probs)

        is_playing = fourth_round.play_game(action)
        player = fourth_round.instance_of_game.get_opponent(player)


if __name__ == "__main__":
    main()
