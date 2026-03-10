import numpy as np

from TicTacToe.Board.task import Board

EMPTY = 0
WHITE = 1
BLACK = -1


class BoardC4(Board):
    """
    Board data:
      1=white(O), -1=black(X), 0=empty
      first dim is column, second is row, so by default:
         pieces[0][0] is the top left square,
         pieces[5][0] is the bottom left square,
    Squares are stored and manipulated as (x,y) tuples.

    Based on the board for the game of TicTacToe by Evgeny Tyurin, github.com/evg-tyurin
    """

    def __init__(self, num_rows: int = 6, num_cols: int = 7):
        """Set up initial board configuration"""
        super().__init__(num_rows, num_cols)
        self._in_a_row = 4

    def get_board_size(self):
        return self._num_rows * self._num_cols

    def get_action_size(self):
        return self._num_cols

    def create_new_board(self):
        return BoardC4(self._num_rows, self._num_cols)

    def copy(self):
        """Create a deep copy of the board"""
        board = BoardC4(self._num_rows, self._num_cols)
        board.pieces = np.copy(self.pieces)
        return board

    def has_valid_moves(self) -> bool:
        return any(self[0, y] == EMPTY for y in range(self._num_cols))

    def get_valid_moves(self):
        """Should return a uint8 binary mask as numpy array of shape (num_cols,)"""
        return (self._pieces[0] == 0).astype(np.uint8)

    def is_win(self, player: int) -> bool:
        # Horizontal check
        for x in range(self._num_rows):
            for y in range(self._num_cols - 3):  # -3 accounts for the last possible starting point
                if all(self[x, y + i] == player for i in range(4)):
                    return True

        # Vertical check
        for y in range(self._num_cols):
            for x in range(self._num_rows - 3):  # -3 accounts for the last possible starting point
                if all(self[x + i, y] == player for i in range(4)):
                    return True

        # Positive diagonal check
        for x in range(self._num_rows - 3):
            for y in range(self._num_cols - 3):
                if all(self[x + i, y + i] == player for i in range(4)):
                    return True

        # Negative diagonal check
        for x in range(3, self._num_rows):  # Starts from 3 to ensure there are enough spaces for a diagonal
            for y in range(self._num_cols - 3):
                if all(self[x - i, y + i] == player for i in range(4)):
                    return True

        return False

    def execute_move(self, player: int, action: int):
        """Perform the given action on the board"""
        row = np.max(np.where(self[:, action] == 0))
        assert self[row, action] == EMPTY
        self[row, action] = player
