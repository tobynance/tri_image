import logging
from contextlib import contextmanager
import os
import random
import shutil
import tempfile


GRAY_SCALE = "L"
RGB = "RGB"


########################################################################
def string_to_ints(line):
    return [int(a) for a in line.split()]


########################################################################
def create_random_triangles(size, num_triangles, color_type):
    import triangle
    triangles = []
    for x in range(num_triangles):
        coords = []
        color = []
        for i in range(3):
            coords.append(random.randint(0, size.x))
            coords.append(random.randint(0, size.y))
        if color_type == GRAY_SCALE:
            t = triangle.Triangle(coords, random.randint(0, 255), random.randint(0, 255))
        else:
            for i in range(3):
                color.append(random.randint(0, 255))
            t = triangle.Triangle(coords, tuple(color), random.randint(0, 255))
        triangles.append(t)
    return triangles


########################################################################
def clean_dir(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)


########################################################################
@contextmanager
def temp_directory(suffix, prefix="tmp", delete=True):
    temp_dir = tempfile.mkdtemp(prefix=prefix, suffix=suffix)
    try:
        yield temp_dir
    finally:
        if delete:
            shutil.rmtree(temp_dir, ignore_errors=True)


########################################################################
def get_logger(name):
    return logging.getLogger(name)
