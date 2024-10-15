import numpy as np

EMPTY = 0
WHITE = 1
BLACK = -1


class Board:
    """
    Board class for the game of TicTacToe.
    The default board size is 3x3.
    Board data:
      1=white(O), -1=black(X), 0=empty
      first dim is row, second is column:
         pieces[0][0] is the top left square,
         pieces[2][0] is the bottom left square,
    Squares are stored and manipulated as (x,y) tuples.

    Based on the board for the game of TicTacToe by Evgeny Tyurin, github.com/evg-tyurin
    """
    def __init__(self, num_rows: int = 3, num_cols: int = 3):
        """Set up the initial board configuration"""
        self._num_rows = num_rows
        self._num_cols = num_cols
        # Create an empty board (numpy 2-dimensional array)
        self._pieces = np.array([[EMPTY] * num_cols for _ in range(num_rows)])

    def get_board_size(self):
        return self._num_rows * self._num_cols

    def get_action_size(self):
        return self._num_rows * self._num_cols

    def create_new_board(self):
        return Board(self._num_rows, self._num_cols)

    def copy(self):
        """Create a deep copy of the board"""
        board = Board(self._num_rows, self._num_cols)
        board.pieces = np.copy(self.pieces)
        return board

    def __getitem__(self, index):
        i, j = index
        return self._pieces[i, j]

    def __setitem__(self, index, value):
        i, j = index
        self._pieces[i, j] = value

    @property
    def pieces(self):
        return self._pieces

    @pieces.setter
    def pieces(self, value):
        self._pieces = value

    @property
    def size(self):
        return self._num_cols

    def has_valid_moves(self) -> bool:
        return any(self[x, y] == EMPTY for y in range(self.size) for x in range(self.size))

    def get_valid_moves(self):
        return (self.pieces.reshape(-1) == 0).astype(np.uint8)

    def is_win(self, player: int) -> bool:
        """Check whether the given player has collected a triplet in any direction on a rectangular board"""
        num_rows, num_cols = self._num_rows, self._num_cols

        # Check horizontal lines
        for y in range(num_rows):
            for x in range(num_cols - 2):  # Only go up to num_cols-3 to start the triplet
                if all(self.pieces[y][x + i] == player for i in range(3)):
                    return True

        # Check vertical lines
        for x in range(num_cols):
            for y in range(num_rows - 2):  # Only go up to num_rows-3 to start the triplet
                if all(self.pieces[y + i][x] == player for i in range(3)):
                    return True

        # Check \ diagonals
        for y in range(num_rows - 2):
            for x in range(num_cols - 2):
                if all(self.pieces[y + i][x + i] == player for i in range(3)):
                    return True

        # Check / diagonals
        for y in range(2, num_rows):  # Start from row 2 to have at least three rows upwards
            for x in range(num_cols - 2):
                if all(self.pieces[y - i][x + i] == player for i in range(3)):
                    return True

        return False

    def execute_move(self, player: int, action: int):
        """Perform the given action on the board"""
        x, y = action // self._num_rows, action % self._num_cols
        assert self[x, y] == EMPTY
        self[x, y] = player

    def __str__(self):
        board_str = []
        for x in range(self._num_rows):
            for y in range(self._num_cols):
                piece = self[x, y]
                if piece == WHITE:
                    board_str.append("X")
                elif piece == BLACK:
                    board_str.append("O")
                elif piece == EMPTY:
                    board_str.append("-")
            board_str.append("\n")
        return "".join(board_str)

    def get_encoded_state(self):
        encoded_state = np.stack(
            (self.pieces == BLACK,
             self.pieces == EMPTY,
             self.pieces == WHITE)
        ).astype(np.float32)
        return encoded_state

    def get_player(self, action):
        row = action // self.size
        column = action % self.size
        return self[row, column]
