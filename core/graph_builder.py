from core.node import Node

class GraphBuilder:
    def __init__(self, grid):
        self.grid = grid
        self.nodes = {}
    
    def build_graph(self):
        rows, cols = len(self.grid), len(self.grid[0])
        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] != '#':
                    has_food = self.grid[i][j] == '.'
                    self.nodes[(i, j)] = Node(i, j, has_food)

        for (i, j), node in self.nodes.items():
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = i + dx, j + dy
                if (ni, nj) in self.nodes:
                    neighbor = self.nodes[(ni, nj)]
                    cost = 0.5 if neighbor.has_food else 1
                    node.add_neighbor(neighbor, cost)
        
        return self.nodes
