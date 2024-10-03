### Creating the Tic-tac-toe

After we've taken care of storing the board, let's start implementing the interface of the Tic-tac-toe game itself. We use the `Game` interface and implement methods according to the logic of Tic-tac-toe. 

You don't have to implement everything from scratch - the interface and some methods are already provided. 

Take a good look at the `TicTacToe` and `Game` classes before you start the task.

In the `TicTacToe` game, `action` means number of cell which player has chosen for his move. Numbering is through, by rows, starts from zero. That is, for a cell with indexes `(1,2)`, `action` will be `5` 

### Task
In this task you need to implement some missing functionality of `TicTacToe` class: 
1. In `get_game_ended` function identify the end of the game. Return `1` if `player` is win, `-1` if `-player` is win, `0` if the game is not finished yet and `1e-4` if the game ended in a draw.
2. In `change_perspective` function invert the board. For `player` board should stay the same, but for `-player` 1 and -1 should be flipped. 

<div class="hint">
  You can solve task in <code>change_perspective()</code> using only one multiplication
</div>
