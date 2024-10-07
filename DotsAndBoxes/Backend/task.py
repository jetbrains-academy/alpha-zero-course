# Based on the source: https://github.com/aqeelanwar/Dots-and-Boxes
# Licence: MIT
from abc import ABC
from time import sleep
import numpy as np
import torch

from DotsAndBoxes.Game.task import DotsAndBoxes

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

class Backend(DotsAndBoxes, ABC):
    def __init__(self, board):
        super().__init__(board)

        self.num_rows = self._board._num_rows
        self.num_cols = self._board._num_cols

        self.player1 = "Player 1"
        self.player2 = "Player 2"
        self.agent = None
        self.agent_play = False

        self.player1_starts = True
        self.refresh()

    def refresh(self):
        self.cell_status = np.zeros(shape=(self.num_rows, self.num_cols))
        self.row_status = np.zeros(shape=(self.num_rows + 1, self.num_cols))
        self.col_status = np.zeros(shape=(self.num_rows, self.num_cols + 1))
        self._board = self._board.create_new_board()

        self.player1_turn = self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []

    def convert_edge_to_logical_position(self, edge_position, distance_between_dots):
        edge_position = np.array(edge_position)
        position = (edge_position - distance_between_dots / 4) // (distance_between_dots / 2)

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

        if r < 0 or c < 0 or r > self.num_rows or c > self.num_cols:
            return '', []
        if ((edge_type == 'row' and c == self.num_cols)
                or (edge_type == 'col' and r == self.num_rows)):
            return '', []
        return edge_type, logical_position

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
            action = r * self.num_cols + c
        else:
            action = self.num_cols * (self.num_rows + 1) + r * (self.num_cols + 1) + c
        return action

    def mark_boxes(self):
        """Mark the completed boxes on the board."""
        boxes = np.argwhere(self.cell_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                if not self.player1_turn:
                    self.cell_status[box[0], box[1]] = -4

    def update_board(self, edge_type, logical_position):
        """Update the board with the new edge."""
        r, c = logical_position
        if r < self.num_rows and c < self.num_cols:
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

    def perform(self, action):
        player = 1 if self.player1_turn else -1
        self._board = self.get_next_state(
            self.get_board(), player, action
        )
        if not self._board.is_pass_on():
            self.player1_turn = not self.player1_turn
        else:
            self._board.pieces[2, -1] = 0

    def convert_action_to_logical_position(self, action):
        is_horizontal = action < self.num_cols * (self.num_rows + 1)
        if is_horizontal:
            logical_position = [int(action / self.num_cols), int(action % self.num_cols)]
            edge_type = 'row'
        else:
            action -= self.num_cols * (self.num_rows + 1)
            logical_position = [int(action / (self.num_cols + 1)),
                                int(action % (self.num_cols + 1))]
            edge_type = 'col'
        return edge_type, logical_position

    def agent_move(self):
        """Handle the agent's move."""
        encoded_state = self.get_board().get_encoded_state()
        tensor_state = torch.tensor(encoded_state).unsqueeze(0).to(device)

        policy, value = self.agent(tensor_state)
        policy = (
            torch.softmax(policy, axis=1)
            .squeeze(0).detach().cpu().numpy()
        )
        valid_moves = self.get_board().get_valid_moves()
        policy *= valid_moves
        policy /= np.sum(policy)
        action = np.argmax(policy)
        sleep(0.05)
        edge_type, logical_position = self.convert_action_to_logical_position(action)
        self.update_board(edge_type, logical_position)
        self.perform(action)
        return edge_type, logical_position
