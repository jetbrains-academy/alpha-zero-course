import os

import torch
from flask import Flask, render_template, request, jsonify

from DotsAndBoxesGPU.Board.task import BoardDandB
from DotsAndBoxesGPU.TrainAndPlay.main import args
from DotsAndBoxesGPU.Visualization.task import DotsAndBoxesVisualization
from ResNetEstimator.Model.task import ResNet

app = Flask(__name__)

# Initialize the game board
board = BoardDandB()
game = DotsAndBoxesVisualization(board)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = ResNet(game, 4, 64, device=device)
model_num = args['num_iterations'] - 1
filename = f'../TrainAndPlay/models/model_{model_num}.pt'

if os.path.exists(filename):
    model.load_state_dict(torch.load(filename, map_location=device))
    model.eval()
    game.agent = model
    game.agent_play = True
    game.player2 = "AlphaZero"

# Constants for the game
NUM_ROWS = board._num_rows
NUM_COLS = board._num_cols
PLAYER1_COLOR = '#0492CF'  # Blue
PLAYER1_COLOR_LIGHT = '#67B0CF'  # Light Blue
PLAYER2_COLOR = '#EE4035'  # Red
PLAYER2_COLOR_LIGHT = '#EE7E77'  # Light Red


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/play_again', methods=['POST'])
def play_again():
    game.play_again()
    return jsonify(success=True)


@app.route('/click', methods=['POST'])
def click():
    is_cur_player1, edge_type, logical_position = None, None, []
    success = False
    data = request.json
    grid_position = [data['x'], data['y']]
    player1 = game.player1
    player2 = game.player2
    if (not game.agent_play
             or (game.agent_play and game.player1_turn)):
        if grid_position == [0, 0]:
            game.emulate_next_move = False
        else:
            game.emulate_next_move = True
        edge_type, logical_position = game.convert_edge_to_logical_position(grid_position)
        if edge_type and not game.is_edge_occupied(edge_type, logical_position):
            is_cur_player1 = game.player1_turn
            success = True

            game.update_board(edge_type, logical_position)
            action = game.get_action_from(edge_type, logical_position)
            game.perform(action)
    elif game.agent_play and not game.player1_turn:
        is_cur_player1 = game.player1_turn
        success = True
        edge_type, logical_position = game.agent_move()

    edge_data = {
        'edge_type': edge_type,
        'logical_position': logical_position
    }
    player_data = {
        'is_cur_player1': is_cur_player1,
        'player1_turn': game.player1_turn,
        'player1_color': PLAYER1_COLOR,
        'player2_color': PLAYER2_COLOR,
        'player1': player1,
        'player2': player2,
        'emulate_click': game.emulate_next_move
    }
    cell_data = {
        'cell_status': game.cell_status.tolist()
    }
    return jsonify(success=success, edge_data=edge_data,
                   player_data=player_data, cell_data=cell_data)


if __name__ == "__main__":
    app.run(debug=False, port=8080)
