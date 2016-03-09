from unittest import TestCase, skip

from tri_image.point import Point


#######################################################################
class TestPoint(TestCase):
    ###################################################################
    def test_constructor(self):
        Point(0, 0)
        Point(10, 0)
        Point(10, 10)

    ####################################################################
    @skip("unwritten")
    def test_equal(self):
        self.fail("Unwritten")

    ####################################################################
    @skip("unwritten")
    def test_not_equal(self):
        self.fail("Unwritten")
