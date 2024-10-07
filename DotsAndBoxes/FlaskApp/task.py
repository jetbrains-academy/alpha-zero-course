import os
from abc import ABC

import torch
from flask import Flask, render_template, request, jsonify

from DotsAndBoxes.Board.task import BoardDandB
from DotsAndBoxes.Backend.task import Backend
from ResNetEstimator.Model.task import ResNet

args = {
    'C': 2,
    'num_searches': 60,
    'num_iterations': 3,
    'num_self_play_iterations': 100,
    'num_epochs': 25,
    'temperature': 1.25,
    'batch_size': 64,
}

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

# Constants for the game
SIZE_OF_WINDOW = 600
PLAYER1_COLOR = '#0492CF'  # Blue
PLAYER1_COLOR_LIGHT = '#67B0CF'  # Light Blue
PLAYER2_COLOR = '#EE4035'  # Red
PLAYER2_COLOR_LIGHT = '#EE7E77'  # Light Red


class FlaskApp(ABC):
    def __init__(self, backend):
        self.backend = backend

        self.number_of_dots = (self.backend.num_rows + self.backend.num_cols) // 2 + 1
        self.distance_between_dots = SIZE_OF_WINDOW / self.number_of_dots

        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/play_again', methods=['POST'])
        def play_again():
            self.backend.refresh()
            return jsonify(success=True)

        @self.app.route('/click', methods=['POST'])
        def click():
            is_cur_player1, edge_type, logical_position = None, None, []
            success = False
            data = request.json
            grid_position = [data['x'], data['y']]
            player1 = self.backend.player1
            player2 = self.backend.player2
            if (not self.backend.agent_play
                    or (self.backend.agent_play and self.backend.player1_turn)):
                if grid_position == [0, 0]:
                    self.backend.emulate_next_move = False
                else:
                    self.backend.emulate_next_move = True
                edge_type, logical_position = self.backend.convert_edge_to_logical_position(
                    grid_position,
                    self.distance_between_dots)
                if edge_type and not self.backend.is_edge_occupied(edge_type, logical_position):
                    is_cur_player1 = self.backend.player1_turn
                    success = True

                    self.backend.update_board(edge_type, logical_position)
                    action = self.backend.get_action_from(edge_type, logical_position)
                    self.backend.perform(action)
            elif self.backend.agent_play and not self.backend.player1_turn:
                is_cur_player1 = self.backend.player1_turn
                edge_type, logical_position = self.backend.agent_move()
                success = True
                if self.backend.is_gameover():
                    self.backend.emulate_next_move = False

            edge_data = {
                'edge_type': edge_type,
                'logical_position': logical_position
            }
            player_data = {
                'is_cur_player1': is_cur_player1,
                'player1_turn': self.backend.player1_turn,
                'player1_color': PLAYER1_COLOR,
                'player2_color': PLAYER2_COLOR,
                'player1_color_light': PLAYER1_COLOR_LIGHT,
                'player2_color_light': PLAYER2_COLOR_LIGHT,
                'player1': player1,
                'player2': player2,
                'player1_score': int(self.backend.get_board()[0, -1]),
                'player2_score': int(self.backend.get_board()[1, -1]),
                'emulate_click': self.backend.emulate_next_move
            }
            cell_data = {
                'cell_status': self.backend.cell_status.tolist()
            }
            return jsonify(success=success, edge_data=edge_data,
                           player_data=player_data, cell_data=cell_data)

    def run(self):
        model = ResNet(self.backend, 4, 64, device=device)
        model_num = args['num_iterations'] - 1
        filename = f'../TrainAndPlay/models/model_{model_num}.pt'

        if os.path.exists(filename):
            model.load_state_dict(torch.load(filename, map_location=device))
            model.eval()
            self.backend.agent = model
            self.backend.agent_play = True
            self.backend.player2 = "AlphaZero"

        self.app.run(debug=False, port=8080)


if __name__ == "__main__":
    game_backend = Backend(BoardDandB())
    app = FlaskApp(game_backend)
    app.run()
