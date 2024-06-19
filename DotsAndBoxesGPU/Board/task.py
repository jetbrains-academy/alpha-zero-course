import numpy as np

from TicTacToe.Board.task import Board

EMPTY = 0
WHITE = 1
BLACK = -1


class BoardDandB(Board):
    """
    Board data: the representation of the board in Dots and Boxes
    differs from the one in TicTacToe and Connect Four.
    Here we have cells, abd aslo horizontal and vertical lines,
    and their amount is different in one row.
    For example, a 3x3 cells board (that corresponds to 4x4 dots)
    has 3 horizontal and 4 vertical lines in each of three rows.
    So the lines of the board are represented as a 2D array of size (2*num_rows + 1) x (num_cols + 1).
    The first half of the rows represents the horizontal lines,
    and the second half represents the vertical lines.
    The last column in the first half is used to store three additional numbers:
    the scores of each player and the pass state.
    """
    def __init__(self, num_rows: int = 3, num_cols: int = 3):
        super().__init__(num_rows, num_cols)
        self.pieces = np.array([[EMPTY]*(num_cols + 1) for _ in range(2*num_rows + 1)])

    def get_board_size(self):
        return (2*self._num_rows + 1)*(self._num_cols + 1)

    def get_action_size(self):
        # add 1 for pass move
        return 2*self._num_rows*(self._num_cols + 1) + 1

    def create_new_board(self):
        return BoardDandB(self._num_rows, self._num_cols)

    def copy(self):
        """Create a deep copy of the board"""
        board = BoardDandB(self._num_rows, self._num_cols)
        board.pieces = np.copy(self.pieces)
        return board

    def increase_score(self, score, player):
        if player == 1:
            self.pieces[0, -1] += score
        else:
            self.pieces[1, -1] += score

    def is_pass_on(self):
        return self.pieces[2, -1] != 0

    def toggle_pass(self, player):
        self.pieces[2, -1] = player

    def is_win(self, player: int) -> bool:
        # return 0 if not ended,
        # 1 if player 1 won,
        # -1 if player 1 lost

        if self.has_valid_moves():
            return False

        if self[0, -1] == self[1, -1]:
            return bool(-1 * player)
        else:
            player_1_won = self[0, -1] > self[1, -1]
            return bool(1*player if player_1_won else -1*player)

    def has_valid_moves(self):
        is_board_full = (np.all(self.pieces[:self._num_rows+1, :-1]) and
                         np.all(self.pieces[-self._num_rows:, :]))
        return not is_board_full

    def get_valid_moves(self):
        """Returns all the valid moves"""
        valid_moves = np.logical_not(self.pieces)
        valid_moves = np.hstack(
            (valid_moves[:self._num_rows + 1, :-1].flatten(),
             valid_moves[-self._num_rows:, :].flatten(), False)
        )
        if self.is_pass_on():
            valid_moves[:] = False
            valid_moves[-1] = True
        return valid_moves

    def execute_move(self, player, action):
        """
            Perform the given move on the board;
            color gives the color of the piece to play (1=white,-1=black)
        """
        # it shouldn't be a pass
        assert self.pieces[2, -1] == 0

        is_horizontal = action < self._num_cols * (self._num_rows + 1)
        if is_horizontal:
            move = (int(action / self._num_cols), action % self._num_cols)
        else:
            action -= self._num_cols * (self._num_rows + 1)
            move = (int(action / (self._num_cols + 1)) + self._num_rows + 1, action % (self._num_cols + 1))

        (x, y) = move

        # Add the piece to the empty square.
        assert self[x, y] == 0
        self[x, y] = 1  # The color doesn't matter

        # Need to check if we have closed a square
        # If so, increase score and mark pass
        horizontal = np.zeros((self._num_rows + 3, self._num_cols + 2))
        horizontal[1:-1, 1:-1] = self.pieces[:self._num_rows + 1, :self._num_cols]

        vertical = np.zeros((self._num_rows + 2, self._num_cols + 3))
        vertical[1:-1, 1:-1] = self.pieces[-self._num_rows:, :]

        score = 0
        if is_horizontal:
            x += 1
            y += 1
            if horizontal[x + 1, y]:
                score += (vertical[x, y] and vertical[x, y + 1])
            if horizontal[x - 1, y]:
                score += (vertical[x - 1, y] and vertical[x - 1, y + 1])
        else:
            x = x - self._num_rows
            y += 1
            if vertical[x, y + 1]:
                score += (horizontal[x, y] and horizontal[x + 1, y])
            if vertical[x, y - 1]:
                score += (horizontal[x, y - 1] and horizontal[x + 1, y - 1])

        self.increase_score(score, player)
        if score > 0:
            self.toggle_pass(player)

    def get_player(self, action):
        if action == self.get_action_size()-1:
            return self.pieces[2, -1]

        is_horizontal = action < self._num_cols * (self._num_rows + 1)
        if is_horizontal:
            move = (int(action / self._num_cols), action % self._num_cols)
        else:
            action -= self._num_cols * (self._num_rows + 1)
            move = (int(action / (self._num_cols + 1)) + self._num_rows + 1, action % (self._num_cols + 1))
        return self[move]

    def __str__(self):
        board_str = []
        for i in range(self._num_rows+1):
            for j in range(self._num_cols):
                s = "*-x-" if self.pieces[i, j] else "*---"
                board_str.append(s)
            board_str.append("*\n")
            if i < self._num_rows:
                for j in range(self._num_cols+1):
                    s = "x   " if self.pieces[i + self._num_rows+1, j] else "|   "
                    board_str.append(s)
            board_str.append("\n")

        board_str.extend(f"Pass: {self.pieces[2, -1]}\n")
        board_str.extend(f"Score {self.pieces[0, -1]} x {self.pieces[1, -1]}\n")
        return "".join(board_str)
