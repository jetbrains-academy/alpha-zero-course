from flask import Flask, render_template, request, jsonify

from DotsAndBoxesGPU.Board.task import BoardDandB
from DotsAndBoxesGPU.Visualization.task import DotsAndBoxesVisualization

app = Flask(__name__)

# Initialize the game board
board = BoardDandB()
game = DotsAndBoxesVisualization(board)

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
    data = request.json
    x, y = data['x'], data['y']
    player1 = game.player1
    player2 = game.player2
    edge_type, logical_position = game.convert_edge_to_logical_position([x, y])
    if edge_type and not game.is_edge_occupied(edge_type, logical_position):
        is_cur_player1 = game.player1_turn

        game.update_board(edge_type, logical_position)
        action = game.get_action_from(edge_type, logical_position)
        game.perform(action)

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
            'player2': player2
        }
        cell_data = {
            'cell_status': game.cell_status.tolist()
        }
        return jsonify(success=True, edge_data=edge_data,
                       player_data=player_data, cell_data=cell_data)
    return jsonify(success=False)


if __name__ == "__main__":
    app.run(debug=True)
