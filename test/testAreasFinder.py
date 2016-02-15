import sys
from unittest import TestCase

from triangular_image.utils import string_to_ints
from test.utils import withRandom

#######################################################################
class TestAreasFinder(TestCase):
    ###################################################################
    def test_FloodFindAreas(self):
        s = self.getSeeder()
        areas = s.floodFindAreas(Image.open("../../data/input/black.png"))
        self.assertEqual(len(areas), 1)

        areas = s.floodFindAreas(Image.open("../../data/input/test.png"))
        #self.assertEqual(len(areas), 4)

        areas = s.floodFindAreas(Image.open("../../data/input/test03.png"))
        #self.assertEqual(len(areas), 3)

    ###################################################################
    def test_generateRandomPoints(self):
        index = 0
        for x, y in generateRandomPoints(300, 20, 20):
            index += 1
        self.assertEqual(index, 300)

