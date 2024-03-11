import unittest
from unittest.mock import MagicMock
import numpy as np

from task import Node


class TestNode(unittest.TestCase):
    def setUp(self):
        self.mock_game = MagicMock()
        self.mock_board_state = MagicMock()
        self.mock_board_state.pieces = np.zeros((3, 3))
        self.args = {'C': 1.4}  # Example hyperparameter for UCB calculation

        # Mocking game methods
        self.mock_game.get_valid_moves.return_value = np.array([1, 0, 0, 1, 1, 0, 0, 1, 1])
        self.mock_game.get_next_state = MagicMock(return_value=self.mock_board_state)
        self.mock_game.change_perspective = MagicMock(return_value=self.mock_board_state)
        self.mock_game.size = 3

    def test_get_ucb_unvisited_child(self):
        parent_node = Node(self.mock_game, self.args, self.mock_board_state)
        parent_node.visit_count = 1
        child_node = Node(self.mock_game, self.args, self.mock_board_state,
                          parent=parent_node, action_taken=0, prior=0.5)
        parent_node.children.append(child_node)

        # For an unvisited child, the UCB should be influenced only by the prior and exploration term
        ucb = parent_node.get_ucb(child_node)
        self.assertTrue(
            ucb > 0,
            msg="For an unvisited child, the UCB should be influenced only by the prior and exploration term")

    def test_expand(self):
        policy = [0.1, 0, 0.2, 0, 0.3, 0, 0.4, 0, 0]
        parent_node = Node(self.mock_game, self.args, self.mock_board_state)

        parent_node.expand(policy)

        # Verify that children are created for actions with positive probability
        # Only four actions have non-zero probability
        self.assertEqual(len(parent_node.children), 4,
                         msg="Verify that children are created for actions with positive probability")

        # Check that children's priors match the policy
        for child in parent_node.children:
            self.assertIn(child.prior, policy,
                          msg="Check that children's priors match the policy")


if __name__ == '__main__':
    unittest.main()
