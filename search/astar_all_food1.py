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
    food_set = state.food_positions

    if not food_set:
        return 0

    food = list(food_set)

    # Menor distância até uma comida
    min_to_food = min(manhattan(pac, f) for f in food)

    # Maior distância entre qualquer par de comidas
    max_between_foods = 0
    for i in range(len(food)):
        for j in range(i + 1, len(food)):
            dist = manhattan(food[i], food[j])
            if dist > max_between_foods:
                max_between_foods = dist

    # Número de comidas restantes
    food_count = len(food)

    # Clusters de comidas (comidas próximas entre si)
    cluster_bonus = 0
    for f1 in food:
        cluster_bonus += sum(1 for f2 in food if f1 != f2 and manhattan(f1, f2) <= 2)

    return (
        min_to_food * 1.0 +
        max_between_foods * 1.0 +
        food_count * 1.2 -
        cluster_bonus * 0.3
    )


def astar_all_food(start_state, graph_nodes):
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
