from PIL import Image, ImageStat, ImageChops
import aggdraw
from point import Point
from triangle import Triangle
from utils import string_to_ints

# The higher the number, the more the fitness function will favor solutions with fewer triangles
TRIANGLE_WEIGHT = 100


########################################################################
class Sketch(object):
    ####################################################################
    def __init__(self, size, triangles=None):
        self.image = None
        self.size = size
        self.cached_fitness = None
        if triangles:
            self.triangles = triangles
        else:
            self.triangles = []

    ####################################################################
    def clear_cached_image(self):
        self.image = None

    ####################################################################
    @staticmethod
    def read_file_obj(file_obj):
        x, y = string_to_ints(file_obj.readline())
        s = Sketch(Point(x, y))
        for line in file_obj:
            items = string_to_ints(line)
            t = Triangle(items[:6], tuple(items[6:9]), items[9])
            s.triangles.append(t)
        return s

    ####################################################################
    @staticmethod
    def read(filename):
        with open(filename) as input_file:
            return Sketch.read_file_obj(input_file)

    ####################################################################
    def save_file_obj(self, file_obj):
        file_obj.write("%d %d\n" % (self.size.x, self.size.y))
        for tri in self.triangles:
            file_obj.write(" ".join([str(x) for x in tri.coordinates]))
            file_obj.write(" %d %d %d " % tri.color)
            file_obj.write("%d\n" % tri.opacity)

    ####################################################################
    def save_file(self, filename):
        with open(filename, "w") as out_file:
            self.save_file_obj(out_file)

    ####################################################################
    def get_image(self):
        if self.image is None:
            self.image = Image.new("RGB", (self.size.x, self.size.y), (0, 0, 0))
            draw = aggdraw.Draw(self.image)
            for tri in self.triangles:
                b = aggdraw.Brush(tri.color, tri.opacity)
                draw.polygon(tri.coordinates, None, b)
            draw.flush()
        return self.image

    ####################################################################
    def save_image(self, filename):
        im = self.get_image()
        if isinstance(filename, basestring):
            im.save(filename)
        else:
            im.save(filename, format="PNG")

    ####################################################################
    def get_fitness(self, other_image):
        if not self.cached_fitness:
            im = self.get_image()
            new_im = ImageChops.difference(im, other_image)
            st = ImageStat.Stat(new_im)
            # Add in a penalty for number of triangles used
            additional_triangle_weight = len(self.triangles) * TRIANGLE_WEIGHT
            self.cached_fitness = sum(st.sum[:3]) + additional_triangle_weight
        return self.cached_fitness

    ####################################################################
    def clone(self):
        s = Sketch(self.size)
        for tri in self.triangles:
            s.triangles.append(tri.clone())
        return s
