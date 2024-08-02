### Implement Game Logic Methods
Here we offer you to understand the backend for visualization of the game.
You will implement the following methods in the `Backend` class:

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

Good luck!
