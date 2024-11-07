import numpy as np

def calculate_score(board):
    black_score = np.count_nonzero(board == 'B')
    white_score = np.count_nonzero(board == 'W')
    return black_score, white_score
def score_valid_move(board, row, col, color):
    return
def play_move(board, row, col, color):
    board[row, col] = color
    seen_opposite = False
    current_row = row - 1
    working_mem = []
    while 0 <= current_row <= 7:
        if not board[current_row, col] or board[row-1, col] == color:
            break
        elif board[current_row, col] == color:
            if seen_opposite:
                for x,y in working_mem:
                    board[x, y] = color
                working_mem = []
                break
        else:
            seen_opposite = True
            working_mem.append((current_row, col))
        current_row -= 1
    
    current_row = row + 1
    working_mem = []
    while 0 <= current_row <= 7:
        if not board[current_row, col] or board[row+1, col] == color:
            break
        elif board[current_row, col] == color:
            if seen_opposite:
                for x,y in working_mem:
                    board[x, y] = color
                break
        else:
            seen_opposite = True
            working_mem.append((current_row, col))
        current_row += 1
    
        
    current_col = col - 1
    working_mem = []
    while 0 <= current_col <= 7:
        if not board[row, current_col] or board[row, col - 1] == color:
            break
        elif board[row, current_col] == color:
            if seen_opposite:
                for x,y in working_mem:
                    board[x, y] = color
                break
        else:
            seen_opposite = True
            working_mem.append((row, current_col))
        current_col -= 1
        
    current_col = col + 1
    working_mem = []
    while 0 <= current_col <= 7:
        if not board[row, current_col]:
            break
        elif board[row, current_col] == color or board[row, col + 1] == color:
            if seen_opposite:
                for x,y in working_mem:
                    board[x, y] = color
                break
        else:
            seen_opposite = True
            working_mem.append((row, current_col))
        current_col += 1
        
    current_row = row + 1
    current_col = col + 1
    working_mem = []
    while 0 <= current_row <= 7 and 0 <= current_col <= 7:
        if not board[current_row, current_col] or board[row +1, col+1] == color:
            break
        elif board[current_row, current_col] == color:
            if seen_opposite:
                for x,y in working_mem:
                    board[x, y] = color
                break
        else:
            seen_opposite = True
            working_mem.append((current_row, current_col))
        current_row += 1
        current_col += 1
        
    current_row = row - 1
    current_col = col - 1
    working_mem = []
    while 0 <= current_row <= 7 and 0 <= current_col <= 7:
        if not board[current_row, current_col] or board[row-1, col-1] == color:
            break
        elif board[current_row, current_col] == color:
            if seen_opposite:
                for x,y in working_mem:
                    board[x, y] = color
                break
        else:
            seen_opposite = True
            working_mem.append((current_row, current_col))
        current_row -= 1
        current_col -= 1
        
    current_row = row + 1
    current_col = col - 1
    working_mem = []
    while 0 <= current_row <= 7 and 0 <= current_col <= 7:
        if not board[current_row, current_col] or board[row+1, col -1] == color:
            break
        elif board[current_row, current_col] == color:
            if seen_opposite:
                for x,y in working_mem:
                    board[x, y] = color
                break
        else:
            seen_opposite = True
            working_mem.append((current_row, current_col))
        current_row += 1
        current_col -= 1
        
    current_row = row - 1
    current_col = col + 1
    working_mem = []
    while 0 <= current_row <= 7 and 0 <= current_col <= 7:
        if not board[current_row, current_col] or board[row-1, col+1]==color:
            break
        elif board[current_row, current_col] == color:
            if seen_opposite:
                for x,y in working_mem:
                    board[x, y] = color
                break
        else:
            seen_opposite = True
            working_mem.append((current_row, current_col))
        current_row -= 1
        current_col += 1
    return board

def is_valid_move(board, row, col, color):
        # Check if placing at (row, col) is valid
        # Implement game rules here
        if not board[row][col] is None:
            return False
        else:
            seen_opposite = False
            current_row = row - 1
            while 0 <= current_row <= 7:
                if not board[current_row, col] or board[row-1, col] == color:
                    break
                elif board[current_row, col] == color:
                    if seen_opposite:
                        return True
                else:
                    seen_opposite = True
                current_row -= 1
            
            current_row = row + 1
            while 0 <= current_row <= 7:
                if not board[current_row, col] or board[row+1, col] == color:
                    break
                elif board[current_row, col] == color:
                    if seen_opposite:
                        return True
                else:
                    seen_opposite = True
                current_row += 1
            
                
            current_col = col - 1
            while 0 <= current_col <= 7:
                if not board[row, current_col] or board[row, col - 1] == color:
                    break
                elif board[row, current_col] == color:
                    if seen_opposite:
                        return True
                else:
                    seen_opposite = True
                current_col -= 1
                
            current_col = col + 1
            while 0 <= current_col <= 7:
                if not board[row, current_col]:
                    break
                elif board[row, current_col] == color or board[row, col + 1] == color:
                    if seen_opposite:
                        return True
                else:
                    seen_opposite = True
                current_col += 1
                
            current_row = row + 1
            current_col = col + 1
            while 0 <= current_row <= 7 and 0 <= current_col <= 7:
                if not board[current_row, current_col] or board[row +1, col+1] == color:
                    break
                elif board[current_row, current_col] == color:
                    if seen_opposite:
                        return True
                else:
                    seen_opposite = True
                current_row += 1
                current_col += 1
                
            current_row = row - 1
            current_col = col - 1
            while 0 <= current_row <= 7 and 0 <= current_col <= 7:
                if not board[current_row, current_col] or board[row-1, col-1] == color:
                    break
                elif board[current_row, current_col] == color:
                    if seen_opposite:
                        return True
                else:
                    seen_opposite = True
                current_row -= 1
                current_col -= 1
                
            current_row = row + 1
            current_col = col - 1
            while 0 <= current_row <= 7 and 0 <= current_col <= 7:
                if not board[current_row, current_col] or board[row+1, col -1] == color:
                    break
                elif board[current_row, current_col] == color:
                    if seen_opposite:
                        return True
                else:
                    seen_opposite = True
                current_row += 1
                current_col -= 1
                
            current_row = row - 1
            current_col = col + 1
            while 0 <= current_row <= 7 and 0 <= current_col <= 7:
                if not board[current_row, current_col] or board[row-1, col+1]==color:
                    break
                elif board[current_row, current_col] == color:
                    if seen_opposite:
                        return True
                else:
                    seen_opposite = True
                current_row -= 1
                current_col += 1
            return False
        
def all_valid_moves(board, color):
    # Return a list of valid moves for the given color
    moves = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if is_valid_move(board, row, col, color):
                moves.append((row, col))
    return moves
        