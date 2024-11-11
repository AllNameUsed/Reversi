import numpy as np

def calculate_score(board):
    black_score = np.count_nonzero(board == 'B')
    white_score = np.count_nonzero(board == 'W')
    return black_score, white_score


def play_move(board, row, col, color):
    board[row, col] = color  # Place the piece
    opponent_color = 'B' if color == 'W' else 'W'

    directions = [(-1, 0),  # Up
                  (1, 0),   # Down
                  (0, -1),  # Left
                  (0, 1),   # Right
                  (-1, -1), # Up-Left
                  (-1, 1),  # Up-Right
                  (1, -1),  # Down-Left
                  (1, 1)]   # Down-Right

    for dr, dc in directions:
        seen_opposite = False
        positions_to_flip = []
        current_row, current_col = row + dr, col + dc

        while 0 <= current_row < 8 and 0 <= current_col < 8:
            current_cell = board[current_row, current_col]
            if current_cell is None:
                break  # Empty cell, stop searching in this direction
            elif current_cell == opponent_color:
                seen_opposite = True
                positions_to_flip.append((current_row, current_col))
            elif current_cell == color:
                if seen_opposite:
                    # Flip all opponent pieces in this direction
                    for r, c in positions_to_flip:
                        board[r, c] = color
                break  # Found own piece, stop searching in this direction
            else:
                break  # Cell contains invalid value (should not happen)
            current_row += dr
            current_col += dc
    return board


def is_valid_move(board, row, col, color):
    if board[row][col] is not None:
        return False  # The cell is already occupied

    opponent_color = 'B' if color == 'W' else 'W'
    directions = [(-1, 0),  # Up
                  (1, 0),   # Down
                  (0, -1),  # Left
                  (0, 1),   # Right
                  (-1, -1), # Up-Left
                  (-1, 1),  # Up-Right
                  (1, -1),  # Down-Left
                  (1, 1)]   # Down-Right

    for dr, dc in directions:
        current_row, current_col = row + dr, col + dc
        seen_opponent = False  # Reset for each direction

        while 0 <= current_row < 8 and 0 <= current_col < 8:
            current_cell = board[current_row][current_col]
            if current_cell == opponent_color:
                seen_opponent = True
            elif current_cell == color:
                if seen_opponent:
                    return True  # Valid move in this direction
                else:
                    break  # Adjacent cell is own color without enclosing opponent's pieces
            else:
                break  # Empty cell or invalid, stop searching this direction
            current_row += dr
            current_col += dc

    return False  # No valid moves in any direction

        
def all_valid_moves(board, color):
    # Return a list of valid moves for the given color
    moves = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if is_valid_move(board, row, col, color):
                moves.append((row, col))
    return moves
        