from PIL import Image, ImageDraw, ImageStat, ImageChops
import aggdraw
from point import Point
from triangle import Triangle
from utils import string_to_ints

### The higher the number, the more fewer triangles will be favored
TRIANGLE_WEIGHT = 100

#######################################################################
class Sketch(object):
    def __init__(self, size, triangles=None):
        self.image = None
        self.size = size
        self.cached_fitness = None
        if triangles:
            self.triangles = triangles
        else:
            self.triangles = []

    ###################################################################
    def clearCachedImage(self):
        self.image = None

    ###################################################################
    @classmethod
    def read(klass, filename):
        input_file = file(filename)
        x, y = string_to_ints(input_file.readline())
        s = Sketch(Point(x, y))
        for line in input_file:
            items = string_to_ints(line)
            t = Triangle(items[:6], tuple(items[6:9]), items[9])
            s.triangles.append(t)
        return s

    ###################################################################
    def saveFile(self, filename):
        out_file = file(filename, "w")
        out_file.write("%d %d\n" % (self.size.x, self.size.y))
        for tri in self.triangles:
            out_file.write(" ".join([str(x) for x in tri.coordinates]))
            out_file.write(" %d %d %d " % tri.color)
            out_file.write("%d\n" % tri.opacity)
        out_file.close()

    ###################################################################
    def getImage(self):
        if self.image == None:
            self.image = Image.new("RGB", (self.size.x, self.size.y), (0, 0, 0))
            draw = aggdraw.Draw(self.image)
            for tri in self.triangles:
                b = aggdraw.Brush(tri.color, tri.opacity)
                draw.polygon(tri.coordinates, None, b)
            draw.flush()
        return self.image

    ###################################################################
    def saveImage(self, filename):
        im = self.getImage()
        im.save(filename)

    ###################################################################
    def getFitness(self, other_image):
        if not self.cached_fitness:
            im = self.getImage()
            new_im = ImageChops.difference(im, other_image)
            st = ImageStat.Stat(new_im)
            self.cached_fitness = sum(st.sum[:3]) + len(self.triangles) * TRIANGLE_WEIGHT
        return self.cached_fitness

    ###################################################################
    def clone(self):
        s = Sketch(self.size)
        for tri in self.triangles:
            s.triangles.append(tri.clone())
        return s
