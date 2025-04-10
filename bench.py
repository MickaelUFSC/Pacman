import time
import multiprocessing
from core.map_loader import MapLoader
from core.graph_builder import GraphBuilder
from core.game_state import GameState

from search.astar_all_food import astar_all_food
from search.astar_all_food1 import astar_all_food as astar_all_food1
from search.bfs_all_food import bfs_all_food
from search.dfs_all_food import dfs_all_food
from search.iddfs_all_food import iddfs_all_food

MAPAS = ["easy.map", "medium.map", "hard.map"]
ALGORITMOS = {
    "A* - H1": astar_all_food,
    "A* - H2": astar_all_food1,
    "BFS": bfs_all_food,
    "DFS": dfs_all_food,
    "IDDFS": iddfs_all_food
}

TIME_LIMIT = 10.0  # segundos


import matplotlib.pyplot as plt

def gerar_graficos(resultados):
    import matplotlib.pyplot as plt

    mapas = ["easy.map", "medium.map", "hard.map"]
    algoritmos = sorted(set(r["Algoritmo"] for r in resultados))

    for metrica in ["Tempo (s)", "Passos"]:
        plt.figure(figsize=(10, 6))
        for mapa in mapas:
            valores = []
            for alg in algoritmos:
                r = next((x for x in resultados if x["Mapa"] == mapa and x["Algoritmo"] == alg), None)
                valor = r[metrica]
                if isinstance(valor, (int, float)):
                    valores.append(valor)
                elif isinstance(valor, str) and valor.startswith(">"):
                    valores.append(11)  # barra simbólica para "timeout"
                else:
                    valores.append(0)
            plt.bar([f"{alg}\n{mapa}" for alg in algoritmos], valores, label=mapa)

        plt.title(f"Comparativo: {metrica}")
        plt.xticks(rotation=45, ha='right')
        plt.ylabel(metrica)
        plt.tight_layout()
        plt.grid(True, axis='y')
        plt.savefig(f"grafico_{metrica.replace(' ', '_').lower()}.png")
        plt.show()


def preparar_estado(mapa_path):
    loader = MapLoader(f"maps/{mapa_path}")
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
    return state, nodes

# Função de execução no processo separado (precisa ser global)
def exec_alg(alg_func, state, graph, queue):
    try:
        result = alg_func(state, graph)
        queue.put(result)
    except Exception as e:
        queue.put(e)

def run_with_timeout(func, state, graph, timeout):
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=exec_alg, args=(func, state, graph, queue))
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        return "TIMEOUT"
    elif not queue.empty():
        return queue.get()
    else:
        return "EXCEPTION"

def benchmark():
    resultados = []

    for mapa in MAPAS:
        for nome_alg, algoritmo in ALGORITMOS.items():
            print(f"\n▶️ Testando {nome_alg} no mapa {mapa}...")

            try:
                state, graph = preparar_estado(mapa)
                start = time.time()

                result = run_with_timeout(algoritmo, state.copy(), graph, TIME_LIMIT)

                if result == "TIMEOUT":
                    resultados.append({
                        "Mapa": mapa,
                        "Algoritmo": nome_alg,
                        "Tempo (s)": ">10s",
                        "Passos": "—"
                    })
                    print("⏱️ Timeout excedido.")
                elif isinstance(result, Exception):
                    raise result
                else:
                    duracao = time.time() - start
                    path = result
                    passos = len(path) if path else "—"

                    resultados.append({
                        "Mapa": mapa,
                        "Algoritmo": nome_alg,
                        "Tempo (s)": round(duracao, 2),
                        "Passos": passos
                    })

            except Exception as e:
                resultados.append({
                    "Mapa": mapa,
                    "Algoritmo": nome_alg,
                    "Tempo (s)": "Erro",
                    "Passos": str(e)
                })

    print("\n📊 RESULTADOS:")
    for r in resultados:
        print(f"{r['Mapa']:10} | {r['Algoritmo']:12} | {r['Tempo (s)']:>7} | Passos: {r['Passos']}")
    gerar_graficos(resultados)
if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    benchmark()
