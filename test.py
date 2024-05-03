def get_grid_layout(paths):
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    x = y = 0
    for move in path:
        if move == 'W':
            y += 1
        elif move == 'A':
            x -= 1
        elif move == 'S':
            y -= 1
        elif move == 'D':
            x += 1
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    num_columns = max_x - min_x + 1
    num_rows = max_y - min_y + 1

    return num_columns, num_rows

paths = ["WASAWWDDDSS", "DDSAASDDSAA", "DSASSDWDSDWWAWDDDSASSDWDSDWWAWD"]
for path in paths:
    columns, rows = get_grid_layout(path)
    print("Number of columns:", columns)
    print("Number of rows:", rows)
