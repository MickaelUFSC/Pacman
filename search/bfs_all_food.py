# search/bfs_all_food.py

from collections import deque
from copy import deepcopy

def bfs_all_food(start_state, graph_nodes):
    """
    Busca em largura até que todas as comidas sejam consumidas.
    
    :param start_state: instância de GameState (com posição inicial e comidas)
    :param graph_nodes: dicionário {(i,j): Node}
    :return: caminho (lista de posições) ou None
    """
    queue = deque()
    visited = set()
    parent = {}

    key = (start_state.pacman_pos, frozenset(start_state.food_positions))
    queue.append((start_state, []))  # estado atual + caminho até aqui
    visited.add(key)

    while queue:
        current_state, path = queue.popleft()

        if current_state.is_goal_state():
            return path

        current_node = graph_nodes[current_state.pacman_pos]

        for neighbor, _ in current_node.neighbors:
            new_state = current_state.copy()
            new_state.move_pacman((neighbor.x, neighbor.y))

            new_key = (new_state.pacman_pos, frozenset(new_state.food_positions))
            if new_key not in visited:
                visited.add(new_key)
                queue.append((new_state, path + [new_state.pacman_pos]))

    return None
