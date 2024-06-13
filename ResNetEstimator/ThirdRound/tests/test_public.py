import unittest
import numpy as np

from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe
from TicTacToe.Round.task import Round

from task import init_and_apply_nn


class TestInitAndApplyNN(unittest.TestCase):
    def setUp(self):
        self.round = Round(TicTacToe(Board()))
        self.round.play_game(2)
        self.round.play_game(7)

    def test_output_shapes_and_types(self):
        value, policy_probs = init_and_apply_nn(self.round)

        self.assertIsInstance(value, float,
                              msg="Type of value is not float.")

        self.assertIsInstance(policy_probs, np.ndarray,
                              msg="Type of policy_probs is not a numpy array.")

        expected_shape = self.round.instance_of_game.get_board().get_action_size()
        self.assertEqual(policy_probs.shape[0], expected_shape,
                         msg="The shape of policy_probs is unexpected.")

    def test_value_range(self):
        value, _ = init_and_apply_nn(self.round)
        self.assertTrue(-1 <= value <= 1,
                        msg="Value is not in the expected range (-1, 1)")

    def test_policy_probs_sum_to_one(self):
        _, policy_probs = init_and_apply_nn(self.round)
        self.assertAlmostEqual(policy_probs.sum(), 1, places=5,
                               msg="Policy probabilities don't sum up to 1.")


if __name__ == '__main__':
    unittest.main()
