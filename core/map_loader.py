class MapLoader:
    def __init__(self, filepath):
        self.filepath = filepath
    
    def load(self):
        with open(self.filepath, 'r') as file:
            return [list(line.strip()) for line in file.readlines()]
