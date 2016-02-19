import math
from unittest import skip

from PIL import Image

from test.utils import BaseTest
from tri_image.triangle import Triangle
from tri_image.point import Point


#######################################################################
class TestTriangle(BaseTest):
    ###################################################################
    def test_constructor(self):
        c = (0, 0, 0)
        Triangle([0, 0, 10, 0, 10, 10], c, 255)

    ###################################################################
    @skip
    def test_area(self):
        # a triangle has three points, and 4 color bands (RGBA)
        c = (0, 0, 0)
        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        self.assertEqual(t.get_area(), 50)

        t = Triangle([10, 10, 0, 0, 10, 0], c, 255)
        self.assertEqual(t.get_area(), 50)

        t = Triangle([0, 0, 5, 0, 5, 10], c, 255)
        self.assertEqual(t.get_area(), 25)

        self.fail("I need to test some non-right triangles, as well as non-axially aligned triangles")

    ###################################################################
    def test_coordinates(self):
        c = (0, 0, 0)
        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        self.assertEqual([0, 0, 10, 0, 10, 10], t.coordinates)

        t = Triangle([10, 10, 0, 0, 10, 0], c, 255)
        self.assertEqual([10, 10, 0, 0, 10, 0], t.coordinates)

        t = Triangle([0, 0, 5, 0, 5, 10], c, 255)
        self.assertEqual([0, 0, 5, 0, 5, 10], t.coordinates)

    ###################################################################
    def test_move(self):
        c = (0, 0, 0)
        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        t.move(18, 9)
        self.assertEqual([18, 9, 28, 9, 28, 19], t.coordinates)

    ###################################################################
    def test_clone(self):
        c = (0, 128, 0)
        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        t2 = t.clone()
        t.coordinates = [18, 0, 10, 0, 10, 10]
        t.color = (255, 0, 0)
        t.opacity = 128

        self.assertEqual(t2.coordinates, [0, 0, 10, 0, 10, 10])
        self.assertEqual(t2.color, c)
        self.assertEqual(t2.opacity, 255)

    ###################################################################
    def test_scale(self):
        c = (0, 0, 0)
        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        # 0 10 10
        # 0  0 10
        center_x = 20.0/3
        center_y = 10.0/3

        t.scale(1.0)
        self.assertEquals(t.coordinates, [0, 0, 10, 0, 10, 10])

        t.scale(1.8)
        self.assertEquals(t.coordinates, [-5, -3, 13, -3, 13, 15])

        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        t.scale(2.0)
        self.assertEquals(t.coordinates, [-7, -3, 13, -3, 13, 17])

        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        t.scale(4.0)
        self.assertEquals(t.coordinates, [-20, -10, 20, -10, 20, 30])

    ###################################################################
    def test_getCentroid(self):
        c = (0, 0, 0)
        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        # 0 10 10
        # 0  0 10
        center_x = 20.0/3
        center_y = 10.0/3
        self.assertEquals(t.get_centroid(), Point(center_x, center_y))

    ###################################################################
    def test_movePoint(self):
        c = (0, 0, 0)
        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        # 0 10 10
        # 0  0 10
        t.move_point(0, 2, 2)
        t.move_point(1, 23, -6)
        t.move_point(2, -14, 42)
        self.assertEqual(t.coordinates, [2, 2, 33, -6, -4, 52])

    ###################################################################
    def test_rotate(self):
        c = (0, 0, 0)
        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        t.rotate(2 * math.pi)
        self.assertEquals(t.coordinates, [0, 0, 10, 0, 10, 10])

    ###################################################################
    def test_setColor(self):
        c = (255, 0, 0)
        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        im = Image.open(self._data("black.png"))
        t.set_color(im)
        self.assertEqual(t.color, (0, 0, 0))
        self.assertEqual(t.opacity, 255)

        c = (255, 0, 0)
        t = Triangle([0, 0, 10, 0, 10, 10], c, 255)
        im = Image.open(self._data("green.png"))
        t.set_color(im)
        self.assertEqual(t.color, (0, 255, 0))
        self.assertEqual(t.opacity, 255)
