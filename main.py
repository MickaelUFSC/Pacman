from core.map_loader import MapLoader
from core.graph_builder import GraphBuilder
from core.game_state import GameState

from search.bfs_all_food import bfs_all_food
from search.dfs_all_food import dfs_all_food
from search.iddfs_all_food import iddfs_all_food
from search.astar_all_food import astar_all_food
from search.astar_all_food1 import astar_all_food1

from time import time

from gui.visualizer import animate_solution

def escolher_mapa():
    mapas = ["easy.map", "medium.map", "hard.map", "pacmap.map", "pacman.map"]
    print("Escolha o mapa:")
    for i, mapa in enumerate(mapas):
        print(f"{i + 1}. {mapa}")
    escolha = int(input("Digite o número do mapa: ")) - 1
    return f"maps/{mapas[escolha]}"

def escolher_algoritmo():
    algoritmos = {
        "1": ("BFS", bfs_all_food),
        "2": ("DFS", dfs_all_food),
        "3": ("IDDFS", iddfs_all_food),
        "4": ("A*", astar_all_food),
        "5": ("A*1", astar_all_food1),
    }
    print("\nEscolha o algoritmo de busca:")
    for k, (nome, _) in algoritmos.items():
        print(f"{k}. {nome}")
    escolha = input("Digite o número do algoritmo: ")
    return algoritmos[escolha]

def preparar_estado(mapa_path):
    loader = MapLoader(mapa_path)
    grid = loader.load()
    builder = GraphBuilder(grid)
    nodes = builder.build_graph()

    start_pos = None
    food_positions = []

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'P':
                start_pos = (i, j)
            elif cell == '.':
                food_positions.append((i, j))

    state = GameState(start_pos, food_positions)
    return state, nodes, grid

import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
def plot_maze_and_path(maze, path, visited=None):
    """
    Plota o labirinto como uma grade de blocos:
    - paredes (preto),
    - comidas (estrelas amarelas),
    - caminho encontrado (linhas vermelhas),
    - posição inicial (verde),
    - posição final (azul),
    - células visitadas (colormap gradiente ou cinza claro com alpha).
    
    Parâmetros:
        maze: list[list[str]] — labirinto como grade de caracteres.
        path: list[tuple] — lista de posições (linha, coluna) do caminho encontrado.
        visited: iterable[tuple] — estados visitados (posições), opcional.
    """
    rows, cols = len(maze), len(maze[0])
    grid = np.zeros((rows, cols))
    food_positions = []
    start_position = None

    for i in range(rows):
        for j in range(cols):
            ch = maze[i][j]
            if ch == '#':
                grid[i, j] = 1
            elif ch == '.':
                food_positions.append((i, j))
            elif ch == 'P':
                start_position = (i, j)

    # Caminho - prepara coordenadas x e y
    xs = [pos[1] for pos in path]
    ys = [pos[0] for pos in path]

    # Comidas
    food_xs = [j for (_, j) in food_positions]
    food_ys = [i for (i, _) in food_positions]

    plt.figure(figsize=(12, 12))
    plt.imshow(grid, cmap='gray', origin='upper')
    
    # Prepara os estados visitados
    visit_counts = Counter(pos for (pos, _) in visited) if visited else Counter()

    # Prepara listas paralelas para o heatmap
    if visit_counts:
        vx, vy, counts = zip(*[
            (c, r, cnt)
            for ((r, c), cnt) in visit_counts.items()
        ])
    else:
        vx, vy, counts = [], [], []

    # Caminho - agora plotado como linhas vermelhas com setas
    if len(path) > 1:
        # Linha principal
        plt.plot(xs, ys, color='red', linewidth=2, label='Caminho')
        
        # Adiciona setas para mostrar direção
        for i in range(1, len(path)):
            dx = xs[i] - xs[i-1]
            dy = ys[i] - ys[i-1]
            plt.arrow(xs[i-1], ys[i-1], dx*0.8, dy*0.8, 
                      head_width=0.2, head_length=0.2, 
                      fc='red', ec='red', length_includes_head=True)

    if counts:
        sc = plt.scatter(vx, vy,
                         c=counts,
                         cmap='winter',
                         marker='s',
                         s=150,
                         alpha=0.8,
                         label="Visitados")
        plt.colorbar(sc, label="Número de visitas")

    # Início (verde)
    if start_position:
        plt.scatter(start_position[1], start_position[0], color='pink', s=100, label='Início')

    # Comidas
    if food_positions:
        plt.scatter(food_xs, food_ys, color='yellow', marker='*', s=120, label="Comidas")
        
    if path:
        end = path[-1]
        plt.scatter(end[1], end[0], color='orange', s=100, label='Fim')

    plt.title("Labirinto e Caminho Encontrado (com Estados Visitados)")
    plt.legend(loc='upper left')
    plt.axis("off")
    plt.savefig('maze_solution.pdf', bbox_inches='tight')
    plt.show()

def main():
    mapa_path = escolher_mapa()
    algoritmo_nome, algoritmo_func = escolher_algoritmo()
    print(f"\n Rodando {algoritmo_nome} no mapa {mapa_path.split('/')[-1]}...\n")
    time_start = time()
    state, nodes, grid = preparar_estado(mapa_path)
    path, visited = algoritmo_func(state, nodes)
    time_end = time()
    print(f" Tempo de execução: {time_end - time_start:.2f} segundos")
    if path:
        plot_maze_and_path(grid, path, visited)  # Plota o labirinto e o caminho encontrado
        print(f" Caminho encontrado com {len(path)} passos:")
        #print(visited)
        #animate_solution(grid, path)  #visualização animada
    else:
        print(" Não foi possível comer todas as comidas.")
    

if __name__ == "__main__":
    main()