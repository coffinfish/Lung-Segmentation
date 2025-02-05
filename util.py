import numpy as np

DELTA = [(0,1),(0,-1),(-1,0),(1,0)]

def safe(coords, max):
    x,y = coords
    return True if 0 <= x <= max-1 and 0 <= y <= max-1 else False

def removebg(image:np.ndarray, coord:tuple):
    x,y = coord
    if x < 0 or x >= len(image) or y < 0 or y >= len(image[0]):
        return image

    stack = [(x, y)]
    visited = set()
    new_image = image.copy()

    while stack:
        curr_x, curr_y = stack.pop()
        if (curr_x, curr_y) in visited:
            continue
        visited.add((curr_x, curr_y))
        # Set the current val to 0 (black)
        new_image[curr_x][curr_y] = 0

        # Add neighboring pixels with the same value to the stack
        for dx, dy in DELTA:
            new_x, new_y = curr_x + dx, curr_y + dy
            if 0 <= new_x < len(image) and 0 <= new_y < len(image[0]) and (image[new_x][new_y] == image[curr_x][curr_y]):
                stack.append((new_x, new_y))

    return new_image

