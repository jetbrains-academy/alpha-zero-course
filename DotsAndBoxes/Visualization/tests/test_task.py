import unittest
from unittest.mock import MagicMock

from task import (DotsAndBoxesVisualization, PLAYER1_COLOR_LIGHT)

from DotsAndBoxes.Board.task import BoardDandB


class TestDotsAndBoxesVisualization(unittest.TestCase):
    def setUp(self):
        self.game = DotsAndBoxesVisualization(BoardDandB())

    def test_is_edge_occupied(self):
        self.game.row_status[1][1] = 1
        self.assertTrue(self.game.is_edge_occupied('row', [1, 1]))
        self.assertFalse(self.game.is_edge_occupied('row', [0, 0]))

        self.game.col_status[1][1] = 1
        self.assertTrue(self.game.is_edge_occupied('col', [1, 1]))
        self.assertFalse(self.game.is_edge_occupied('col', [0, 0]))

    def test_get_action_from_row(self):
        # Test getting action from row edge
        edge_type = 'row'
        logical_position = (1, 2)
        expected_action = 1 * self.game._num_cols + 2
        action = self.game.get_action_from(edge_type, logical_position)
        self.assertEqual(action, expected_action, f"Expected {expected_action} but got {action}")

    def test_get_action_from_col(self):
        # Test getting action from col edge
        edge_type = 'col'
        logical_position = (1, 2)
        expected_action = (self.game._num_cols * (self.game._num_rows + 1) +
                           1 * (self.game._num_cols + 1) + 2)
        action = self.game.get_action_from(edge_type, logical_position)
        self.assertEqual(action, expected_action, f"Expected {expected_action} but got {action}")

    def test_update_board(self):
        self.game.update_board('row', [1, 1])
        self.assertEqual(self.game.row_status[1][1], 1)
        self.assertEqual(self.game.cell_status[1][1], 1)

        self.game.update_board('col', [1, 1])
        self.assertEqual(self.game.col_status[1][1], 1)
        self.assertEqual(self.game.cell_status[1][1], 2)

        self.game.update_board('row', [1, 0])
        self.assertEqual(self.game.row_status[1][0], 1)
        self.assertEqual(self.game.cell_status[0][0], 1)
        self.assertEqual(self.game.cell_status[0][1], 1)

    def test_shade_box(self):
        # Mocking the Canvas method
        self.game.canvas.create_rectangle = MagicMock()

        self.game.shade_box([1, 1], PLAYER1_COLOR_LIGHT)
        start_x = self.game.distance_between_dots / 2 + 1 * self.game.distance_between_dots + self.game.edge_width / 2
        start_y = self.game.distance_between_dots / 2 + 1 * self.game.distance_between_dots + self.game.edge_width / 2
        end_x = start_x + self.game.distance_between_dots - self.game.edge_width
        end_y = start_y + self.game.distance_between_dots - self.game.edge_width

        self.game.canvas.create_rectangle.assert_called_once_with(start_x, start_y, end_x, end_y,
                                                                  fill=PLAYER1_COLOR_LIGHT, outline='')


if __name__ == "__main__":
    unittest.main()
