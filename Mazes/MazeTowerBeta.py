# Maze Tower Full Version with Classic, Challenge, Infinite, and Mystery Modes
from pyamaze import maze
import pygame
import sys
import time
import os
import random

pygame.init()
WIDTH, HEIGHT = 600, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Tower (Beta 1.2)")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
bigfont = pygame.font.SysFont(None, 80)

WHITE = (255, 255, 255)
BG_COLOR = (30, 30, 30)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
AQUA = (0, 255, 255)
GRAY = (100, 100, 100)

LEVEL_MAX = 25

size_map = {
    (1, 5): 10,
    (6, 10): 15,
    (11, 15): 20,
    (16, 20): 25,
    (21, 25): 30
}

timer_map = {
    (1, 5): 20,
    (6, 10): 30,
    (11, 15): 40,
    (16, 20): 50,
    (21, 25): 60
}

def get_maze_size(level):
    for level_range, size in size_map.items():
        if level_range[0] <= level <= level_range[1]:
            return size
    return 10

def get_timer(level):
    for level_range, t in timer_map.items():
        if level_range[0] <= level <= level_range[1]:
            return t
    return 30

def save_highest_level(level, mode):
    file = f"maze_data_{mode}.txt"
    with open(file, "w") as f:
        f.write(str(level))

def load_highest_level(mode):
    file = f"maze_data_{mode}.txt"
    if os.path.exists(file):
        with open(file, "r") as f:
            return int(f.read().strip())
    return 1

