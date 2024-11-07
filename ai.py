from enum import Enum
import random
import numpy as np
from utils import all_valid_moves

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    
class AIPlayer:
    def __init__(self, difficulty, color):
        self.difficulty = difficulty
        self.color = color  # 'B' or 'W'

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
            flips = self.count_flips(board, move, self.color)
            if flips > max_flips:
                max_flips = flips
                best_move = move
        return best_move

    def hard_move(self, board):
        # Advanced heuristic or minimax algorithm
        # Placeholder for complex AI logic
        moves = all_valid_moves(board, self.color)
        # Implement advanced strategy here
        return moves[0] if moves else (-1, -1)

    def count_flips(self, board, move, color):
        # Count how many pieces would be flipped by making this move
        return 0  # Placeholder
