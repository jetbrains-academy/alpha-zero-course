import unittest
import numpy as np
from TicTacToe.Round.task import Round

from task import init_and_apply_nn


class TestInitAndApplyNN(unittest.TestCase):
    def setUp(self):
        self.round = Round()
        self.round.play_game(2)
        self.round.play_game(7)

    def test_output_shapes_and_types(self):
        value, policy_probs = init_and_apply_nn(self.round)

        # Check if value is a float
        self.assertIsInstance(value, float)

        # Check if policy_probs is a numpy array
        self.assertIsInstance(policy_probs, np.ndarray)

        # Check the shape of policy_probs
        expected_shape = self.round.tictactoe.get_action_size()
        self.assertEqual(policy_probs.shape[0], expected_shape)

    def test_value_range(self):
        value, _ = init_and_apply_nn(self.round)
        # Check that value is in the expected range (-1, 1)
        self.assertTrue(-1 <= value <= 1)

    def test_policy_probs_sum_to_one(self):
        _, policy_probs = init_and_apply_nn(self.round)
        # Check if the probabilities sum to 1
        self.assertAlmostEqual(policy_probs.sum(), 1, places=5)


if __name__ == '__main__':
    unittest.main()
