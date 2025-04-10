import heapq
from itertools import count
from core.node import Node

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def astar(map_grid, start_pos):
    total_foods = sum(row.count('.') for row in map_grid)

    def heuristic(pos, foods_left):
        dist = sum(manhattan(pos, food) for food in foods_left)
        foods_eaten = total_foods - len(foods_left)
        return dist + 2 * foods_eaten  # Peso ajustável

    rows, cols = len(map_grid), len(map_grid[0])
    food_positions = {(i, j) for i in range(rows) for j in range(cols) if map_grid[i][j] == '.'}
    initial_state = (start_pos, frozenset(food_positions))

    visited = set()
    heap = []
    counter = count()
    start_node = Node(initial_state)
    cost_so_far = {initial_state: 0}
    
    heapq.heappush(heap, (0, next(counter), start_node))

    while heap:
        _, _, node = heapq.heappop(heap)
        pos, foods_left = node.state

        if not foods_left:
            return node.path()

        for action, (di, dj) in [('UP', (-1, 0)), ('DOWN', (1, 0)), ('LEFT', (0, -1)), ('RIGHT', (0, 1))]:
            ni, nj = pos[0] + di, pos[1] + dj
            new_pos = (ni, nj)

            if 0 <= ni < rows and 0 <= nj < cols and map_grid[ni][nj] != '#':
                new_foods_left = set(foods_left)
                if new_pos in new_foods_left:
                    new_foods_left.remove(new_pos)

                new_state = (new_pos, frozenset(new_foods_left))
                new_cost = node.depth + 1

                if new_state not in cost_so_far or new_cost < cost_so_far[new_state]:
                    cost_so_far[new_state] = new_cost
                    priority = new_cost + heuristic(new_pos, new_foods_left)
                    heapq.heappush(heap, (priority, next(counter), Node(new_state, node, action, new_cost)))

    return None
