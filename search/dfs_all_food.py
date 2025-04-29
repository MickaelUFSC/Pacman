# search/dfs_all_food.py

from copy import deepcopy

def dfs_all_food(start_state, graph_nodes):
    """
    Busca em profundidade até que todas as comidas sejam consumidas.
    
    :param start_state: instância de GameState
    :param graph_nodes: dicionário {(i,j): Node}
    :return: caminho (lista de posições) ou None
    """
    stack = []
    visited = set()

    key = (start_state.pacman_pos, frozenset(start_state.food_positions))
    stack.append((start_state, []))
    visited.add(key)

    while stack:
        current_state, path = stack.pop()

        if current_state.is_goal_state():
            #print(path)
            return path, visited

        current_node = graph_nodes[current_state.pacman_pos]

        for neighbor, _ in current_node.neighbors:
            new_state = current_state.copy()
            new_state.move_pacman((neighbor.x, neighbor.y))

            new_key = (new_state.pacman_pos, frozenset(new_state.food_positions))
            if new_key not in visited:
                visited.add(new_key)
                stack.append((new_state, path + [new_state.pacman_pos]))

    return None, visited
