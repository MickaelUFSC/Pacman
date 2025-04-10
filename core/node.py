class Node:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state  # (pos, frozenset(foods_left))
        self.parent = parent
        self.action = action
        self.depth = depth

    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        return list(reversed(p))
