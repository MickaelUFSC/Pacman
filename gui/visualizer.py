import pygame
import time

TILE_SIZE = 30
WALL_COLOR = (0, 0, 0)
FOOD_COLOR = (255, 215, 0)
PACMAN_COLOR = (50, 200, 255)
BG_COLOR = (255, 255, 255)

def draw_grid(screen, map_grid, pac_pos, foods):
    screen.fill(BG_COLOR)
    for i, row in enumerate(map_grid):
        for j, cell in enumerate(row):
            x, y = j * TILE_SIZE, i * TILE_SIZE
            if cell == '#':
                pygame.draw.rect(screen, WALL_COLOR, (x, y, TILE_SIZE, TILE_SIZE))
            elif (i, j) in foods:
                pygame.draw.circle(screen, FOOD_COLOR, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), TILE_SIZE // 6)

    # Desenha o PacMan
    pi, pj = pac_pos
    pygame.draw.circle(screen, PACMAN_COLOR, (pj * TILE_SIZE + TILE_SIZE // 2, pi * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)

    pygame.display.flip()

def animate_solution(map_grid, solution_path):
    pygame.init()
    rows, cols = len(map_grid), len(map_grid[0])
    screen = pygame.display.set_mode((cols * TILE_SIZE, rows * TILE_SIZE))
    pygame.display.set_caption("Busca Visual")

    foods = {(i, j) for i in range(rows) for j in range(cols) if map_grid[i][j] == '.'}

    for node in solution_path:
        pos, remaining = node.state
        draw_grid(screen, map_grid, pos, remaining)
        time.sleep(0.1)

    print("✅ Animação concluída.")
    pygame.time.wait(2000)
    pygame.quit()
