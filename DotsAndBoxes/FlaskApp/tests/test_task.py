import unittest
import json

from task import (FlaskApp, PLAYER1_COLOR, PLAYER2_COLOR,
                  PLAYER1_COLOR_LIGHT, PLAYER2_COLOR_LIGHT)

from DotsAndBoxes.Backend.task import Backend
from DotsAndBoxes.Board.task import BoardDandB


class DotsAndBoxesClickTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.game_backend = Backend(BoardDandB())
        self.app = FlaskApp(self.game_backend).app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        # Initialize the game state
        self.client.post('/play_again')

    def test_valid_click(self):
        # Simulate a valid click
        response = self.client.post('/click', data=json.dumps({'x': 300, 'y': 75}),
                                    content_type='application/json')
        data = json.loads(response.data)

        # Check if the response indicates success
        self.assertTrue(data['success'])
        self.assertIn('edge_data', data)
        self.assertIn('player_data', data)
        self.assertIn('cell_data', data)

        # Check if the correct player is updated
        self.assertEqual(data['player_data']['is_cur_player1'], True)
        self.assertEqual(data['player_data']['player1_turn'], self.game_backend.player1_turn)

    def test_invalid_click(self):
        # Simulate an invalid click (out of board area)
        response = self.client.post('/click', data=json.dumps({'x': 700, 'y': 700}),
                                    content_type='application/json')
        data = json.loads(response.data)

        # Check if the response indicates failure
        self.assertFalse(data['success'])

    def test_click_on_occupied_edge(self):
        # Simulate a valid click
        response = self.client.post('/click', data=json.dumps({'x': 300, 'y': 225}),
                                    content_type='application/json')
        data = json.loads(response.data)

        # Check if the response indicates success
        self.assertTrue(data['success'])

        # Simulate another click on the same spot
        response = self.client.post('/click', data=json.dumps({'x': 300, 'y': 225}),
                                    content_type='application/json')
        data = json.loads(response.data)

        # Check if the response indicates failure (edge already occupied)
        self.assertFalse(data['success'])


if __name__ == "__main__":
    unittest.main()
