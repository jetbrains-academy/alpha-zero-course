## Creating the game board
To start implementing the Tic-tac-toe game logic, we need to first take care of board storage. You don't have to implement everything from scratch — the interface and some methods are already provided. 

Take a good look at the `Board` class before you start the task.

### Task
In this task you need to implement some missing functionality of `Board` class:
1. In `__init__` function create an array for board storage
2. In `__getitem__` function return value of element with `index`
3. In `__setitem__` function add assignment for element with `index`
4. In `has_legal_moves` function check if at least one cell of the board is empty
5. In `is_win` function check if `player` have a triplet in any direction
6. In `execute_move` function ensure using `assert` that cell with `move` coordinates is empty. After it, fill the cell with `player` 

<div class="hint">
    In <code>is_win()</code> remember to check: 3 horizontal lines, 3 vertical lines and 2 diagonals
</div>
