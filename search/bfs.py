from collections import deque
from core.node import Node

def bfs(map_grid, start_pos):
    rows, cols = len(map_grid), len(map_grid[0])

    # Coletar todas as posições com comida
    food_positions = {(i, j) for i in range(rows) for j in range(cols) if map_grid[i][j] == '.'}
    initial_state = (start_pos, frozenset(food_positions))

    visited = set()
    visited.add(initial_state)

    queue = deque([Node(initial_state)])

    while queue:
        node = queue.popleft()
        pos, foods_left = node.state

        # Condição de sucesso: todas as comidas foram coletadas
        if not foods_left:
            return node.path()

        for action, (di, dj) in [('UP', (-1, 0)), ('DOWN', (1, 0)), ('LEFT', (0, -1)), ('RIGHT', (0, 1))]:
            ni, nj = pos[0] + di, pos[1] + dj
            new_pos = (ni, nj)

            if (0 <= ni < rows and 0 <= nj < cols and map_grid[ni][nj] != '#'):
                new_foods_left = set(foods_left)
                if new_pos in new_foods_left:
                    new_foods_left.remove(new_pos)

                new_state = (new_pos, frozenset(new_foods_left))
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(Node(new_state, node, action, node.depth + 1))
    return None
