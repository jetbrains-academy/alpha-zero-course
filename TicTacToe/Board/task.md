To start implementing the TicTacToe game logic, we need to first take care of board storage. You don't have to implement everything from scratch — the interface and some methods are already provided. 

Take a good look at the `Board` class before you start the task.

### Task
In this task you need to implement some missing functionality of `Board` class:
1. In `__init__` function create an array for board storage
2. In `__getitem__` function return value of element with `index`
3. In `__setitem__` function add assignment for element with `index`
4. In `has_valid_moves` function check if at least one cell of the board is empty
5. In `get_valid_moves` function calculate a flat array of `np.uint8` according the rule: `[i]` array element is `1` if `action` with value `i` is valid and `0` otherwise. For example, for the beginning of the game, `get_valid_moves()` returns `[1 1 1 1 1 1 1 1 1]`
6. In `is_win` function check if `player` have a triplet in any direction
7. In `execute_move` function ensure using `assert` that cell with `move` coordinates is empty. After it, fill the cell with `player`
8. In `get_encoded_state` function return `np.stack` of 3 matrices of `np.float32` values. All matrices are another `board.pieces` representations
   1. `[i,j] == 1` if in original matrix `[i,j] == -1`. Zero otherwise.
   2. `[i,j] == 1` if in original matrix `[i,j] == 0`. Zero otherwise.
   3. `[i,j] == 1` if in original matrix `[i,j] == 1`. Zero otherwise.

<div class="hint">
    In <code>is_win()</code> remember to check: all the horizontal lines, vertical lines and two types of diagonals.
</div>
