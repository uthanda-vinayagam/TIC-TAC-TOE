import pygame
import sys
import random
import math


pygame.init()


WIDTH, HEIGHT = 300, 450
ROWS, COLS = 3, 3
SQSIZE = WIDTH // COLS


BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)


LINE_WIDTH = 5
CIRCLE_RADIUS = SQSIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQSIZE // 4


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe with Score & Menu")
font = pygame.font.SysFont(None, 28)


board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
player_turn = True
game_over = False
odd_even_decided = False
player_score = 0
ai_score = 0
menu_active = True
message = "Pick Odd or Even (O/E) & Number (1-5)"


def draw_lines():
    for i in range(1, ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQSIZE), (WIDTH, i * SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQSIZE, 0), (i * SQSIZE, ROWS * SQSIZE), LINE_WIDTH)

def draw_figures():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE//2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQSIZE + SPACE, row * SQSIZE + SPACE),
                                 (col * SQSIZE + SQSIZE - SPACE, row * SQSIZE + SQSIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQSIZE + SPACE, row * SQSIZE + SQSIZE - SPACE),
                                 (col * SQSIZE + SQSIZE - SPACE, row * SQSIZE + SPACE), CROSS_WIDTH)

def draw_text(text):
    pygame.draw.rect(screen, BG_COLOR, (0, HEIGHT - 100, WIDTH, 100))
    txt_surface = font.render(text, True, TEXT_COLOR)
    screen.blit(txt_surface, (10, HEIGHT - 80))

def draw_score():
    score_text = font.render(f"Player: {player_score}  AI: {ai_score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, HEIGHT - 40))


def available_moves():
    return [(r, c) for r in range(ROWS) for c in range(COLS) if board[r][c] == ' ']

def check_winner(player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(COLS):
        if all(board[row][col] == player for row in range(ROWS)):
            return True
    if all(board[i][i] == player for i in range(ROWS)):
        return True
    if all(board[i][COLS - i - 1] == player for i in range(ROWS)):
        return True
    return False

def is_full():
    return all(all(cell != ' ' for cell in row) for row in board)

def minimax(depth, is_maximizing):
    if check_winner('O'):
        return 1
    if check_winner('X'):
        return -1
    if is_full():
        return 0

    if is_maximizing:
        best = -math.inf
        for (r, c) in available_moves():
            board[r][c] = 'O'
            score = minimax(depth + 1, False)
            board[r][c] = ' '
            best = max(score, best)
        return best
    else:
        best = math.inf
        for (r, c) in available_moves():
            board[r][c] = 'X'
            score = minimax(depth + 1, True)
            board[r][c] = ' '
            best = min(score, best)
        return best

def ai_move():
    best_score = -math.inf
    move = None
    for (r, c) in available_moves():
        board[r][c] = 'O'
        score = minimax(0, False)
        board[r][c] = ' '
        if score > best_score:
            best_score = score
            move = (r, c)
    if move:
        board[move[0]][move[1]] = 'O'

def reset_game():
    global board, player_turn, game_over, odd_even_decided, menu_active, message
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    player_turn = True
    game_over = False
    odd_even_decided = False
    menu_active = True
    message = "Pick Odd or Even (O/E) & Number (1-5)"


clock = pygame.time.Clock()
while True:
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    draw_text(message)
    draw_score()
    pygame.display.update()
    clock.tick(30)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

        if menu_active and event.type == pygame.KEYDOWN:
            if event.unicode.upper() in ['O', 'E']:
                user_choice = event.unicode.upper()
                user_num = random.randint(1, 5)
                ai_num = random.randint(1, 5)
                total = user_num + ai_num
                result = "odd" if total % 2 else "even"
                winner = "Player" if (result == "odd" and user_choice == 'O') or (result == "even" and user_choice == 'E') else "AI"
                player_turn = (winner == "Player")
                message = f"You:{user_num} AI:{ai_num} → {result.upper()} → {winner} starts"
                menu_active = False

                if not player_turn:
                    pygame.time.delay(500)
                    ai_move()
                    player_turn = True

        if not game_over and not menu_active and player_turn:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < ROWS * SQSIZE:
                    row = y // SQSIZE
                    col = x // SQSIZE
                    if board[row][col] == ' ':
                        board[row][col] = 'X'
                        if check_winner('X'):
                            message = "Player Wins! Press R to restart."
                            player_score += 1
                            game_over = True
                        elif is_full():
                            message = "Draw! Press R to restart."
                            game_over = True
                        else:
                            pygame.time.delay(300)
                            ai_move()
                            if check_winner('O'):
                                message = "AI Wins! Press R to restart."
                                ai_score += 1
                                game_over = True
                            elif is_full():
                                message = "Draw! Press R to restart."
                                game_over = True
