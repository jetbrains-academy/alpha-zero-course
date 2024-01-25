## Creating the TicTacToe

After we've taken care of storing the board, let's start implementing the interface of the Tic-tac-toe game itself. We use the `Game` interface and implement methods according to the logic of Tic-tac-toe. 

You don't have to implement everything from scratch - the interface and some methods are already provided. 

Take a good look at the `TicTacToe` and `Game` classes before you start the task.

In the `TicTacToe` game, `action` means number of cell which player has chosen for his move. Numbering is through, by rows, starts from zero. That is, for a cell with indexes `(1,2)`, `action` will be `5` 

### Task
In this task you need to implement some missing functionality of `TicTacToe` class:
1. In `__init__` function create the instance of `Board` class
2. In `get_next_state` function calculate indexes by the `action` number (look description above)
3. In `get_valid_moves` function calculate flat array of `np.uint8` according the rule: `[i]` array element is `1` if `action` with value `i` is valid and `0` otherwise. For example, for the beginning of the game, `get_valid_moves()` returns `[1 1 1 1 1 1 1 1 1]`  
4. In `get_game_ended` function identify the end of the game. Return 1 if `player` is win, -1 if `-player` is win and 0 if the game is not finished yet.
5. In `change_perspective` function invert the board. For `player` board should stay the same, but for `-player` 1 and -1 should be flipped. 
6. In `get_encoded_state` function return `np.stack` of 3 matrices of `np.float32` values. All matrices are another `board.pieces` representations
   1. `[i,j] == 1` if in original matrix `[i,j] == -1`. Zero otherwise.
   2. `[i,j] == 1` if in original matrix `[i,j] == 0`. Zero otherwise.
   3. `[i,j] == 1` if in original matrix `[i,j] == 1`. Zero otherwise.

<div class="hint">
  You can solve task in <code>change_perspective()</code> using only one multiplication
</div>
