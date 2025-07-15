import pygame
import random
import sys
import time


TILE_SIZE = 32
FPS = 60


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 100, 255)
GOAL_COLOR = (0, 255, 0)
WALL_COLOR = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 70, 70)
HOVER_COLOR = (120, 120, 120)


pygame.init()
font = pygame.font.SysFont('Arial', 20)


maze = []
ROWS, COLS = 0, 0
WIDTH, HEIGHT = 0, 0
screen = None
player_pos = [1, 1]
goal_pos = []
moves = 0
start_time = 0
game_over = False


def generate_maze(rows, cols):
    maze = [[1] * cols for _ in range(rows)]
    stack = [(1, 1)]
    maze[1][1] = 0

    def neighbors(r, c):
        dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(dirs)
        result = []
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1 and maze[nr][nc] == 1:
                result.append((nr, nc, r + dr // 2, c + dc // 2))
        return result

    while stack:
        r, c = stack[-1]
        nbs = neighbors(r, c)
        if nbs:
            nr, nc, wr, wc = nbs[0]
            maze[wr][wc] = 0
            maze[nr][nc] = 0
            stack.append((nr, nc))
        else:
            stack.pop()
    return maze


def draw_button(text, x, y, w, h, mouse_pos):
    rect = pygame.Rect(x, y, w, h)
    color = HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)
    txt = font.render(text, True, WHITE)
    screen.blit(txt, (x + (w - txt.get_width()) // 2, y + (h - txt.get_height()) // 2))
    return rect


def show_menu():
    global screen
    screen = pygame.display.set_mode((600, 400))
    while True:
        screen.fill(BG_COLOR)
        mouse = pygame.mouse.get_pos()
        title = font.render("Select Difficulty", True, WHITE)
        screen.blit(title, (220, 50))

        easy = draw_button("Easy (11x11)", 200, 120, 200, 40, mouse)
        med = draw_button("Medium (18x18)", 200, 180, 200, 40, mouse)
        hard = draw_button("Hard (27x27)", 200, 240, 200, 40, mouse)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy.collidepoint(mouse):
                    return 11, 11
                elif med.collidepoint(mouse):
                    return 21, 21
                elif hard.collidepoint(mouse):
                    return 31, 31


def init_game(rows, cols):
    global maze, ROWS, COLS, WIDTH, HEIGHT, screen, player_pos, goal_pos, moves, start_time, game_over
    ROWS, COLS = rows, cols
    WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE + 50
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    maze = generate_maze(ROWS, COLS)
    player_pos = [1, 1]
    goal_pos = [ROWS - 2, COLS - 2]
    moves = 0
    start_time = time.time()
    game_over = False


def draw_maze():
    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE if maze[r][c] == 0 else WALL_COLOR
            pygame.draw.rect(screen, color, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, GOAL_COLOR, (goal_pos[1]*TILE_SIZE, goal_pos[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[1]*TILE_SIZE, player_pos[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_ui():
    elapsed = int(time.time() - start_time)
    info = f"Moves: {moves} | Time: {elapsed}s"
    pygame.draw.rect(screen, BG_COLOR, (0, HEIGHT - 50, WIDTH, 50))
    txt = font.render(info, True, TEXT_COLOR)
    screen.blit(txt, (10, HEIGHT - 35))

def show_message(message):
    msg = font.render(message, True, GOAL_COLOR)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))


def is_valid_move(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS and maze[r][c] == 0

def handle_movement(key):
    global moves
    r, c = player_pos
    if key == pygame.K_UP and is_valid_move(r - 1, c): player_pos[0] -= 1; moves += 1
    if key == pygame.K_DOWN and is_valid_move(r + 1, c): player_pos[0] += 1; moves += 1
    if key == pygame.K_LEFT and is_valid_move(r, c - 1): player_pos[1] -= 1; moves += 1
    if key == pygame.K_RIGHT and is_valid_move(r, c + 1): player_pos[1] += 1; moves += 1

def restart_game():
    init_game(ROWS, COLS)


if __name__ == "__main__":
    rows, cols = show_menu()
    init_game(rows, cols)
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)
        draw_maze()
        draw_ui()

        if player_pos == goal_pos:
            game_over = True
            show_message("🎉 You reached the goal! (R: Restart | Q: Quit)")

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        restart_game()
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False
                else:
                    handle_movement(event.key)

    pygame.quit()
    sys.exit()
