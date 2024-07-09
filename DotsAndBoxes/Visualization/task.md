### Visualization in Tkinter

Most likely you need to [install Tkinter](https://tkdocs.com/tutorial/install.html) 
on your system for everything to display.

#### Implement Game Logic Methods
You will implement the following methods in the `DotsAndBoxesVisualization` class:

1. **`is_edge_occupied(self, logical_position, edge_type)`**:
   - **Purpose**: Check if a specified edge is already occupied.
   - **Parameters**:
     - `logical_position`: A list `[r, c]` representing the row and column indices of the edge
     - `edge_type`: A string (`'row'` or `'col'`) indicating whether the edge is horizontal or vertical
   - **Returns**: `True` if the edge is occupied, `False` otherwise

2. **`get_action_from(self, edge_type, logical_position)`**:
   - **Purpose**: Given edge_type and logical_position calculate the action number.
   - **Parameters**:
     - `edge_type`: A string (`'row'` or `'col'`) indicating the type of edge
     - `logical_position`: A list `[r, c]` representing the row and column indices of the edge
   - **Returns**: Action number

3. **`update_board(self, edge_type, logical_position)`**:
   - **Purpose**: Update the board state when a player adds an edge.
   - **Parameters**:
     - `edge_type`: A string (`'row'` or `'col'`) indicating the type of edge
     - `logical_position`: A list `[r, c]` representing the row and column indices of the edge
   - **Functionality**: 
     - Set the corresponding edge in `row_status` or `col_status` arrays to `1`
     - Increment the values in `cell_status` for the affected boxes

3. **`shade_box(self, box, color)`**:
   - **Purpose**: Shade a completed box with the player's color.
   - **Parameters**:
     - `box`: A list `[r, c]` representing the row and column indices of the box
     - `color`: A string representing the color to fill the box with

As a final result, you should get the nice visualization of the game board and the players' moves in the Tkinter window.
It will work only if you are using the standart version of the course on your own computer, 
not the remote one. Don't worry, for the remote version, in one step 
you are implementing web variant, which work in any browser.

Good luck!
