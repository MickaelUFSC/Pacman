import heapq
import itertools

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def count_connected_food(food_positions, radius=3):
    clusters = 0
    for food in food_positions:
        neighbors = sum(1 for other in food_positions if other != food and manhattan(food, other) <= radius)
        clusters += neighbors
    return clusters

def heuristic(state):
    pac = state.pacman_pos
    foods = state.food_positions
    if not foods:
        return 0

    # Distância até o alimento mais próximo
    min_dist = min(manhattan(pac, food) for food in foods)

    # Quantidade de comida
    food_count = len(foods)

    # Estimativa de agrupamento mais leve (sem calcular todos os vizinhos)
    # Considera a distância média de cada comida até o centroide (boa aproximação)
    avg_cluster_dist = 0
    if food_count > 1:
        cx = sum(f[0] for f in foods) / food_count
        cy = sum(f[1] for f in foods) / food_count
        avg_cluster_dist = sum(abs(f[0] - cx) + abs(f[1] - cy) for f in foods) / food_count

    return min_dist * 1.5 + food_count * 2 + avg_cluster_dist * 1.2


def astar_all_food1(start_state, graph_nodes):
    """
    A* para comer todas as comidas.
    :param start_state: GameState
    :param graph_nodes: dicionário de nós (grafo)
    :return: caminho (lista de posições) ou None
    """
    open_set = []
    visited = set()
    counter = itertools.count()  # Desempate para heapq

    start_h = heuristic(start_state)
    heapq.heappush(open_set, (start_h, 0, next(counter), start_state, [start_state.pacman_pos]))

    while open_set:
        f, g, _, current_state, path = heapq.heappop(open_set)

        key = (current_state.pacman_pos, frozenset(current_state.food_positions))
        if key in visited:
            continue
        visited.add(key)

        if current_state.is_goal_state():
            return path

        current_node = graph_nodes[current_state.pacman_pos]
        for neighbor, cost in current_node.neighbors:
            new_pos = (neighbor.x, neighbor.y)

            new_state = current_state.copy()
            new_state.move_pacman(new_pos)

            new_g = g + cost
            new_h = heuristic(new_state)
            new_f = new_g + new_h

            heapq.heappush(open_set, (new_f, new_g, next(counter), new_state, path + [new_pos]))

    return None
