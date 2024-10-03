import unittest
from unittest.mock import MagicMock, patch
import numpy as np
from tkinter import Tk, Canvas

from DotsAndBoxes.Backend.task import Backend
from DotsAndBoxes.Board.task import BoardDandB

from task import TkinterApp, PLAYER1_COLOR, SIZE_OF_WINDOW


class TestTkinterApp(unittest.TestCase):
    def setUp(self):
        self.backend = Backend(BoardDandB())
        self.app = TkinterApp(self.backend)

        # Mocking Tkinter components
        self.app.window = MagicMock(spec=Tk)
        self.app.canvas = MagicMock(spec=Canvas)

    def test_emulate_click(self):
        with patch.object(self.app.canvas, 'event_generate') as mock_event_generate:
            self.app.emulate_click(100, 200)
            mock_event_generate.assert_called_with('<Button-1>', x=100, y=200)

    def test_make_edge(self):
        self.app.backend.player1_turn = True
        self.app.make_edge('row', [1, 1])

        start_x = self.app.distance_between_dots / 2 + 1 * self.app.distance_between_dots
        start_y = self.app.distance_between_dots / 2 + 1 * self.app.distance_between_dots
        end_x, end_y = start_x + self.app.distance_between_dots, start_y

        self.app.canvas.create_line.assert_called_with(start_x, start_y, end_x, end_y, fill=PLAYER1_COLOR,
                                                       width=self.app.edge_width)

    def test_display_turn_text(self):
        self.app.backend.player1_turn = True
        self.app.backend.player1 = "Player 1"
        self.app.backend.player2 = "Player 2"
        self.app.backend.turntext_handle = None

        self.app.display_turn_text()

        text = 'Next turn: Player 1'
        color = PLAYER1_COLOR
        self.app.canvas.create_text.assert_called_with(
            SIZE_OF_WINDOW - 5 * len(text),
            SIZE_OF_WINDOW - self.app.distance_between_dots / 8,
            font="cmr 15 bold", text=text, fill=color
        )

    def test_play_again(self):
        with patch.object(self.app, 'redraw_board') as mock_redraw_board, \
                patch.object(self.app.backend, 'refresh') as mock_refresh, \
                patch.object(self.app, 'display_turn_text') as mock_display_turn_text:
            self.app.play_again()

            self.app.canvas.delete.assert_called_with("all")
            mock_redraw_board.assert_called_once()
            mock_refresh.assert_called_once()
            mock_display_turn_text.assert_called_once()
            self.assertFalse(self.app.start_new_game)

    def test_click_start_new_game(self):
        with patch.object(self.app, 'play_again') as mock_play_again:
            self.app.start_new_game = True
            mock_event = MagicMock()
            self.app.click(mock_event)
            mock_play_again.assert_called_once()

    def test_click_emulate_move(self):
        self.app.backend.agent_play = False
        mock_event = MagicMock()
        mock_event.x, mock_event.y = 100, 200

        with patch.object(self.app.backend, 'convert_edge_to_logical_position') as mock_convert_edge, \
                patch.object(self.app.backend, 'is_edge_occupied', return_value=False) as mock_is_edge_occupied, \
                patch.object(self.app, 'draw_edge') as mock_draw_edge, \
                patch.object(self.app.backend, 'get_action_from') as mock_get_action_from, \
                patch.object(self.app.backend, 'perform') as mock_perform, \
                patch.object(self.app, 'display_turn_text') as mock_display_turn_text:
            mock_convert_edge.return_value = ('row', [1, 1])

            self.app.click(mock_event)

            mock_convert_edge.assert_called_with([100, 200], self.app.distance_between_dots)
            mock_is_edge_occupied.assert_called_with('row', [1, 1])
            mock_draw_edge.assert_called_with('row', [1, 1])
            mock_get_action_from.assert_called_with('row', [1, 1])
            mock_perform.assert_called_once()
            mock_display_turn_text.assert_called_once()


if __name__ == '__main__':
    unittest.main()
