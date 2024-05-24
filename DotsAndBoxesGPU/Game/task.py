from abc import ABC

from TicTacToe.Game.task import TicTacToe


class DotsAndBoxes(TicTacToe, ABC):
    def __init__(self, board):
        super().__init__(board)

    def get_next_state(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        b = board.copy()

        if action == b.get_action_size() - 1:
            b.pieces[2, -1] = 0
        else:
            b.execute_move(player, action)
        return b

    def change_perspective(self, board, player):
        board_changed = self._board.create_new_board()
        board_changed.pieces = board.pieces.copy() * player
        if player == -1:
            # swap score
            tmp = board_changed[0, -1] * player
            board_changed[0, -1] = board_changed[1, -1]* player
            board_changed[1, -1] = tmp
        return board_changed
