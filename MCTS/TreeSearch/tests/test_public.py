import unittest

from MCTS.TreeSearch.task import MCTS
from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe


class TestCase(unittest.TestCase):
    def test_search(self):
        board = Board(3, 3)
        game = TicTacToe(board)
        board = game.get_next_state(board, 1, 0)
        mcts = MCTS(game, {'C': 1.41, 'num_searches': 1})
        probs = mcts.search(board.copy())
        self.assertTrue(probs.max() - 1 < 0.01,
                        msg=f"[Board size = 2] Expected max probability after one search: 1, actual: {probs.max()}")

        mcts = MCTS(game, args={'C': 1.41, 'num_searches': 2})
        probs = mcts.search(board.copy())
        self.assertTrue(probs.max() - 0.5 < 0.01,
                        msg=f"[Board size = 2] Expected max probability after two searches: 0.5, actual: {probs.max()}")

        mcts = MCTS(game, args={'C': 1.41, 'num_searches': 100})
        probs = mcts.search(board.copy())
        self.assertTrue(probs.min() - 0 < 0.01,
                        msg=f"[Board size = 2] Expected min probability after three searches: 0, actual: {probs.min()}")

