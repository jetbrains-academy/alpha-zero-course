import numpy as np

from MCTS.TreeSearch.task import MCTS
from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe
from TicTacToe.Round.task import Round


def mcts_init(round):
    args = {
        'C': 1.41,
        'num_searches': 2000
    }
    return MCTS(round.instance_of_game, args)


def main():
    second_round = Round(TicTacToe(Board()))
    mcts = mcts_init(second_round)
    player = second_round.player
    board = second_round.instance_of_game.get_board()
    is_playing = True
    while is_playing:
        if player == 1:
            second_round.print_game_layout()
            action = int(input())
        else:
            neutral_state = second_round.instance_of_game.change_perspective(board, player)
            mcts_probs = mcts.search(neutral_state)
            action = np.argmax(mcts_probs)

        is_playing = second_round.play_game(action)
        player = second_round.instance_of_game.get_opponent(player)


if __name__ == "__main__":
    main()
