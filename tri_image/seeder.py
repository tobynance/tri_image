import sys, random, time, math
from sketch import Sketch
from triangle import Triangle
from point import Point
from PIL import Image, ImageDraw, ImageStat, ImageOps, ImageChops
import areasFinder


#######################################################################
class Seeder(object):
    def __init__(self, source_image, output_folder, num_triangles):
        self.source_image = source_image
        self.size = Point(self.source_image.size[0], self.source_image.size[1])
        self.output_folder = output_folder
        self.num_triangles = num_triangles

    ###################################################################
    def run(self):
        sketches = (self.getSketchForPosterity(i) for i in range(1, 9))
        return min(sketches, key=lambda x: x.getFitness(self.source_image))

    ###################################################################
    def getTrianglesForRectangle(self, min_x, max_x, min_y, max_y):
        c = (0, 0, 0)

        t1 = Triangle([min_x, min_y, min_x, max_y, max_x, max_y], c, 255)
        t1.setColor(self.source_image)
        t2 = Triangle([min_x, min_y, max_x, min_y, max_x, max_y], c, 255)
        t2.setColor(self.source_image)
        return [t1, t2]
        s1 = Sketch(self.size, [t1, t2])

        t3 = Triangle([min_x, min_y, max_x, min_y, min_x, max_y], c, 255)
        t3.setColor(self.source_image)
        t4 = Triangle([max_x, min_y, max_x, max_y, min_x, max_y], c, 255)
        t4.setColor(self.source_image)
        s2 = Sketch(self.size, [t3, t4])


        fit1 = s1.getFitness(self.source_image)
        fit2 = s2.getFitness(self.source_image)

        if fit1 <= fit2:
            return [t1, t2]
        else:
            return [t3, t4]

    ###################################################################
    def getTrianglesForArea(self, area):
        """Given an area, return two triangles that form a box covering it.
        The box can have the diagonal running either top-left to bottom-right,
        or bottom-left to top-right.  This returns whichever is a better choice"""

        xs = [pixel[0] for pixel in area]
        ys = [pixel[1] for pixel in area]
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)

        return self.getTrianglesForRectangle(min_x, max_x, min_y, max_y)

    ###################################################################
    def getSketchForPosterity(self, num_bits):
        """Posterize the image using the number of bits, then
        find the areas of contiguous color and make triangles out of them,
        returning the resulting sketch"""
        # print "posterity:", num_bits
        im = self.source_image.convert("L")
        im = ImageOps.posterize(im, num_bits)
        im = im.convert("RGB")
        areas = areasFinder.getAreas(im, 1000)

        triangles = []
        for area in areas:
            triangles.extend(self.getTrianglesForArea(area))
        triangles = self.filterAndSortTriangles(triangles)
        num_background_triangles = max(50, self.num_triangles // 10)
        background_triangles = self.coverBackground(num_background_triangles)
        if len(triangles) > (self.num_triangles - num_background_triangles):
            over = len(triangles) - (self.num_triangles - num_background_triangles)
            triangles = triangles[over:]
        triangles = background_triangles + triangles
        # print "num triangles:", len(triangles)
        return Sketch(self.size, triangles)

    ###################################################################
    def filterAndSortTriangles(self, triangles):
        ### filterAndSortTriangles will only return up to seeder.num_triangles back.
        ### it will include the largest triangles, and the triangles will be sorted
        ### with the largest first on the list (since they are drawn first, they
        ### will be on bottom, with the smaller triangles drawn on top of them)
        triangles.sort(key = lambda x: x.getArea(), reverse=True)
        return triangles[:self.num_triangles]

    ###################################################################
    def coverBackground(self, num_triangles):
        ### Create a background layer of triangles, using up to num_triangles
        ### that completely cover the background of the image.  This is to provide
        ### a backdrop to the other triangles that basically covers the major
        ### background colors
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
                triangles += self.getTrianglesForRectangle(left, right, top, bottom)
        return triangles
        
#######################################################################
class Area(object):
    def __init__(self, color):
        self.color = color
        self.pixels = set()

    ###################################################################
    def isAdjacent(self, x, y):
        up = (x, y-1)
        down = (x, y+1)
        right = (x-1, y)
        left = (x+1, y)

        for pixel in [up, down, right, left]:
            if pixel in self.pixels:
                return True
        return False
