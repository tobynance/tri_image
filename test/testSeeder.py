import sys, os, Image
from unittest import TestCase

from triangular_image.triangle import Triangle
from triangular_image.point import Point
from triangular_image.sketch import Sketch
from triangular_image.seeder import Seeder
import triangular_image.areasFinder as areasFinder
import triangular_image.utils as utils

#######################################################################
class TestSeeder(TestCase):
    ###################################################################
    def getSeeder(self, input_image="../data/input/test.png", num_triangles=2):
        if isinstance(input_image, str):
            input_image = Image.open(input_image)
        return Seeder(source_image=input_image,
                    output_folder="../data/output/test_1",
                    num_triangles=num_triangles)

    ###################################################################
    def test_constructor(self):
        s = self.getSeeder()

    ###################################################################
    def test_Seeder_run(self):
        s = self.getSeeder()
        ### should return the best sketch that the seeder can make
        sketch = s.run()
        sketch.saveImage("../data/output/seed.png")
        sketch.saveFile("../data/output/seed.txt")

    ###################################################################
    def test_getTrianglesForArea(self):
        s = self.getSeeder()
        source_im = Image.open("../data/input/black.png")
        areas = areasFinder.getAreas(source_im, 1000)
        triangles = s.getTrianglesForArea(areas[0])
        self.assertEqual(len(triangles), 2)
        self.assertEqual(triangles[0].coordinates, [0, 0, 0, 64, 64, 64])
        self.assertEqual(triangles[1].coordinates, [0, 0, 64, 0, 64, 64])

    ###################################################################
    def test_getSketchForPosterity(self):
        s = self.getSeeder()
        num_bits = 1
        sketch = s.getSketchForPosterity(num_bits)

    ###################################################################
    def test_filterTriangles(self):
        s = self.getSeeder()
        triangles = utils.createRandomTriangles(s.size, 20)
        new_triangles = s.filterAndSortTriangles(triangles)
        ### filterAndSortTriangles will only return up to seeder.num_triangles back.
        ### it will include the largest triangles, and the triangles will be sorted
        ### with the largest first on the list (since they are drawn first, they
        ### will be on bottom, with the smaller triangles drawn on top of them)

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
        s = self.getSeeder(input_image=im)
        new_triangles = s.coverBackground(2)
        self.assertTrue(len(new_triangles) == 2)
        for tri in new_triangles:
            self.assertTrue(tri.color == (128, 0, 0))
        