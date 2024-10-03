import unittest

from task import Backend

from DotsAndBoxes.Board.task import BoardDandB


class TestDotsAndBoxesBackend(unittest.TestCase):
    def setUp(self):
        self.game_backend = Backend(BoardDandB())

    def test_is_edge_occupied(self):
        self.game_backend.row_status[1][1] = 1
        self.assertTrue(self.game_backend.is_edge_occupied('row', [1, 1]))
        self.assertFalse(self.game_backend.is_edge_occupied('row', [0, 0]))

        self.game_backend.col_status[1][1] = 1
        self.assertTrue(self.game_backend.is_edge_occupied('col', [1, 1]))
        self.assertFalse(self.game_backend.is_edge_occupied('col', [0, 0]))

    def test_get_action_from_row(self):
        # Test getting action from row edge
        edge_type = 'row'
        logical_position = (1, 2)
        expected_action = 1 * self.game_backend.num_cols + 2
        action = self.game_backend.get_action_from(edge_type, logical_position)
        self.assertEqual(action, expected_action, f"Expected {expected_action} but got {action}")

    def test_get_action_from_col(self):
        # Test getting action from col edge
        edge_type = 'col'
        logical_position = (1, 2)
        expected_action = (self.game_backend.num_cols * (self.game_backend.num_rows + 1) +
                           1 * (self.game_backend.num_cols + 1) + 2)
        action = self.game_backend.get_action_from(edge_type, logical_position)
        self.assertEqual(action, expected_action, f"Expected {expected_action} but got {action}")

    def test_update_board(self):
        self.game_backend.update_board('row', [1, 1])
        self.assertEqual(self.game_backend.row_status[1][1], 1)
        self.assertEqual(self.game_backend.cell_status[1][1], 1)

        self.game_backend.update_board('col', [1, 1])
        self.assertEqual(self.game_backend.col_status[1][1], 1)
        self.assertEqual(self.game_backend.cell_status[1][1], 2)

        self.game_backend.update_board('row', [1, 0])
        self.assertEqual(self.game_backend.row_status[1][0], 1)
        self.assertEqual(self.game_backend.cell_status[0][0], 1)
        self.assertEqual(self.game_backend.cell_status[0][1], 1)


if __name__ == "__main__":
    unittest.main()
