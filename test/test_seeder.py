import os
from PIL import Image
from unittest import skip
from test.utils import BaseTest
from tri_image import areas_finder
from tri_image import utils

data_folder = os.path.join(os.path.dirname(__file__), "data")


#######################################################################
class TestSeeder(BaseTest):
    ###################################################################
    def test_constructor(self):
        self.get_seeder()

    ###################################################################
    @skip
    def test_Seeder_run(self):
        s = self.get_seeder()

        # should return the best sketch that the seeder can make
        sketch = s.run()
        sketch.save_image(os.path.join(self.out_folder, "seed.png"))
        sketch.save_file(os.path.join(self.out_folder, "seed.txt"))
        self.fail("No assertion made")

    ###################################################################
    def test_get_triangles_for_area(self):
        s = self.get_seeder()
        source_im = Image.open(os.path.join(data_folder, "black.png"))
        areas = areas_finder.get_areas(source_im, 1000)
        triangles = s.get_triangles_for_area(areas[0])
        self.assertEqual(len(triangles), 2)
        self.assertEqual(triangles[0].coordinates, [0, 0, 0, 64, 64, 64])
        self.assertEqual(triangles[1].coordinates, [0, 0, 64, 0, 64, 64])

    ###################################################################
    @skip
    def test_get_sketch_for_posterity(self):
        s = self.get_seeder()
        num_bits = 1
        sketch = s.get_sketch_for_posterity(num_bits)

        self.fail("No assertion made")

    ###################################################################
    def test_filter_triangles(self):
        s = self.get_seeder()
        triangles = utils.create_random_triangles(s.size, 20)
        new_triangles = s.filter_and_sort_triangles(triangles)

        self.assertTrue(len(new_triangles) <= s.num_triangles)

        previous_area = new_triangles[0].get_area()
        for tri in new_triangles[1:]:
            area = tri.get_area()
            if area > previous_area:
                self.fail()
            previous_area = area

    ###################################################################
    def test_coverBackground(self):
        im = Image.new("RGB", (20, 20), color=(128, 0, 0))
        s = self.get_seeder(input_image=im)
        new_triangles = s.cover_background(2)
        self.assertTrue(len(new_triangles) == 2)
        for tri in new_triangles:
            self.assertTrue(tri.color == (128, 0, 0))
