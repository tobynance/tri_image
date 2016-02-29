from PIL import Image, ImageStat, ImageChops
import aggdraw
from point import Point
from triangle import Triangle
from utils import string_to_ints, RGB

# The higher the number, the more the fitness function will favor solutions with fewer triangles
TRIANGLE_WEIGHT = 100


########################################################################
class Sketch(object):
    ####################################################################
    def __init__(self, size, color_type, triangles=None):
        assert isinstance(color_type, basestring)
        self.image = None
        self.size = size
        self.color_type = color_type
        self.cached_fitness = None
        self.triangles = triangles or []

    ####################################################################
    def clear_cached_image(self):
        self.image = None

    ####################################################################
    @staticmethod
    def read_file_obj(file_obj):
        first_line = file_obj.readline()
        items = first_line.split()
        x, y = [int(a) for a in items[:2]]
        if len(items) == 3:
            color_type = items[2]
        else:
            color_type = RGB
        s = Sketch(Point(x, y), color_type)
        for line in file_obj:
            items = string_to_ints(line)
            if color_type == RGB:
                t = Triangle(items[:6], tuple(items[6:9]), items[9])
            else:
                t = Triangle(items[:6], items[6], items[7])
            s.triangles.append(t)
        return s

    ####################################################################
    @staticmethod
    def read(filename):
        with open(filename) as input_file:
            return Sketch.read_file_obj(input_file)

    ####################################################################
    def save_file_obj(self, file_obj):
        file_obj.write("%d %d %s\n" % (self.size.x, self.size.y, self.color_type))
        for tri in self.triangles:
            file_obj.write(" ".join([str(x) for x in tri.coordinates]))
            if self.color_type == RGB:
                file_obj.write(" %d %d %d " % tri.color)
            else:
                file_obj.write(" %d " % tri.color)
            file_obj.write("%d\n" % tri.opacity)

    ####################################################################
    def save_file(self, filename):
        with open(filename, "w") as out_file:
            self.save_file_obj(out_file)

    ####################################################################
    def get_image(self):
        if self.image is None:
            if self.color_type == RGB:
                black = (0, 0, 0)
            else:
                black = 0
            self.image = Image.new(self.color_type, (self.size.x, self.size.y), black)
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
        s = Sketch(self.size, self.color_type)
        for tri in self.triangles:
            s.triangles.append(tri.clone())
        return s
