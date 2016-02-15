import sys
from unittest import TestCase

from triangular_image.utils import string_to_ints
from test.utils import withRandom

#######################################################################
class TestUtils(TestCase):
    ###################################################################
    def test_string_to_ints(self):
        self.assertEqual([1, 2, 3], string_to_ints("1 2 3"))

    ###################################################################
    @withRandom
    def test_create_random_triangles(self):
        self.fail()
        e = self.getEvolver()
        items = e.createRandomTriangles(2)
        self.assertEqual(len(items), 2)
        self.assertTrue(isinstance(items[0], Triangle))
        self.assertEqual(items[0].coordinates, [1, 2, 4, 5, 7, 8])
        self.assertEqual(items[0].color, (3, 6, 9))
        self.assertEqual(items[0].opacity, 10)

        items = e.createRandomTriangles(4)
        self.assertEqual(len(items), 4)
        self.assertTrue(isinstance(items[0], Triangle))
