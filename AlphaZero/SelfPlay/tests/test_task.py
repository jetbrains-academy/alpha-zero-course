import unittest
from unittest.mock import MagicMock
import numpy as np

from task import AlphaZero


class TestAlphaZero(unittest.TestCase):
    def setUp(self):
        self.mock_model = MagicMock()
        self.mock_optimizer = MagicMock()
        self.mock_game = MagicMock()
        self.mock_state = MagicMock()
        self.args = {'num_iterations': 1, 'num_self_play_iterations': 1, 'num_epochs': 1}

        # Mocking the game and MCTS outputs
        self.mock_game.size = 3
        self.mock_game.get_action_size.return_value = 9
        self.mock_game.get_opponent.return_value = -1
        self.mock_game.get_game_ended.return_value = 1
        self.mock_game.change_perspective = lambda board, player: board
        self.mock_game.get_next_state.return_value = self.mock_state

        # Setting up AlphaZero with mocked components
        self.az = AlphaZero(self.mock_model, self.mock_optimizer, self.mock_game, self.args)
        self.az.mcts.search = MagicMock(return_value=np.ones(9) / 9)  # Uniform probability distribution

    def test_self_play_memory_structure(self):
        memory = self.az.self_play_random()

        # Check if memory is not empty
        self.assertTrue(len(memory) > 0, msg="Check if memory is not empty")

        # Validate the structure of memory entries
        for state, probs, outcome in memory:
            self.assertIsInstance(state, np.ndarray, msg="Check if state is ndarray")
            self.assertEqual(state.shape, (3, 3, 3), msg="Check if state has shape (3,3)")
            self.assertIsInstance(probs, np.ndarray, msg="Check if probs is ndarray")
            self.assertEqual(probs.shape, (9,), msg="Check if probs has shape (9,)")


if __name__ == '__main__':
    unittest.main()
