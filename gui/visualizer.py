import pygame
import time

CELL_SIZE = 24
WALL_COLOR = (0, 0, 128)           # Azul escuro
FOOD_COLOR = (255, 255, 0)         # Amarelo
PACMAN_COLOR = (255, 255, 0)       # Amarelo (PacMan)
PATH_COLOR = (50, 50, 150)         # Azul claro
BACKGROUND_COLOR = (0, 0, 0)       # Preto

class Visualizer:
    def __init__(self, map_grid):
        pygame.init()
        self.map_grid = [list(row) for row in map_grid]
        self.rows = len(map_grid)
        self.cols = len(map_grid[0])
        self.width = self.cols * CELL_SIZE
        self.height = self.rows * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PacMan Visualizer")

    def draw_cell(self, row, col, color):
        pygame.draw.rect(
            self.screen,
            color,
            (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

    def draw_food(self, row, col):
        center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        radius = CELL_SIZE // 6
        pygame.draw.circle(self.screen, FOOD_COLOR, center, radius)

    def draw_pacman(self, row, col):
        center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        radius = CELL_SIZE // 2 - 2
        pygame.draw.circle(self.screen, PACMAN_COLOR, center, radius)

    def draw_map(self):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.map_grid[i][j]
                if cell == '#':
                    self.draw_cell(i, j, WALL_COLOR)
                else:
                    self.draw_cell(i, j, BACKGROUND_COLOR)
                    if cell == '.':
                        self.draw_food(i, j)

    def update_pacman_position(self, old_pos, new_pos):
        row, col = old_pos
        if self.map_grid[row][col] == '.':
            self.map_grid[row][col] = ' '  # comeu a comida
        self.draw_cell(row, col, BACKGROUND_COLOR)

        row, col = new_pos
        self.draw_pacman(row, col)

    def visualize(self, path):
        clock = pygame.time.Clock()
        self.draw_map()
        pygame.display.update()
        
        # Aguarda o pressionamento da tecla espaço para iniciar
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
        
        for i in range(1, len(path)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.update_pacman_position(path[i-1], path[i])
            pygame.display.update()
            clock.tick(10)  # 10 frames por segundo

        # Espera até o usuário fechar
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

def animate_solution(map_grid, path):
    vis = Visualizer(map_grid)
    vis.visualize(path)
