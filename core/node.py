class Node:
    def __init__(self, x, y, has_food=False):
        self.x = x
        self.y = y
        self.has_food = has_food
        self.neighbors = []  # (Node, cost)
    
    def add_neighbor(self, neighbor_node, cost):
        self.neighbors.append((neighbor_node, cost))
