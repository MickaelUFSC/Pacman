import argparse
import time
from core.map_loader import load_map
from search.bfs import bfs
from search.dfs import dfs
from search.astar import astar  
from gui.visualizer import animate_solution

def print_solution(path, elapsed_time):
    if not path:
        print("Nenhuma solução encontrada.")
        return
    for node in path:
        print(f"{node.state[0]} -> {node.action}")
    print(f"\n✅ Solução encontrada com {len(path) - 1} movimentos.")
    print(f"⏱️ Tempo de execução: {elapsed_time:.4f} segundos.\n")
def main():
    parser = argparse.ArgumentParser(description="Busca no Pacman")
    parser.add_argument('--map', choices=['easy', 'medium', 'hard'], default='easy', help='Mapa a ser usado')
    parser.add_argument('--alg', choices=['bfs', 'dfs', 'astar'], default='bfs', help='Algoritmo de busca')

    args = parser.parse_args()

    map_path = f"maps/{args.map}.map"
    map_grid, start = load_map(map_path)

    print(f"🔍 Executando {args.alg.upper()} no mapa {args.map}...\n")

    start_time = time.time()

    if args.alg == 'bfs':
        solution = bfs(map_grid, start)
    elif args.alg == 'dfs':
        solution = dfs(map_grid, start)
    elif args.alg == 'astar':
        solution = astar(map_grid, start)

    elapsed_time = time.time() - start_time
    print_solution(solution, elapsed_time)
    
    if solution:
        animate_solution(map_grid, solution)

if __name__ == '__main__':
    main()
