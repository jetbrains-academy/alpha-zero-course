import numpy as np
import unittest

from TicTacToe.Board.task import Board
from TicTacToe.Game.task import TicTacToe

from task import Node

board_for_test = np.array([
    [0, 1, -1],
    [0, 0, -1],
    [1, 0, 0],
])


class TestNode(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe(Board())
        self.game.get_board().pieces = board_for_test
        self.mock_board_state = self.game.get_board()
        self.args = {'C': 1.4}  # Example hyperparameter for UCB calculation

    def test_get_ucb_unvisited_child(self):
        parent_node = Node(self.game, self.args, self.mock_board_state)
        parent_node.visit_count = 1
        child_node = Node(self.game, self.args, self.mock_board_state,
                          parent=parent_node, action_taken=0, prior=0.5)
        parent_node.children.append(child_node)

        # For an unvisited child, the UCB should be influenced only by the prior and exploration term
        ucb = parent_node.get_ucb(child_node)
        self.assertTrue(
            ucb > 0,
            msg="For an unvisited child, the UCB should be influenced only by the prior and exploration term")

    def test_expand(self):
        policy = [0.1, 0, 0, 0.2, 0.3, 0, 0, 0.2, 0.2]
        parent_node = Node(self.game, self.args, self.mock_board_state)

        parent_node.expand(policy)

        # Verify that children are created for actions with positive probability
        # Only five actions have non-zero probability
        self.assertEqual(len(parent_node.children), 5,
                         msg="Verify that children are created for actions with positive probability")

        # Check that children's priors match the policy
        for child in parent_node.children:
            self.assertIn(child.prior, policy,
                          msg="Check that children's priors match the policy")


if __name__ == '__main__':
    unittest.main()
