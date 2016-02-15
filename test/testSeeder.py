import os
from PIL import Image

from test.utils import BaseTest
import tri_image.areasFinder as areasFinder
import tri_image.utils as utils

data_folder = os.path.join(os.path.dirname(__file__), "data")


#######################################################################
class TestSeeder(BaseTest):
    ###################################################################
    def test_constructor(self):
        s = self.get_seeder()

    ###################################################################
    def test_Seeder_run(self):
        s = self.get_seeder()

        # should return the best sketch that the seeder can make
        sketch = s.run()
        sketch.saveImage(os.path.join(self.out_folder, "seed.png"))
        sketch.saveFile(os.path.join(self.out_folder, "seed.txt"))
        self.fail("No assertion made")

    ###################################################################
    def test_getTrianglesForArea(self):
        s = self.get_seeder()
        source_im = Image.open(os.path.join(data_folder, "black.png"))
        areas = areasFinder.getAreas(source_im, 1000)
        triangles = s.getTrianglesForArea(areas[0])
        self.assertEqual(len(triangles), 2)
        self.assertEqual(triangles[0].coordinates, [0, 0, 0, 64, 64, 64])
        self.assertEqual(triangles[1].coordinates, [0, 0, 64, 0, 64, 64])

    ###################################################################
    def test_getSketchForPosterity(self):
        s = self.get_seeder()
        num_bits = 1
        sketch = s.getSketchForPosterity(num_bits)
        self.fail("No assertion made")

    ###################################################################
    def test_filterTriangles(self):
        s = self.get_seeder()
        triangles = utils.createRandomTriangles(s.size, 20)
        new_triangles = s.filterAndSortTriangles(triangles)

        self.assertTrue(len(new_triangles) <= s.num_triangles)

        previous_area = new_triangles[0].getArea()
        for tri in new_triangles[1:]:
            area = tri.getArea()
            if area > previous_area:
                self.fail()
            previous_area = area

    ###################################################################
    def test_coverBackground(self):
        im = Image.new("RGB", (20, 20), color=(128, 0, 0))
        s = self.get_seeder(input_image=im)
        new_triangles = s.coverBackground(2)
        self.assertTrue(len(new_triangles) == 2)
        for tri in new_triangles:
            self.assertTrue(tri.color == (128, 0, 0))
