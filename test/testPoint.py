import sys
from unittest import TestCase

from triangular_image.point import Point

#######################################################################
class TestPoint(TestCase):
    ###################################################################
    def test_constructor(self):
        p1 = Point(0, 0)
        p2 = Point(10, 0)
        p3 = Point(10, 10)
