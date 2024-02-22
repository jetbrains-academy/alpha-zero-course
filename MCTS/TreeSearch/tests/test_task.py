import unittest

from MCTS.TreeSearch.task import MCTS
from TicTacToe.GameImplementation.Game import TicTacToe


class TestCase(unittest.TestCase):
    def test_search(self):
        game = TicTacToe(size=2)
        board = game.get_init_board()
        board = game.get_next_state(board, 1, 0)
        mcts = MCTS(game, {'C': 1.41, 'num_searches': 1})
        probs = mcts.search(board)
        self.assertTrue(probs.max() - 1 < 0.01)

        mcts = MCTS(game, args={'C': 1.41, 'num_searches': 2})
        probs = mcts.search(board)
        self.assertTrue(probs.max() - 0.5 < 0.01)

        mcts = MCTS(game, args={'C': 1.41, 'num_searches': 100})
        probs = mcts.search(board)
        self.assertTrue(probs.min() - 0 < 0.01)

