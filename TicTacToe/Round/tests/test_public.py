import unittest
import sys
import io

from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe
from TicTacToe.Round.task import Round


class TestCase(unittest.TestCase):
    def test_init(self):
        original_stdout = sys.stdout
        fake_stdout = io.StringIO()
        sys.stdout = fake_stdout
        try:
            board = Board()
            first_round = Round(TicTacToe(board))
            first_round.print_game_layout()
        finally:
            sys.stdout = original_stdout
        out = fake_stdout.getvalue()
        empty_field = '---\n---\n---\n'
        self.assertEqual(empty_field, out[:12], msg="Empty field expected to be printed first")
        valid_moves = 'valid_moves [0, 1, 2, 3, 4, 5, 6, 7, 8]'
        valid_moves_found = out.find(valid_moves) != -1
        self.assertTrue(valid_moves_found, msg=f"In output no valid moves list found: {out}")

    def test_game_draw(self):
        original_stdout = sys.stdout
        fake_stdout = io.StringIO()
        sys.stdout = fake_stdout
        try:
            inputs = [0, 1, 2, 3, 5, 4, 6, 8, 7]
            inputs.reverse()
            board = Board()
            first_round = Round(TicTacToe(board))
            is_playing = True
            while is_playing:
                first_round.print_game_layout()
                is_playing = first_round.play_game(inputs.pop())
        finally:
            sys.stdout = original_stdout
        out = fake_stdout.getvalue()
        correct_win = out.find('draw') != -1
        self.assertTrue(correct_win, msg=f"Expected draw, got {out}")

    def test_action_not_valid(self):
        original_stdout = sys.stdout
        fake_stdout = io.StringIO()
        sys.stdout = fake_stdout
        try:
            board = Board()
            first_round = Round(TicTacToe(board))
            first_round.print_game_layout()
            first_round.play_game(0)
            first_round.print_game_layout()
            first_round.play_game(0)
        finally:
            sys.stdout = original_stdout
        out = fake_stdout.getvalue()
        action_not_valid_found = out.find('action not valid') != -1
        self.assertTrue(action_not_valid_found,
                        msg=f"No \"action not valid\" message found after twice choosing zero action: {out} ")
