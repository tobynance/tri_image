from PIL import Image

from test.utils import BaseTest
from tri_image import areas_finder


#######################################################################
class TestAreasFinder(BaseTest):
    ###################################################################
    def test_flood_find_areas(self):
        areas = areas_finder.get_areas(Image.open(self._data("black.png")), 100)
        self.assertEqual(len(areas), 1)

        areas = areas_finder.get_areas(Image.open(self._data("test.png")), 100)
        self.assertGreater(len(areas), 3)

        areas = areas_finder.get_areas(Image.open(self._data("test03.png")), 100)
        self.assertGreater(len(areas), 2)

    ###################################################################
    def test_generate_random_points(self):
        count = len(list(areas_finder.get_random_points(300, 20, 20)))
        self.assertEqual(count, 300)

