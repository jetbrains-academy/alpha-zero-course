import unittest
from copy import deepcopy

from MCTS.TreeNode.task import Node
from TicTacToe.GameImplementation.Game import TicTacToe


def _init_root():
    game = TicTacToe(size=2)
    args = {'C': 1.41, 'num_searches': 1}
    board = game.get_init_board()
    tree_node = Node(game, args, board)
    return tree_node


def _get_tree_with_one_node():
    root = _init_root()
    game = deepcopy(root.game)
    board = deepcopy(root.state)
    board = game.get_next_state(board, 1, 0)
    node = Node(game, root.args, board, parent=root, action_taken=0)
    root.children.append(node)

    return node


def _get_tree_with_two_nodes():
    node = _get_tree_with_one_node()
    game = deepcopy(node.game)
    board = deepcopy(node.state)
    board = game.get_next_state(board, -1, 1)
    node = Node(game, node.args, board, parent=node, action_taken=1)

    return node


def _get_tree_with_fully_expanded_node():
    root = _init_root()
    for i in root.expandable_moves:
        root.expand()
    return root


def _get_root_with_first_best_child():
    root = _get_tree_with_fully_expanded_node()
    root.children[0].value_sum = -100500
    for child in root.children:
        child.visit_count = 1

    return root


class TestCase(unittest.TestCase):
    def test_tree_node_init(self):
        root = _init_root()
        actual = root.expandable_moves.sum()
        self.assertEqual(actual, 4, msg=f"Wrong number of expandable moves. Expected: 4, actual: {actual}")

    def test_get_player(self):
        root = _init_root()
        self.assertEqual(root.get_player(), None)
        node_1 = _get_tree_with_one_node()
        self.assertEqual(node_1.get_player(), 1)
        node_2 = _get_tree_with_two_nodes()
        self.assertEqual(node_2.get_player(), -1)

    def test_expandable_moves(self):
        root = _get_tree_with_fully_expanded_node()
        self.assertEqual(root.is_fully_expanded(), True)
        self.assertEqual(root.children[0].is_fully_expanded(), False)

    def test_select(self):
        root = _get_root_with_first_best_child()
        self.assertEqual(root.select(), root.children[0])

    def test_expand(self):
        root = _init_root()
        root.expand()
        self.assertEqual(len(root.children), 1)
        for i in range(3):
            root.expand()
        self.assertEqual(len(root.children), 4)
        self.assertEqual(root.is_fully_expanded(), True)

    def test_backpropagate(self):
        root = _init_root()
        root.expand()
        value = 100
        root.children[0].backpropagate(value)
        self.assertEqual(root.children[0].value_sum, value)
        self.assertEqual(root.children[0].visit_count, 1)
        self.assertEqual(root.value_sum, -value)
        self.assertEqual(root.visit_count, 1)


