def load_map(file_path):
    with open(file_path, 'r') as f:
        lines = [list(line.strip()) for line in f.readlines()]
    start = None
    for i, row in enumerate(lines):
        for j, cell in enumerate(row):
            if cell == 'P':
                start = (i, j)
    return lines, start