import numpy
import random


#######################################################################
def grid_from_image(im):
    im = im.convert("L")
    grid = numpy.zeros(im.size)
    pix = im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            grid[x, y] = pix[x, y]
    return grid


#######################################################################
def get_random_points(num_points, width, height):
    for i in range(num_points):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        yield x, y


#######################################################################
def get_areas(im, num_points):
    grid = grid_from_image(im)
    areas = []
    for x, y in get_random_points(num_points, grid.shape[0], grid.shape[1]):
        area = flood_fill_area(grid, x, y)
        if area:
            areas.append(area)
    return areas


#######################################################################
def flood_fill_area(grid, x, y):
    search_color = grid[x, y]
    if search_color == -1:
        return None

    area = set()
    pixel_queue = set()
    pixel_queue.add((x, y))
    while len(pixel_queue) > 0:
        x, y = pixel_queue.pop()
        area.add((x, y))
        grid[x, y] = -1
        for a, b in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= a < grid.shape[0] and 0 <= b < grid.shape[1]:
                if grid[a, b] == search_color:
                    pixel_queue.add((a, b))
    return area
