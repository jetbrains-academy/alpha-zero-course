# Based on the source: https://github.com/aqeelanwar/Dots-and-Boxes
# Licence: MIT
from abc import ABC
from time import sleep
from tkinter import Tk, Canvas
import numpy as np
import torch
import threading

from DotsAndBoxesGPU.Board.task import BoardDandB
from DotsAndBoxesGPU.Game.task import DotsAndBoxes

# Constants
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


def is_main_thread():
    return threading.current_thread() == threading.main_thread()


class DotsAndBoxesVisualization(DotsAndBoxes, ABC):
    def __init__(self, board):
        super().__init__(board)
        self._num_rows = board._num_rows
        self._num_cols = board._num_cols

        NUMBER_OF_DOTS = (self._num_rows + self._num_cols) // 2 + 1
        self.dot_width = 0.15 * SIZE_OF_WINDOW / NUMBER_OF_DOTS
        self.edge_width = 0.06 * SIZE_OF_WINDOW / NUMBER_OF_DOTS
        self.distance_between_dots = SIZE_OF_WINDOW / NUMBER_OF_DOTS

        self.player1 = "Player 1"
        self.player2 = "Player 2"
        self.agent = None
        self.agent_play = False

        self.window = Tk()
        self.window.title('Dots & Boxes')
        self.canvas = Canvas(self.window, width=SIZE_OF_WINDOW, height=SIZE_OF_WINDOW)
        self.canvas.pack()
        self.window.bind(MAIN_BUTTON_NAME, self.click)
        self.player1_starts = True
        self.play_again()

    def emulate_click(self, x, y):
        self.canvas.event_generate(MAIN_BUTTON_NAME, x=x, y=y)

    def play_again(self):
        """Reset the game to play again."""
        if is_main_thread():
            self.refresh_board()
        self.cell_status = np.zeros(shape=(self._num_rows, self._num_cols))
        self.row_status = np.zeros(shape=(self._num_rows + 1, self._num_cols))
        self.col_status = np.zeros(shape=(self._num_rows, self._num_cols + 1))
        self._board = self._board.create_new_board()

        self.player1_turn = self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        if is_main_thread():
            self.display_turn_text()

    def run(self):
        """Start the Tkinter main loop."""
        self.window.mainloop()

    def is_edge_occupied(self, edge_type, logical_position):
        r, c = logical_position
        if edge_type == 'row':
            return self.row_status[r, c] == 1
        if edge_type == 'col':
            return self.col_status[r, c] == 1
        return True


    def get_action_from(self, edge_type, logical_position):
        r, c = logical_position
        if edge_type == 'row':
            action = r * self._num_cols + c
        else:
            action = self._num_cols*(self._num_rows + 1) + r*(self._num_cols + 1) + c
        return action

    def convert_edge_to_logical_position(self, edge_position):
        edge_position = np.array(edge_position)
        position = (edge_position - self.distance_between_dots / 4) // (self.distance_between_dots / 2)

        r, c = -1, -1
        edge_type, logical_position = '', []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int(position[1] // 2)
            c = int((position[0] - 1) // 2)
            logical_position = [r, c]
            edge_type = 'row'
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            r = int((position[1] - 1) // 2)
            c = int(position[0] // 2)
            logical_position = [r, c]
            edge_type = 'col'

        if r < 0 or c < 0 or r > self._num_rows or c > self._num_cols:
            return '', []
        if ((edge_type == 'row' and c == self._num_cols)
            or (edge_type == 'col' and r == self._num_rows)):
            return '', []
        return edge_type, logical_position

    def mark_box(self):
        """Mark the completed boxes on the board."""
        boxes = np.argwhere(self.cell_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                if self.player1_turn:
                    color = PLAYER1_COLOR_LIGHT
                else:
                    color = PLAYER2_COLOR_LIGHT
                    self.cell_status[*box] = -4
                self.shade_box(box, color)

    def update_board(self, edge_type, logical_position):
        """Update the board with the new edge."""
        r, c = logical_position
        if r < self._num_rows and c < self._num_cols:
            self.cell_status[r, c] += 1

        if edge_type == 'row':
            self.row_status[r, c] = 1
            if r > 0:
                self.cell_status[r - 1, c] += 1
        elif edge_type == 'col':
            self.col_status[r, c] = 1
            if c > 0:
                self.cell_status[r, c - 1] += 1

    def is_gameover(self):
        return np.all(self.row_status == 1) and np.all(self.col_status == 1)

    def make_edge(self, edge_type, logical_position):
        r, c = logical_position
        start_x = self.distance_between_dots / 2 + c * self.distance_between_dots
        start_y = self.distance_between_dots / 2 + r * self.distance_between_dots
        if edge_type == 'row':
            end_x, end_y = start_x + self.distance_between_dots, start_y
        else:
            end_x, end_y = start_x, start_y + self.distance_between_dots

        color = PLAYER1_COLOR if self.player1_turn else PLAYER2_COLOR
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=self.edge_width)

    def display_gameover(self):
        player1_score = len(np.argwhere(self.cell_status == 4))
        player2_score = len(np.argwhere(self.cell_status == -4))

        text, color = (f'Winner: {self.player1}', PLAYER1_COLOR) if player1_score > player2_score else (
            f'Winner: {self.player2}', PLAYER2_COLOR) if player2_score > player1_score else ('Its a tie', 'gray')

        self.canvas.delete("all")
        self.canvas.create_text(SIZE_OF_WINDOW / 2, SIZE_OF_WINDOW / 3, font="cmr 40 bold", fill=color, text=text)
        self.canvas.create_text(SIZE_OF_WINDOW / 2, 5 * SIZE_OF_WINDOW / 8, font="cmr 40 bold", fill=GREEN_COLOR,
                                text='Scores \n')
        score_text = f'{self.player1} : {player1_score}\n{self.player2} : {player2_score}\n'
        self.canvas.create_text(SIZE_OF_WINDOW / 2, 3 * SIZE_OF_WINDOW / 4, font="cmr 30 bold", fill=GREEN_COLOR,
                                text=score_text)
        self.canvas.create_text(SIZE_OF_WINDOW / 2, 15 * SIZE_OF_WINDOW / 16, font="cmr 20 bold", fill="gray",
                                text='Click to play again \n')
        self.reset_board = True

    def refresh_board(self):
        for i in range(self._num_rows + 1):
            x = i * self.distance_between_dots + self.distance_between_dots / 2
            self.canvas.create_line(x, self.distance_between_dots / 2,
                                    x, SIZE_OF_WINDOW - self.distance_between_dots / 2,
                                    fill='gray', dash=(2, 2))
        for j in range(self._num_cols + 1):
            y = j * self.distance_between_dots + self.distance_between_dots / 2
            self.canvas.create_line(self.distance_between_dots / 2, y,
                                    SIZE_OF_WINDOW - self.distance_between_dots / 2, y,
                                    fill='gray', dash=(2, 2))
        for i in range(self._num_rows + 1):
            for j in range(self._num_cols + 1):
                start_x = i * self.distance_between_dots + self.distance_between_dots / 2
                end_x = j * self.distance_between_dots + self.distance_between_dots / 2
                self.canvas.create_oval(start_x - self.dot_width / 2, end_x - self.dot_width / 2,
                                        start_x + self.dot_width / 2,
                                        end_x + self.dot_width / 2, fill=DOT_COLOR, outline=DOT_COLOR)

    def shade_box(self, box, color):
        start_x = self.distance_between_dots / 2 + box[1] * self.distance_between_dots + self.edge_width / 2
        start_y = self.distance_between_dots / 2 + box[0] * self.distance_between_dots + self.edge_width / 2
        end_x = start_x + self.distance_between_dots - self.edge_width
        end_y = start_y + self.distance_between_dots - self.edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def display_turn_text(self):
        text = f'Next turn: {self.player1 if self.player1_turn else self.player2}'
        color = PLAYER1_COLOR if self.player1_turn else PLAYER2_COLOR
        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(SIZE_OF_WINDOW - 5 * len(text),
                                                       SIZE_OF_WINDOW - self.distance_between_dots / 8,
                                                       font="cmr 15 bold", text=text, fill=color)

    def click(self, event):
        """Handle the click event."""
        if self.is_gameover() and not self.reset_board:
            self.canvas.delete("all")
            self.display_gameover()
            return
        if (not self.reset_board and
                (not self.agent_play
                 or (self.agent_play and self.player1_turn))):
            grid_position = [event.x, event.y]
            if grid_position == [0, 0]:
                self.emulate_next_move = False
            else:
                self.emulate_next_move = True
            edge_type, logical_position = self.convert_edge_to_logical_position(grid_position)
            if edge_type and not self.is_edge_occupied(edge_type, logical_position):
                self.update_board(edge_type, logical_position)
                self.draw_edge(edge_type, logical_position)
                self.perform(self.get_action_from(edge_type, logical_position))
            if self.agent_play and self.emulate_next_move:
                for _ in range(self._num_rows*self._num_cols):
                    self.emulate_click(0, 0)
        elif not self.reset_board and self.agent_play and not self.player1_turn:
            self.agent_move()
        elif self.reset_board:
            grid_position = [event.x, event.y]
            if grid_position != [0, 0]:
                self.canvas.delete("all")
                self.play_again()
                self.reset_board = False

    def perform(self, action):
        player = 1 if self.player1_turn else -1
        self._board = self.get_next_state(
            self.get_board(), player, action
        )
        if not self._board.is_pass_on():
            self.player1_turn = not self.player1_turn
            if is_main_thread():
                self.display_turn_text()
        else:
            self._board.pieces[2, -1] = 0

    def update(self):
        """Force Tkinter to draw everything"""
        self.window.update_idletasks()
        self.window.update()

    def draw_edge(self, edge_type, logical_position):
        """Draw the edge on the board."""
        self.make_edge(edge_type, logical_position)
        self.mark_box()
        self.refresh_board()
        self.update()

    def convert_action_to_logical_position(self, action):
        is_horizontal = action < self._num_cols * (self._num_rows + 1)
        if is_horizontal:
            logical_position = (int(action / self._num_cols), action % self._num_cols)
            edge_type = 'row'
        else:
            action -= self._num_cols * (self._num_rows + 1)
            logical_position = (int(action / (self._num_cols + 1)),
                               action % (self._num_cols + 1))
            edge_type = 'col'
        return edge_type, logical_position

    def agent_move(self):
        """Handle the agent's move."""
        encoded_state = self.get_board().get_encoded_state()
        tensor_state = torch.tensor(encoded_state).unsqueeze(0)

        policy, value = self.agent(tensor_state)
        policy = (
            torch.softmax(policy, axis=1)
            .squeeze(0).detach().cpu().numpy()
        )
        valid_moves = self.get_board().get_valid_moves()
        policy *= valid_moves
        policy /= np.sum(policy)
        action = np.argmax(policy)
        sleep(0.5)
        edge_type, logical_position = self.convert_action_to_logical_position(action)
        self.update_board(edge_type, logical_position)
        self.draw_edge(edge_type, logical_position)
        self.perform(action)
        sleep(0.5)


if __name__ == "__main__":
    game_instance = DotsAndBoxesVisualization(BoardDandB())
    game_instance.run()
