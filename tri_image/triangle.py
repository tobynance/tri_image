import itertools
import math

from PIL import Image, ImageDraw, ImageStat

from point import Point
import utils


########################################################################
class Triangle(object):
    ####################################################################
    def __init__(self, coordinates, color, opacity):
        self.coordinates = coordinates
        self.color = color
        self.opacity = opacity

    ####################################################################
    def get_area(self):
        c = self.coordinates
        return abs((c[0] * (c[3] - c[5]) +
                    c[2] * (c[5] - c[1]) +
                    c[4] * (c[1] - c[3])) / 2.0)

    ####################################################################
    def move(self, dx, dy):
        for i in range(0, len(self.coordinates), 2):
            self.coordinates[i] += dx
            self.coordinates[i+1] += dy

    ####################################################################
    def clone(self):
        return Triangle(self.coordinates[:], self.color, self.opacity)

    ####################################################################
    def get_centroid(self):
        x = sum(self.coordinates[::2])/3.0
        y = sum(self.coordinates[1::2])/3.0
        return Point(x, y)

    ####################################################################
    def scale(self, amount):
        center = self.get_centroid()
        xs = self.coordinates[::2]
        ys = self.coordinates[1::2]
        dxs = [x - center.x for x in xs]
        dys = [y - center.y for y in ys]
        cs = [math.sqrt(x ** 2 + y ** 2) * amount for x, y in zip(dxs, dys)]
        directions = [math.atan2(y, x) for x, y in zip(dxs, dys)]
        new_xs = [int(round(center.x + c * math.cos(d))) for c, d in zip(cs, directions)]
        new_ys = [int(round(center.y + c * math.sin(d))) for c, d in zip(cs, directions)]
        self.coordinates = list(itertools.chain(*zip(new_xs, new_ys)))

    ####################################################################
    def move_point(self, index, dx, dy):
        self.coordinates[index * 2] += dx
        self.coordinates[1 + (index * 2)] += dy

    ####################################################################
    def rotate(self, radians):
        center = self.get_centroid()
        xs = self.coordinates[::2]
        ys = self.coordinates[1::2]
        dxs = [x - center.x for x in xs]
        dys = [y - center.y for y in ys]
        distances = [math.sqrt(x ** 2 + y ** 2) for x, y in zip(dxs, dys)]
        directions = [math.atan2(y, x) + radians for x, y in zip(dxs, dys)]
        new_xs = [int(round(center.x + c * math.cos(d))) for c, d in zip(distances, directions)]
        new_ys = [int(round(center.y + c * math.sin(d))) for c, d in zip(distances, directions)]
        self.coordinates = list(itertools.chain(*zip(new_xs, new_ys)))

    ####################################################################
    def set_color(self, im, color_type):
        new_im = Image.new("1", im.size, color=0)
        draw = ImageDraw.Draw(new_im)
        draw.polygon(self.coordinates, fill=1)

        st = ImageStat.Stat(im, new_im)
        if color_type == utils.RGB:
            self.color = tuple([int(round(x)) for x in st.median])
        else:
            self.color = int(round(st.median[0]))
        self.opacity = 255
