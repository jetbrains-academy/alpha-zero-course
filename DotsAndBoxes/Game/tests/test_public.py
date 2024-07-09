import unittest

from TicTacToe.Game.task import TicTacToe
from DotsAndBoxes.Board.task import BoardDandB

from task import DotsAndBoxes


class TestDotsAndBoxes(unittest.TestCase):
    def setUp(self):
        self.board = BoardDandB()
        self.game = DotsAndBoxes(self.board)

    def test_get_next_state(self):
        # Test regular move
        returned_board = self.game.get_next_state(self.board, 1, 5)
        self.assertEqual(returned_board[1, 2], 1,
                         msg="The move should be executed correctly")

        # Test another move
        returned_board = self.game.get_next_state(returned_board, -1, 9)
        self.assertEqual(returned_board[3, 0], 1,
                         msg="The move of second player should be executed correctly")

    def test_change_perspective(self):
        # Mock the indices for simplicity in this test
        self.game._board[0, -1] = 1
        self.game._board[1, -1] = 2

        # Test perspective change for player -1
        changed_board = self.game.change_perspective(self.game._board, -1)
        self.assertEqual(changed_board[0, -1], 2,
                         msg="The score of player 1 should be 2 after perspective change")
        self.assertEqual(changed_board[1, -1], 1,
                         msg="The score of player 2 should be 1 after perspective change")

        # Ensure it returns the original when player is 1
        changed_board = self.game.change_perspective(self.game._board, 1)
        self.assertEqual(changed_board[0, -1], 1,
                         msg="The score of player 1 should be 1 after perspective change")
        self.assertEqual(changed_board[1, -1], 2,
                         msg="The score of player 2 should be 2 after perspective change")


if __name__ == '__main__':
    unittest.main()
