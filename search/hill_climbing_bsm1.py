def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def greedy_count_heuristic(state):
    if not state.food_positions:
        return 0
    pac = state.pacman_pos
    nearest_food = min(manhattan(pac, food) for food in state.food_positions)
    return nearest_food + len(state.food_positions)

def hill_climbing_bsm1(start_state, graph_nodes):
    current_state = start_state
    current_h = greedy_count_heuristic(current_state)
    path = [current_state.pacman_pos]
    visited = set()

    while not current_state.is_goal_state():
        visited.add((current_state.pacman_pos, frozenset(current_state.food_positions)))
        current_node = graph_nodes[current_state.pacman_pos]
        neighbors = []

        for neighbor, _ in current_node.neighbors:
            new_pos = (neighbor.x, neighbor.y)
            new_state = current_state.copy()
            new_state.move_pacman(new_pos)
            key = (new_state.pacman_pos, frozenset(new_state.food_positions))
            if key in visited:
                continue
            h = greedy_count_heuristic(new_state)
            neighbors.append((h, new_state, new_pos))

        if not neighbors:
            break  # Ficou preso

        # Pega o melhor vizinho
        neighbors.sort(key=lambda x: x[0])
        best_h, best_state, best_pos = neighbors[0]

        if best_h >= current_h:
            break  # Nenhum vizinho é melhor

        current_state = best_state
        current_h = best_h
        path.append(best_pos)

    return path if current_state.is_goal_state() else None