def draw_home():
    screen.fill(BG_COLOR)
    title = bigfont.render("Maze Tower", True, YELLOW)
    high1 = font.render(f"Classic Max: {load_highest_level('classic')}", True, GREEN)
    high2 = font.render(f"Challenge Max: {load_highest_level('challenge')}", True, PURPLE)
    high3 = font.render(f"Infinite Max: {load_highest_level('infinite')}", True, BLUE)
    high4 = font.render(f"Mystery Max: {load_highest_level('mystery')}", True, AQUA)
    mode_text = font.render("Mode Select:", True, RED)
    mode_text2 = font.render("[C] Classic  [H] Challenge", True, RED)
    mode_text3 = font.render("[I] Infinite  [M] Mystery", True, RED)
    screen.blit(title, ((WIDTH - title.get_width()) // 2, 80))
    screen.blit(high1, ((WIDTH - high1.get_width()) // 2, 160))
    screen.blit(high2, ((WIDTH - high2.get_width()) // 2, 210))
    screen.blit(high3, ((WIDTH - high3.get_width()) // 2, 260))
    screen.blit(high4, ((WIDTH - high4.get_width()) // 2, 310))
    screen.blit(mode_text, ((WIDTH - mode_text.get_width()) // 2 -50, 400))
    screen.blit(mode_text2, ((WIDTH - mode_text.get_width()) // 2 - 50, 450))
    screen.blit(mode_text3, ((WIDTH - mode_text.get_width()) // 2 - 50, 500))
    jump_text = font.render("Jump To Highest Level:", True, WHITE)
    cl_text = font.render("[1] Infinite", True, GREEN)
    my_text = font.render("[2] Mystery", True, AQUA)
    screen.blit(jump_text, ((WIDTH - jump_text.get_width()) // 2, 550))
    screen.blit(cl_text, (100, 600))
    screen.blit(my_text, (350, 600))
    pygame.display.flip()


def play_level(level, mode):
    completed = False
    if mode == "infinite" or mode == "mystery":
        size = level + 4
    else:
        size = get_maze_size(level)

    m = maze(size, size)
    m.CreateMaze()
    path = m.path

    ROWS, COLS = m.rows, m.cols
    global WIDTH, HEIGHT
    WIDTH = max(600, COLS * 20)
    HEIGHT = max(640, ROWS * 20 + 40)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    CELL_SIZE = WIDTH // COLS
    start = (1, 1)
    if mode == "mystery" or (mode == "infinite" and level % 3 == 0):
        goal = (random.randint(1, ROWS), random.randint(1, COLS))
        fake_goals = []
        multiplier = 1 + (level - 1) // 3
        while len(fake_goals) < multiplier:
            f = (random.randint(1, ROWS), random.randint(1, COLS))
            if f != goal and f != start and f not in fake_goals:
                fake_goals.append(f)
    else:
        goal = (ROWS, COLS)

    player_pos = list(start)
    PLAYER_COLOR = RED
    WALL_COLOR = (200, 200, 200)
    START_COLOR = GREEN
    GOAL_COLOR = BLUE

    start_time = time.time()
    time_limit = get_timer(level) if mode == "challenge" else None

    def draw_maze():
        screen.fill(BG_COLOR)
        for x in range(1, COLS + 1):
            for y in range(1, ROWS + 1):
                cell = m.maze_map[(y, x)]
                cx, cy = (x - 1) * CELL_SIZE, (y - 1) * CELL_SIZE
                if (y, x) == start:
                    pygame.draw.rect(screen, START_COLOR, (cx + 5, cy + 5, CELL_SIZE - 10, CELL_SIZE - 10))
                elif (y, x) == goal and not (mode == "infinite" and level % 3 == 0):
                    pygame.draw.rect(screen, GOAL_COLOR, (cx + 5, cy + 5, CELL_SIZE - 10, CELL_SIZE - 10))
                elif mode == "mystery" and (y, x) in fake_goals:
                    pygame.draw.rect(screen, BLUE, (cx + 5, cy + 5, CELL_SIZE - 10, CELL_SIZE - 10))
                if cell['N'] == 0:
                    pygame.draw.line(screen, WALL_COLOR, (cx, cy), (cx + CELL_SIZE, cy), 2)
                if cell['S'] == 0:
                    pygame.draw.line(screen, WALL_COLOR, (cx, cy + CELL_SIZE), (cx + CELL_SIZE, cy + CELL_SIZE), 2)
                if cell['E'] == 0:
                    pygame.draw.line(screen, WALL_COLOR, (cx + CELL_SIZE, cy), (cx + CELL_SIZE, cy + CELL_SIZE), 2)
                if cell['W'] == 0:
                    pygame.draw.line(screen, WALL_COLOR, (cx, cy), (cx, cy + CELL_SIZE), 2)

        level_text = font.render(f"Level: {level}", True, WHITE)
        back_text = font.render("B: Back", True, WHITE)
        screen.blit(level_text, (10, HEIGHT - 30))
        screen.blit(back_text, (WIDTH - back_text.get_width() - 10, HEIGHT - 30))

        if mode == "challenge":
            remaining = max(0, int(time_limit - (time.time() - start_time)))
            time_text = font.render(f"Time Left: {remaining}s", True, YELLOW)
            screen.blit(time_text, ((WIDTH - time_text.get_width()) // 2, HEIGHT - 30))

    def draw_player():
        x, y = player_pos[1] - 1, player_pos[0] - 1
        pygame.draw.rect(screen, PLAYER_COLOR, (x * CELL_SIZE + 5, y * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10))

    def can_move(dir):
        cell = m.maze_map.get(tuple(player_pos))
        return cell.get(dir, 0) == 1

    def show_win():
        text = bigfont.render("Level Completed!", True, YELLOW)
        screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))

    while True:
        draw_maze()
        draw_player()
        if tuple(player_pos) == goal:
            completed = True
            show_win()

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return 'back'

        if mode == "challenge" and (time.time() - start_time > time_limit):
            return 'timeout'

        keys = pygame.key.get_pressed()
        if not completed:
            if keys[pygame.K_UP] and can_move('N'):
                time.sleep(0.1)
                player_pos[0] -= 1
            elif keys[pygame.K_DOWN] and can_move('S'):
                time.sleep(0.1)
                player_pos[0] += 1
            elif keys[pygame.K_LEFT] and can_move('W'):
                time.sleep(0.1)
                player_pos[1] -= 1
            elif keys[pygame.K_RIGHT] and can_move('E'):
                time.sleep(0.1)
                player_pos[1] += 1
        else:
            pygame.time.wait(1000)
            if level > load_highest_level(mode):
                save_highest_level(level, mode)
            return 'next'

# Game loop
level = 1
mode = "classic"
in_home = True


while True:
    if in_home:
        draw_home()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    level = 1
                    mode = "classic"
                    in_home = False
                elif event.key == pygame.K_h:
                    level = 1
                    mode = "challenge"
                    in_home = False
                elif event.key == pygame.K_i:
                    level = 1
                    mode = "infinite"
                    in_home = False
                elif event.key == pygame.K_m:
                    level = 1
                    mode = "mystery"
                    in_home = False
                elif event.key == pygame.K_1:
                    level = load_highest_level("infinite") + 1
                    if level == 2:
                        level = level - 1
                    mode = "infinite"
                    in_home = False
                elif event.key == pygame.K_2:
                    level = load_highest_level("mystery") + 1
                    if level == 2:
                        level = level - 1
                    mode = "mystery"
                    in_home = False
    else:
        result = play_level(level, mode)
        if result == 'next':
            level += 1
        elif result == 'back' or result == 'timeout':
            if result == 'timeout':
              text = bigfont.render("Time Out!", True, RED)
              screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
              pygame.display.flip()
              time.sleep(1.5)
            in_home = True
