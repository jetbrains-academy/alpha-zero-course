import unittest
import numpy as np
from TicTacToe.Game.Game import TicTacToe


class TestCase(unittest.TestCase):
    def test_init(self):
        tictactoe = TicTacToe(4)
        board = tictactoe.get_board()
        self.assertEqual(16, board.pieces.size, msg="Board in TicTacToe(4) should have 16 cells")

    def test_next_state(self):
        tictactoe = TicTacToe()
        board = tictactoe.get_board()
        board = tictactoe.get_next_state(board, 1, 4)
        self.assertEqual(1, board[1, 1],
                         msg="get_next_state() after action 4 for player 1 should return board where [1,1] element == 1")

    def test_get_valid_moves(self):
        tictactoe = TicTacToe()
        board = tictactoe.get_board()
        board = tictactoe.get_next_state(board, 1, 0)
        board = tictactoe.get_next_state(board, -1, 1)
        board = tictactoe.get_next_state(board, 1, 2)
        valid_moves = tictactoe.get_valid_moves(board)
        actual_board = list(valid_moves)
        expected_board = [0, 0, 0, 1, 1, 1, 1, 1, 1]
        self.assertEqual(expected_board, actual_board,
                         msg="get_valid_moves() returns wrong list after players made their actions to 1st row")

    def test_get_game_ended(self):
        tictactoe = TicTacToe()
        board = tictactoe.get_board()
        board.pieces = np.array([[0, 0, 0],
                                 [0, 0, 0],
                                 [0, 0, 0]])
        self.assertEqual(0,
                         tictactoe.get_game_ended(board, 1),
                         msg="get_game_ended() should return 0 on start field")
        board.pieces = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [0, 0, 1]])
        self.assertEqual(1,
                         tictactoe.get_game_ended(board, 1),
                         msg="get_game_ended() not detected that 1 player is win")
        board.pieces = np.array([[1, 0, 0],
                                 [0, 1, 0],
                                 [0, 0, 1]])
        self.assertEqual(-1,
                         tictactoe.get_game_ended(board, -1),
                         msg="get_game_ended() not detected that -1 player is loose")
        board.pieces = np.array([[1, -1, 1],
                                 [1, -1, -1],
                                 [-1, 1, 1]])
        self.assertEqual(1e-4,
                         tictactoe.get_game_ended(board, -1),
                         msg="get_game_ended() not detected draw")

    def test_change_perspective(self):
        tictactoe = TicTacToe()
        board = tictactoe.get_board()
        board.pieces = np.array([[1, 0, 1],
                                 [0, 0, 0],
                                 [-1, 0, -1]])
        new_board = tictactoe.change_perspective(board, -1)
        actual = str(new_board)
        expected = 'O-O\n---\nX-X\n'
        self.assertEqual(expected,
                         actual,
                         msg="wrong change_perspective() work")

    def test_get_encoded_state(self):
        tictactoe = TicTacToe()
        board = tictactoe.get_board()
        board.pieces = np.array([[1, 0, 1],
                                 [0, 0, 0],
                                 [-1, 0, -1]])
        expected = np.stack(
            (board.pieces == -1, board.pieces == 0, board.pieces == 1)
        ).astype(np.float32)
        actual = tictactoe.get_encoded_state(board)
        self.assertTrue(np.array_equal(expected, actual),
                        msg=f"get_encoded_state result for {board.pieces}\nshould be: {expected},\nbut got {actual}")
