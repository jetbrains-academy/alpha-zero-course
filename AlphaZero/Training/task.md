## Implementing Training in AlphaZero for TicTacToe

### Objectives:
1. **Self-Play (`self_play`):** Develop a method that simulates games of TicTacToe where the AI plays against itself. This process should generate valuable data (game states, action probabilities, and outcomes) for training the neural network. Use the MCTS algorithm to explore possible moves and select actions based on a temperature-adjusted strategy.
2. **Training (`train`):** Implement a method to train the neural network model using the data collected from self-play. Your training process should update the model to better predict action probabilities and game outcomes (win/loss/draw), thereby improving the AI's decision-making in future games.

### 1. `Self-Play` method
  - Simulate complete games of TicTacToe by alternating moves between two AI players until the game ends
  - For each move, generate action probabilities using the MCTS algorithm, apply temperature scaling, and randomly select an action based on these adjusted probabilities
  - Collect and return game data including states, action probabilities, and the final outcome for each move

### 2. `Training` method
  - Shuffle the collected game data to prepare for batch training
  - Process the data in batches, converting game states into tensors suitable for neural network input, along with corresponding action probability and outcome targets
  - Calculate loss for both action probabilities and game outcomes, backpropagate errors, and update the model using gradient descent
