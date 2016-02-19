import math

from PIL import ImageOps

import areas_finder
from point import Point
from sketch import Sketch
from triangle import Triangle


#######################################################################
class Seeder(object):
    def __init__(self, source_image, output_folder, num_triangles):
        self.source_image = source_image
        self.size = Point(self.source_image.size[0], self.source_image.size[1])
        self.output_folder = output_folder
        self.num_triangles = num_triangles

    ###################################################################
    def run(self):
        sketches = (self.get_sketch_for_posterity(i) for i in range(1, 9))
        return min(sketches, key=lambda x: x.get_fitness(self.source_image))

    ###################################################################
    def get_triangles_for_rectangle(self, min_x, max_x, min_y, max_y):
        """
        Args:
            min_x: int
            max_x: int
            min_y: int
            max_y: int

        Returns: List(tri_image.triangle.Triangle) of length 2
        """
        c = (0, 0, 0)

        t1 = Triangle([min_x, min_y, min_x, max_y, max_x, max_y], c, 255)
        t1.set_color(self.source_image)
        t2 = Triangle([min_x, min_y, max_x, min_y, max_x, max_y], c, 255)
        t2.set_color(self.source_image)
        return [t1, t2]

    ###################################################################
    def get_triangles_for_area(self, area):
        """
        Given an area, return two triangles that form a box covering it.

        Args:
            area: set of tuples of ints representing pixel coords
        """

        xs = [pixel[0] for pixel in area]
        ys = [pixel[1] for pixel in area]
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)

        return self.get_triangles_for_rectangle(min_x, max_x, min_y, max_y)

    ###################################################################
    def get_sketch_for_posterity(self, num_bits):
        """Posterize the image using the number of bits, then
        find the areas of contiguous color and make triangles out of them,
        returning the resulting sketch

        Args:
            num_bits: int
        """
        im = self.source_image.convert("L")
        im = ImageOps.posterize(im, num_bits)
        im = im.convert("RGB")
        areas = areas_finder.get_areas(im, 1000)

        triangles = []
        for area in areas:
            triangles.extend(self.get_triangles_for_area(area))
        triangles = self.filter_and_sort_triangles(triangles)
        num_background_triangles = max(50, self.num_triangles // 10)
        background_triangles = self.cover_background(num_background_triangles)
        if len(triangles) > (self.num_triangles - num_background_triangles):
            over = len(triangles) - (self.num_triangles - num_background_triangles)
            triangles = triangles[over:]
        triangles = background_triangles + triangles
        return Sketch(self.size, triangles)

    ###################################################################
    def filter_and_sort_triangles(self, triangles):
        """
        Filter_and_sort_triangles will only return up to seeder.num_triangles back.
        it will include the largest triangles, and the triangles will be sorted
        with the largest first on the list (since they are drawn first, they
        will be on bottom, with the smaller triangles drawn on top of them)

        Args:
            triangles: List(tri_image.triangle.Triangle)
        """
        triangles.sort(key=lambda x: x.get_area(), reverse=True)
        return triangles[:self.num_triangles]

    ###################################################################
    def cover_background(self, num_triangles):
        """
        Create a background layer of triangles, using up to num_triangles
        that completely cover the background of the image.  This is to provide
        a backdrop to the other triangles that basically covers the major
        background colors

        Args:
            num_triangles: int
        """
        dimension = int(round(math.sqrt(num_triangles / 2.0)))
        while (dimension * dimension * 2) > num_triangles:
            dimension -= 1
            if dimension <= 0:
                return []

        triangles = []
        block_height = self.size.y // dimension
        block_width = self.size.x // dimension

        for x in range(dimension):
            for y in range(dimension):
                top = y * block_height
                bottom = (y+1) * block_height
                left = x * block_width
                right = (x+1) * block_width
                triangles += self.get_triangles_for_rectangle(left, right, top, bottom)
        return triangles


#######################################################################
class Area(object):
    def __init__(self, color):
        self.color = color
        self.pixels = set()

    ###################################################################
    def is_adjacent(self, x, y):
        up = (x, y-1)
        down = (x, y+1)
        right = (x-1, y)
        left = (x+1, y)

        for pixel in [up, down, right, left]:
            if pixel in self.pixels:
                return True
        return False
