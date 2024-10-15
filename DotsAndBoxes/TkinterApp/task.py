from abc import ABC
from time import sleep
from tkinter import Tk, Canvas

import numpy as np

from DotsAndBoxes.Backend.task import Backend
from DotsAndBoxes.Board.task import BoardDandB

SIZE_OF_WINDOW = 600
SYMBOL_SIZE = (SIZE_OF_WINDOW / 3 - SIZE_OF_WINDOW / 8) / 2
SYMBOL_THICKNESS = 50
DOT_COLOR = '#808080'  # Gray Color
PLAYER1_COLOR = '#0492CF'  # Blue
PLAYER1_COLOR_LIGHT = '#67B0CF'  # Light Blue
PLAYER2_COLOR = '#EE4035'  # Red
PLAYER2_COLOR_LIGHT = '#EE7E77'  # Light Red
GREEN_COLOR = '#7BC043'  # Green
MAIN_BUTTON_NAME = '<Button-1>'


class TkinterApp(ABC):
    def __init__(self, backend):
        self.backend = backend

        self.number_of_dots = (self.backend.num_rows + self.backend.num_cols) // 2 + 1
        self.dot_width = 0.15 * SIZE_OF_WINDOW / self.number_of_dots
        self.edge_width = 0.06 * SIZE_OF_WINDOW / self.number_of_dots
        self.distance_between_dots = SIZE_OF_WINDOW / self.number_of_dots

        self.window = Tk()
        self.window.title('Dots & Boxes')
        self.canvas = Canvas(self.window, width=SIZE_OF_WINDOW, height=SIZE_OF_WINDOW)
        self.canvas.pack()
        self.window.bind(MAIN_BUTTON_NAME, self.click)
        self.start_new_game = False
        self.emulate_next_move = False

    def emulate_click(self, x, y):
        self.canvas.event_generate(MAIN_BUTTON_NAME, x=x, y=y)

    def run(self):
        """Start the Tkinter main loop."""
        self.play_again()
        self.window.mainloop()

    def redraw_board(self):
        for i in range(self.backend.num_rows + 1):
            x = i * self.distance_between_dots + self.distance_between_dots / 2
            self.canvas.create_line(x, self.distance_between_dots / 2,
                                    x, SIZE_OF_WINDOW - self.distance_between_dots / 2,
                                    fill='gray', dash=(2, 2))
        for j in range(self.backend.num_cols + 1):
            y = j * self.distance_between_dots + self.distance_between_dots / 2
            self.canvas.create_line(self.distance_between_dots / 2, y,
                                    SIZE_OF_WINDOW - self.distance_between_dots / 2, y,
                                    fill='gray', dash=(2, 2))

        for i in range(self.backend.num_rows + 1):
            for j in range(self.backend.num_cols + 1):
                start_x = i * self.distance_between_dots + self.distance_between_dots / 2
                end_x = j * self.distance_between_dots + self.distance_between_dots / 2
                self.canvas.create_oval(start_x - self.dot_width / 2, end_x - self.dot_width / 2,
                                        start_x + self.dot_width / 2,
                                        end_x + self.dot_width / 2, fill=DOT_COLOR, outline=DOT_COLOR)

    def make_edge(self, edge_type, logical_position):
        r, c = logical_position
        start_x = self.distance_between_dots / 2 + c * self.distance_between_dots
        start_y = self.distance_between_dots / 2 + r * self.distance_between_dots
        if edge_type == 'row':
            end_x, end_y = start_x + self.distance_between_dots, start_y
        else:
            end_x, end_y = start_x, start_y + self.distance_between_dots

        color = PLAYER1_COLOR if self.backend.player1_turn else PLAYER2_COLOR
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=self.edge_width)

    def display_gameover(self):
        player1_score = len(np.argwhere(self.backend.cell_status == 4))
        player2_score = len(np.argwhere(self.backend.cell_status == -4))

        text, color = (f'Winner: {self.backend.player1}', PLAYER1_COLOR) if player1_score > player2_score else (
            f'Winner: {self.backend.player2}', PLAYER2_COLOR) if player2_score > player1_score else (
            'Its a tie', 'gray')

        self.canvas.delete("all")
        self.canvas.create_text(SIZE_OF_WINDOW / 2, SIZE_OF_WINDOW / 3, font="cmr 40 bold", fill=color, text=text)
        self.canvas.create_text(SIZE_OF_WINDOW / 2, 5 * SIZE_OF_WINDOW / 8, font="cmr 40 bold", fill=GREEN_COLOR,
                                text='Scores \n')
        score_text = f'{self.backend.player1} : {player1_score}\n{self.backend.player2} : {player2_score}\n'
        self.canvas.create_text(SIZE_OF_WINDOW / 2, 3 * SIZE_OF_WINDOW / 4, font="cmr 30 bold", fill=GREEN_COLOR,
                                text=score_text)
        self.canvas.create_text(SIZE_OF_WINDOW / 2, 15 * SIZE_OF_WINDOW / 16, font="cmr 20 bold", fill="gray",
                                text='Click to play again \n')
        self.start_new_game = True

    def shade_boxes(self):
        boxes = np.argwhere((self.backend.cell_status == 4) | (self.backend.cell_status == -4))
        for box in boxes:
            start_x = self.distance_between_dots / 2 + box[1] * self.distance_between_dots + self.edge_width / 2
            start_y = self.distance_between_dots / 2 + box[0] * self.distance_between_dots + self.edge_width / 2
            end_x = start_x + self.distance_between_dots - self.edge_width
            end_y = start_y + self.distance_between_dots - self.edge_width
            if self.backend.cell_status[box[0], box[1]] == 4:
                color = PLAYER1_COLOR_LIGHT
            else:
                color = PLAYER2_COLOR_LIGHT
            self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def display_turn_text(self):
        text = f'Next turn: {self.backend.player1 if self.backend.player1_turn else self.backend.player2}'
        color = PLAYER1_COLOR if self.backend.player1_turn else PLAYER2_COLOR
        self.canvas.delete(self.backend.turntext_handle)
        self.backend.turntext_handle = self.canvas.create_text(
            SIZE_OF_WINDOW - 5 * len(text),
            SIZE_OF_WINDOW - self.distance_between_dots / 8,
            font="cmr 15 bold", text=text, fill=color
        )

    def play_again(self):
        """Reset the game to play again."""
        self.canvas.delete("all")
        self.redraw_board()
        self.backend.refresh()
        self.display_turn_text()
        self.start_new_game = False

    def click(self, event):
        """Handle the click event."""
        if self.start_new_game:
            self.play_again()
            return
        if (not self.backend.agent_play or
                (self.backend.agent_play and self.backend.player1_turn)):
            grid_position = [event.x, event.y]
            if grid_position == [0, 0]:
                self.emulate_next_move = False
            else:
                self.emulate_next_move = True
            edge_type, logical_position = self.backend.convert_edge_to_logical_position(
                grid_position, self.distance_between_dots)
            if edge_type and not self.backend.is_edge_occupied(edge_type, logical_position):
                self.backend.update_board(edge_type, logical_position)
                self.draw_edge(edge_type, logical_position)
                self.backend.perform(self.backend.get_action_from(edge_type, logical_position))
                self.display_turn_text()

            if self.backend.agent_play and self.emulate_next_move:
                self.emulate_click(0, 0)

        elif self.backend.agent_play and not self.backend.player1_turn:
            edge_type, logical_position = self.backend.agent_move()
            self.draw_edge(edge_type, logical_position)
            self.display_turn_text()
            if self.emulate_next_move:
                self.emulate_click(0, 0)
        if self.backend.is_gameover():
            sleep(0.5)
            self.canvas.delete("all")
            self.display_gameover()
            return

    def update(self):
        """Force Tkinter to draw everything"""
        self.window.update_idletasks()
        self.window.update()

    def draw_edge(self, edge_type, logical_position):
        """Draw the edge on the board."""
        self.make_edge(edge_type, logical_position)
        self.backend.mark_boxes()
        self.shade_boxes()
        self.redraw_board()
        self.update()


def main():
    global app
    game_backend = Backend(BoardDandB())
    app = TkinterApp(game_backend)
    app.run()


if __name__ == "__main__":
    main()
