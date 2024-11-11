from enum import Enum
import random
import numpy as np
from utils import all_valid_moves, calculate_score, play_move

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    
class AIPlayer:
    def __init__(self, difficulty, color):
        self.difficulty = difficulty
        self.color = color  # 'B' or 'W'

    def get_opponent_color(self):
        return 'W' if self.color == 'B' else 'B'

    def get_move(self, board):
        if self.difficulty == Difficulty.EASY:
            return self.easy_move(board)
        elif self.difficulty == Difficulty.MEDIUM:
            return self.medium_move(board)
        elif self.difficulty == Difficulty.HARD:
            return self.hard_move(board)

    def easy_move(self, board):
        # Random valid move
        moves = all_valid_moves(board, self.color)
        return random.choice(moves) if moves else (-1, -1)

    def medium_move(self, board):
        # Simple heuristic: choose move that flips the most pieces
        moves = all_valid_moves(board, self.color)
        max_flips = -1
        best_move = (-1, -1)
        for move in moves:
            flips = self.score_move(board, move, self.color)
            if flips > max_flips:
                max_flips = flips
                best_move = move
        return best_move

    def hard_move(self, board):
        # Advanced heuristic or minimax algorithm
        # Placeholder for complex AI logic
        _, best_move = self.minmax(board, search_depth=6, alpha=float('-inf'), beta=float('inf'), max_turn=True)
        return best_move if best_move else (-1, -1)
    

    def is_terminal_node(self, board):
        # Check if the game is over
        if np.all(board != None):
            return True
        black_moves = all_valid_moves(board, 'B')
        white_moves = all_valid_moves(board, 'W')
        if not black_moves and not white_moves:
            return True
        return False
    
    def evaluate_board(self, board):
        # Positional weights for each square on the board
        positional_weights = np.array([
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100]
        ])
        # Calculate positional score
        score = 0
        for row in range(8):
            for col in range(8):
                if board[row][col] == self.color:
                    score += positional_weights[row][col]
                elif board[row][col] == self.get_opponent_color():
                    score -= positional_weights[row][col]
        return score
        
    def minmax(self, board, search_depth, alpha, beta, max_turn):
        if search_depth == 0 or self.is_terminal_node(board):
            evaluation = self.evaluate_board(board)
            return evaluation, None

        current_color = self.color if max_turn else self.get_opponent_color()
        valid_moves = all_valid_moves(board, current_color)

        if not valid_moves:
            # Skip turn if no valid moves
            evaluation, _ = self.minmax(board, search_depth - 1, alpha, beta, not max_turn)
            return evaluation, None

        best_move = None

        if max_turn:
            max_eval = float('-inf')
            for move in valid_moves:
                new_board = np.copy(board)
                new_board = play_move(new_board, move[0], move[1], current_color)
                eval, _ = self.minmax(new_board, search_depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                new_board = np.copy(board)
                new_board = play_move(new_board, move[0], move[1], current_color)
                eval, _ = self.minmax(new_board, search_depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval, best_move

    def score_move(self, board, move, color):
        # Count how many pieces would be flipped by making this move
        dummy = np.copy(board) 
        dummy = play_move(dummy,move[0], move[1], color)
        
        if color =="B":
            opponent = "W"
        else:
            opponent = "B"
        if len(all_valid_moves(dummy, opponent)) == 0:
            return 100
        score_b, score_w = calculate_score(dummy)
        if color == "B":
            return score_b
        else:
            return score_w
