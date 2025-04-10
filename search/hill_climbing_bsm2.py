import random
from core.game_state import GameState

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def heuristic(state):
    if not state.food_positions:
        return 0
    pac = state.pacman_pos
    nearest_food = min(manhattan(pac, food) for food in state.food_positions)
    return nearest_food + len(state.food_positions) * 3  # Peso mais alto para não ficar parado

def hill_climbing_bsm2(start_state, graph_nodes, max_restarts=1000, max_steps=1000):
    total_food = len(start_state.food_positions)
    best_path = None
    best_collected = -1

    for r in range(max_restarts):
        current_state = GameState(
            random.choice(list(graph_nodes.keys())),
            list(start_state.food_positions)
        )
        path = [current_state.pacman_pos]
        current_h = heuristic(current_state)
        visited = set()

        for step in range(max_steps):
            if current_state.is_goal_state():
                print(f"✅ Goal encontrado no restart {r + 1}, passo {step}, comidas: 0")
                return path

            key = (current_state.pacman_pos, frozenset(current_state.food_positions))
            visited.add(key)

            neighbors = []
            for neighbor, _ in graph_nodes[current_state.pacman_pos].neighbors:
                new_state = current_state.copy()
                new_state.move_pacman((neighbor.x, neighbor.y))
                new_key = (new_state.pacman_pos, frozenset(new_state.food_positions))
                if new_key in visited:
                    continue
                h = heuristic(new_state)
                neighbors.append((h, new_state, (neighbor.x, neighbor.y)))

            if not neighbors:
                break

            neighbors.sort(key=lambda x: x[0])
            best_h, best_state, best_pos = neighbors[0]

            if best_h < current_h:
                current_state = best_state
                current_h = best_h
                path.append(best_pos)
            else:
                break  # Ficou preso

        collected = total_food - len(current_state.food_positions)
        print(f"[RESTART {r + 1}/{max_restarts}] Comeu {collected} comidas em {len(path)} passos (restando {len(current_state.food_positions)})")

        if collected > best_collected:
            best_collected = collected
            best_path = path

    print("❌ Nenhuma solução completa encontrada após todos os reinícios.")
    return best_path if best_collected > 0 else None
