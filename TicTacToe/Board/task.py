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
      first dim is column , 2nd is row:
         pieces[0][0] is the top left square,
         pieces[2][0] is the bottom left square,
    Squares are stored and manipulated as (x,y) tuples.

    Based on the board for the game of TicTacToe by Evgeny Tyurin, github.com/evg-tyurin
    """
    def __init__(self, size: int = 3):
        """Set up initial board configuration"""
        self._size = size
        # Create the empty board array.
        self._pieces = np.array([[EMPTY] * size for _ in range(size)])

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
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def get_legal_moves(self) -> list:
        return [(x, y) for y in range(self.size) for x in range(self.size) if self[x][y] == EMPTY]

    def has_legal_moves(self) -> bool:
        return any(self[x, y] == EMPTY for y in range(self.size) for x in range(self.size))

    def is_win(self, player: int) -> bool:
        """Check whether the given player has collected a triplet in any direction"""
        return any(all(self[x, y] == player for x in range(self.size)) for y in range(self.size)) or \
            any(all(self[x, y] == player for y in range(self.size)) for x in range(self.size)) or \
            all(self[d, d] == player for d in range(self.size)) or \
            all(self[d, self.size - d - 1] == player for d in range(self.size))

    def execute_move(self, move: tuple, player: int):
        """Perform the given move on the board"""
        x, y = move
        assert self[x, y] == EMPTY
        self[x, y] = player

    def __str__(self):
        n = self.size

        board_str = []

        for y in range(n):
            # print the row
            for x in range(n):
                piece = self[y, x]
                if piece == 1:
                    board_str.append("X")
                elif piece == -1:
                    board_str.append("O")
                else:
                    board_str.append("-")
            board_str.append("\n")
        return "".join(board_str)
