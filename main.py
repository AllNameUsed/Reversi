import pygame
import sys
import time
import numpy as np
from ai import AIPlayer, Difficulty
from utils import is_valid_move, calculate_score, play_move, all_valid_moves

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 750, 615
ROWS, COLS = 8, 8
SQUARE_SIZE = 75
BOARDER = 7

# Colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SETTINGS_COLOR = (200, 200, 200)
BUTTON_COLOR = (180, 180, 180)
BUTTON_HOVER_COLOR = (150, 150, 150)

# Game settings
game_mode = 'Human vs CPU'  # or 'Human vs Human'
ai_difficulty = Difficulty.EASY  # Default AI difficulty

# Load images or fonts if necessary
setting_img = pygame.image.load('assets/settings_image.png')
setting_img = pygame.transform.scale(setting_img, (50, 50))

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")


# Game board representation
board = [[None for _ in range(COLS)] for _ in range(ROWS)]

def draw_scoreboard(black_score, white_score):
    # Draw the scoreboard on the right-hand side
    # Fill the border area with a background color
    scoreboard_rect = pygame.Rect(600, 0, WIDTH - 600, HEIGHT)
    pygame.draw.rect(screen, (0, 0, 0), scoreboard_rect)  # Black background

    # Draw the text
    x_pos = 610
    y_pos = 200
    score_font = pygame.font.SysFont(None, 36)

    # Render player labels
    black_label = score_font.render('Black:', True, WHITE)
    white_label = score_font.render('White:', True, WHITE)
    screen.blit(black_label, (x_pos, y_pos))
    screen.blit(white_label, (x_pos, y_pos + 50))

    # Render scores
    black_score_text = score_font.render(str(black_score), True, WHITE)
    white_score_text = score_font.render(str(white_score), True, WHITE)
    screen.blit(black_score_text, (x_pos + 80, y_pos))
    screen.blit(white_score_text, (x_pos + 80, y_pos + 50))

def is_game_over(board):
    # Check if there are any empty spaces
    if np.all(board != None):
        return True
    # Check if either player has valid moves
    black_moves = all_valid_moves(board, 'B')
    white_moves = all_valid_moves(board, 'W')
    if not black_moves and not white_moves:
        return True
    return False

