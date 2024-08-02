Your next task is to enhance the AlphaZero class by implementing two critical methods: `self_play_random` and `learn`. These methods are pivotal for training the AlphaZero algorithm on the game of TicTacToe, leveraging Monte Carlo Tree Search (MCTS) and deep learning.

### 1. `self_play_random` method
- **Goal:** Simulate self-play sessions where two instances of the AlphaZero algorithm play against each other. Each move is chosen based on action probabilities derived from MCTS, followed by a random selection weighted by these probabilities.
- **Output:** Generate and return a `memory` list containing the states, action probabilities, and outcomes of each move until the game ends. This data will be used for training the neural network model.

### 2. `learn` method
- **Goal:** Use the data collected from multiple self-play sessions to train the neural network model. This involves running a specified number of self-play iterations to gather training data, followed by training epochs where the model's weights are updated.
- **Steps:**
  1. Collect training data by running self-play sessions.
  2. You will implement `train` in the following task.
  3. Save the model and optimizer state after each training iteration.

### Requirements:
- For `self_play_random`, ensure that the game's current state is correctly converted to a neutral perspective before searching for action probabilities with MCTS. After selecting an action, update the game state and switch the player.
- The `learn` method must iterate over the specified number of iterations and epochs, properly handling model evaluation and training modes. Additionally, ensure to save the model's and optimizer's state at the end of each iteration.

<div class="hint">
Utilize the <code>np.random.choice</code> function to select actions based on the calculated probabilities.
</div>
<div class="hint">
Pay attention to the handling of the game's outcome (<code>value</code>) 
and how it affects the memory data structure.
</div>
<div class="hint">
Make sure to switch the model between evaluation and training modes appropriately in the <code>learn</code> method.
</div>
