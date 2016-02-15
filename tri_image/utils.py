import os, random
import shutil
from triangle import Triangle
#######################################################################
def string_to_ints(line):
    return [int(a) for a in line.split()]

#######################################################################
def createRandomTriangles(size, num_triangles):
    triangles = []
    for x in range(num_triangles):
        coords = []
        color = []
        for i in range(3):
            coords.append(random.randint(0, size.x))
            coords.append(random.randint(0, size.y))
            color.append(random.randint(0, 255))
        t = Triangle(coords, tuple(color), random.randint(0, 255))
        triangles.append(t)
    return triangles

#######################################################################
def cleanDir(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)
