from copy import deepcopy

def iddfs_all_food(start_state, graph_nodes, max_depth=300):
    """
    Busca em profundidade iterativa para comer todas as comidas.
    
    :param start_state: GameState inicial
    :param graph_nodes: dicionário {(i,j): Node}
    :param max_depth: profundidade máxima a tentar
    :return: caminho (lista de posições) ou None
    """
    for depth in range(max_depth + 1):
        visited = set()
        result = dls(start_state, graph_nodes, depth, [], visited)
        if result:
            return result
    return None

def dls(state, graph_nodes, depth, path, visited):
    """
    Busca limitada em profundidade (Depth-Limited Search)
    
    :param state: estado atual
    :param graph_nodes: grafo
    :param depth: profundidade restante
    :param path: caminho percorrido
    :param visited: conjunto de estados visitados
    """
    key = (state.pacman_pos, frozenset(state.food_positions))
    if key in visited:
        return None
    visited.add(key)

    if state.is_goal_state():
        return path

    if depth == 0:
        return None

    current_node = graph_nodes[state.pacman_pos]

    for neighbor, _ in current_node.neighbors:
        new_state = state.copy()
        new_pos = (neighbor.x, neighbor.y)
        new_state.move_pacman(new_pos)

        result = dls(new_state, graph_nodes, depth - 1, path + [new_pos], visited)
        if result:
            return result

    return None