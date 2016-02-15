from PIL import Image

from test.utils import BaseTest
from tri_image import areasFinder


#######################################################################
class TestAreasFinder(BaseTest):
    ###################################################################
    def test_FloodFindAreas(self):
        s = self.get_seeder()
        areas = areasFinder.getAreas(Image.open(self._data("black.png")), 100)
        self.assertEqual(len(areas), 1)

        areas = areasFinder.getAreas(Image.open(self._data("test.png")), 100)
        self.assertGreater(len(areas), 3)

        areas = areasFinder.getAreas(Image.open(self._data("test03.png")), 100)
        self.assertGreater(len(areas), 2)

    ###################################################################
    def test_generateRandomPoints(self):
        index = 0
        for x, y in areasFinder.getRandomPoints(300, 20, 20):
            index += 1
        self.assertEqual(index, 300)

