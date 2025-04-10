from core.map_loader import MapLoader
from core.graph_builder import GraphBuilder
from core.game_state import GameState

from search.bfs_all_food import bfs_all_food
from search.dfs_all_food import dfs_all_food
from search.iddfs_all_food import iddfs_all_food
from search.astar_all_food import astar_all_food
from search.hill_climbing_bsm1 import hill_climbing_bsm1
from search.hill_climbing_bsm2 import hill_climbing_bsm2
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
        "5": ("BSM1",hill_climbing_bsm1),
        "6": ("BSM2",hill_climbing_bsm2),
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

def main():
    mapa_path = escolher_mapa()
    algoritmo_nome, algoritmo_func = escolher_algoritmo()
    print(f"\n🧠 Rodando {algoritmo_nome} no mapa {mapa_path.split('/')[-1]}...\n")
    time_start = time()
    state, nodes, grid = preparar_estado(mapa_path)
    path = algoritmo_func(state, nodes)
    time_end = time()
    print(f" Tempo de execução: {time_end - time_start:.2f} segundos")
    if path:
        print(f" Caminho encontrado com {len(path)} passos:")
        animate_solution(grid, path)  # <<< visualização animada
    else:
        print(" Não foi possível comer todas as comidas.")
    

if __name__ == "__main__":
    main()