def game_over_screen(black_score, white_score):
    running = True
    clock = pygame.time.Clock()
    score_font = pygame.font.SysFont(None, 36)
    large_font = pygame.font.SysFont(None, 72)
    while running:
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black overlay with alpha

        screen.blit(overlay, (0, 0))

        # Display Game Over text
        game_over_text = large_font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))

        # Display final scores
        score_text = score_font.render(f"Black: {black_score}  White: {white_score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))

        # Draw Restart Button
        restart_button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        if restart_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, restart_button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, restart_button_rect)
        restart_text = score_font.render('Restart Game', True, BLACK)
        screen.blit(restart_text, (restart_button_rect.x + (restart_button_rect.width - restart_text.get_width())//2,
                                   restart_button_rect.y + (restart_button_rect.height - restart_text.get_height())//2))

        pygame.display.flip()
        clock.tick(60)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button_rect.collidepoint(event.pos):
                    running = False  # Exit game over screen and restart game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def draw_board(phantom_piece=None, illegal_move_indicator=None):
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, GREEN, (col*SQUARE_SIZE + BOARDER, row*SQUARE_SIZE+BOARDER, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, BLACK, (col*SQUARE_SIZE+BOARDER, row*SQUARE_SIZE+BOARDER, SQUARE_SIZE, SQUARE_SIZE), 1)
            if board[row][col] == 'W':
                pygame.draw.circle(screen, WHITE, (col*SQUARE_SIZE + SQUARE_SIZE//2 + BOARDER, row*SQUARE_SIZE + SQUARE_SIZE//2+BOARDER), SQUARE_SIZE//2 - 5)
            elif board[row][col] == 'B':
                pygame.draw.circle(screen, BLACK, (col*SQUARE_SIZE + SQUARE_SIZE//2+BOARDER, row*SQUARE_SIZE + SQUARE_SIZE//2+BOARDER), SQUARE_SIZE//2 - 5)

    # Draw the phantom piece if applicable
    if phantom_piece:
        row, col, color = phantom_piece
        piece_color = BLACK if color == 'B' else WHITE
        # Create a semi-transparent surface for the phantom piece
        phantom_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(phantom_surface, piece_color + (100,), (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//2 - 5)
        screen.blit(phantom_surface, (col*SQUARE_SIZE+BOARDER, row*SQUARE_SIZE+BOARDER))
        
    # Draw illegal move indicator:
    if illegal_move_indicator:
        row = illegal_move_indicator['row']
        col = illegal_move_indicator['col']
        piece_color = (255, 0, 0)  # Red color
        illegal_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(illegal_surface, piece_color + (150,), (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//2 - 5)
        screen.blit(illegal_surface, (col*SQUARE_SIZE+BOARDER, row*SQUARE_SIZE+BOARDER))


def draw_settings_icon():
    # You can add an image or icon here
    screen.blit(setting_img, (WIDTH -70, 20))

# ... [Imports and initial setup remain the same] ...

def settings_menu():
    global game_mode, ai_difficulty, turn
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(GREEN)
        # Draw menu options
        font = pygame.font.SysFont(None, 36)
        small_font = pygame.font.SysFont(None, 28)
        title = font.render('Settings', True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        # Game Mode Selection
        modes = ['Human vs Human', 'Human vs CPU']
        for i, mode in enumerate(modes):
            text = font.render(mode, True, BLACK)
            screen.blit(text, (100, 150 + i*50))
            if game_mode == mode:
                pygame.draw.circle(screen, BLACK, (70, 165 + i*50), 10)

        # AI Difficulty Selection
        difficulties = ['Easy', 'Medium', 'Hard']
        for i, diff in enumerate(difficulties):
            text = font.render(diff, True, BLACK)
            screen.blit(text, (400, 150 + i*50))
            if ai_difficulty.name == diff.upper():
                pygame.draw.circle(screen, BLACK, (370, 165 + i*50), 10)

        # Draw Restart Button
        restart_button_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT - 150, 100, 40)
        mouse_pos = pygame.mouse.get_pos()
        if restart_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, restart_button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, restart_button_rect)
        restart_text = small_font.render('Restart', True, BLACK)
        screen.blit(restart_text, (restart_button_rect.x + (restart_button_rect.width - restart_text.get_width())//2,
                                   restart_button_rect.y + (restart_button_rect.height - restart_text.get_height())//2))

        # Draw Back Button
        back_button_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT - 100, 100, 40)
        if back_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, back_button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect)
        back_text = small_font.render('Back', True, BLACK)
        screen.blit(back_text, (back_button_rect.x + (back_button_rect.width - back_text.get_width())//2,
                                back_button_rect.y + (back_button_rect.height - back_text.get_height())//2))

        pygame.display.flip()
        clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                # Check for mode selection
                for i in range(len(modes)):
                    if 100 <= mx <= 300 and 150 + i*50 <= my <= 180 + i*50:
                        if game_mode != modes[i]:
                            game_mode = modes[i]
                            reset_game()
                            turn = 'B'  # Ensure Black starts first
                # Check for difficulty selection
                for i in range(len(difficulties)):
                    if 400 <= mx <= 600 and 150 + i*50 <= my <= 180 + i*50:
                        ai_difficulty = Difficulty[difficulties[i].upper()]
                # Check if Restart button is clicked
                if restart_button_rect.collidepoint(mx, my):
                    reset_game()
                    turn = 'B'  # Ensure Black starts first
                # Check if Back button is clicked
                elif back_button_rect.collidepoint(mx, my):
                    screen.fill(BLACK)
                    running = False  # Exit the settings menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen.fill(BLACK)
                    running = False

def reset_game():
    global board, turn
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'
    board = np.array(board)
    turn = 'B'  # Reset turn to Black

def main():
    global board, turn
    # Game loop
    running = True
    clock = pygame.time.Clock()
    turn = 'B'  # 'B' for Black, 'W' for White
    ai_player = AIPlayer(ai_difficulty, 'W')  # AI plays as White by default

    # Initialize starting position
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'
    board = np.array(board)

    phantom_piece = None  # Initialize phantom piece
    illegal_indicator = None
    ai_move_time = None  # Time when AI will make its move

    while running:
        draw_board(phantom_piece, illegal_indicator)
        draw_settings_icon()
        pygame.display.flip()
        clock.tick(60)

        # Calculate and draw the scoreboard
        black_score, white_score = calculate_score(board)
        draw_scoreboard(black_score, white_score)

        # Check if the game is over
        if is_game_over(board):
            game_over_screen(black_score, white_score)
            reset_game()
            ai_player = AIPlayer(ai_difficulty, 'W')  # Reset AI player in case settings changed
            phantom_piece = None
            illegal_indicator = None
            ai_move_time = None
            continue  # Start the loop again after resetting

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                if (mx < WIDTH - 50 or my > 50):  # Avoid drawing over settings icon
                    col = mx // SQUARE_SIZE
                    row = my // SQUARE_SIZE
                    if 0 <= col < COLS and 0 <= row < ROWS:
                        if board[row][col] is None:
                            # Only show phantom piece on player's turn
                            if (game_mode == 'Human vs Human') or (game_mode == 'Human vs CPU' and turn == 'B'):
                                # Check if move is valid before showing phantom piece
                                if is_valid_move(board, row, col, turn):
                                    phantom_piece = (row, col, turn)
                                else:
                                    phantom_piece = None
                            else:
                                phantom_piece = None  # Not the player's turn
                        else:
                            phantom_piece = None  # Spot is occupied
                    else:
                        phantom_piece = None  # Mouse is outside the board
                else:
                    phantom_piece = None  # Mouse is over settings icon

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if WIDTH - 70 <= mx <= WIDTH - 20 and 20 <= my <= 70:
                    settings_menu()
                    # Update AI player in case difficulty changed
                    ai_player = AIPlayer(ai_difficulty, 'W')
                    turn = 'B'  # Ensure Black starts first after exiting settings menu
                else:
                    col = mx // SQUARE_SIZE
                    row = my // SQUARE_SIZE
                    if 0 <= col < COLS and 0 <= row < ROWS:
                        # Handle move
                        if len(all_valid_moves(board=board, color=turn)) == 0:
                            turn = 'W' if turn == 'B' else 'B'
                            phantom_piece = None  # Clear phantom piece if player skips turn
                            ai_move_time = None  # Reset AI move time
                        elif game_mode == 'Human vs Human' or (game_mode == 'Human vs CPU' and turn == 'B'):
                            if board[row][col] is None:
                                # Check if move is valid
                                if is_valid_move(board=board, row=row, col=col, color=turn):
                                    play_move(board=board, row=row, col=col, color=turn)
                                    # Switch turns
                                    turn = 'W' if turn == 'B' else 'B'
                                    phantom_piece = None  # Clear phantom piece after move
                                    illegal_indicator = None  # Clear illegal move indicator
                                    # If the next turn is the AI's, set the AI move time
                                    if game_mode == 'Human vs CPU' and turn == ai_player.color:
                                        ai_move_time = pygame.time.get_ticks() + 1000  # Wait 1 second
                                else:
                                    # Illegal move: display red phantom piece
                                    illegal_indicator = {'row': row, 'col': col, 'time': pygame.time.get_ticks()}
                            else:
                                # Spot is occupied
                                illegal_indicator = {'row': row, 'col': col, 'time': pygame.time.get_ticks()}

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings_menu()
                    # Update AI player in case difficulty changed
                    ai_player = AIPlayer(ai_difficulty, 'W')
                    turn = 'B'  # Ensure Black starts first after exiting settings menu

        # AI Move
        if game_mode == 'Human vs CPU' and turn == ai_player.color:
            current_time = pygame.time.get_ticks()
            if ai_move_time is None:
                # Set the AI move time if not already set
                ai_move_time = current_time + 1000  # Wait 1 second
            elif current_time >= ai_move_time:
                # AI calculates move
                row, col = ai_player.get_move(board)
                if (row, col) != (-1, -1):
                    play_move(board=board, row=row, col=col, color=turn)
                    # Switch turns
                    turn = 'W' if turn == 'B' else 'B'
                    phantom_piece = None  # Clear phantom piece after AI move
                    illegal_indicator = None  # Clear illegal move indicator
                else:
                    # AI has no valid moves
                    turn = 'W' if turn == 'B' else 'B'
                    phantom_piece = None  # Clear phantom piece if AI skips turn
                ai_move_time = None  # Reset AI move time after move

        else:
            ai_move_time = None  # Ensure AI move time is reset when it's not AI's turn

        if illegal_indicator:
            current_time = pygame.time.get_ticks()
            if current_time - illegal_indicator['time'] > 250:  # Display for 250 milliseconds
                illegal_indicator = None

    pygame.quit()

if __name__ == '__main__':
    main()
