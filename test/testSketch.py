import sys, os, Image
from unittest import TestCase

from triangular_image.triangle import Triangle
from triangular_image.point import Point
from triangular_image.sketch import Sketch

#######################################################################
class TestSketch(TestCase):
    ###################################################################
    def tearDown(self):
        if os.path.exists("test.txt"):
            os.remove("test.txt")
        if os.path.exists("test.png"):
            os.remove("test.png")

    ###################################################################
    def test_constructor(self):
        s = Sketch(Point(65, 65))
        s = Sketch(Point(65, 65), [1, 2, 3])

    ###################################################################
    def test_save(self):
        t1 = Triangle([0, 0, 10, 0, 10, 10], (255, 0, 0), 255)
        t2 = Triangle([37, 18, 22, 64, 3, 2], (0, 255, 0), 128)
        s = Sketch(Point(65, 65), [t1, t2])
        s.saveFile("test.txt")
        savedFile = file("test.txt").read().strip()
        expectedFile = file("../data/input/test.txt").read().strip()
        self.assertEqual(savedFile, expectedFile)

    ###################################################################
    def test_read(self):
        s = Sketch.read("../data/input/test.txt")
        self.assertEqual(s.size.x, 65)
        self.assertEqual(s.size.y, 65)
        self.assertEqual(len(s.triangles), 2)
        s.saveFile("test.txt")
        savedFile = file("test.txt").read().strip()
        expectedFile = file("../data/input/test.txt").read().strip()
        self.assertEqual(savedFile, expectedFile)

    ###################################################################
    def test_saveImage(self):
        s = Sketch.read("../data/input/test.txt")
        s.saveImage("test.png")
        im1 = Image.open("test.png")
        im2 = Image.open("../data/input/test.png")
        self.assertEqual(list(im1.getdata()), list(im2.getdata()))

    ###################################################################
    def test_fitness(self):
        s = Sketch.read("../data/input/test.txt")
        im2 = Image.open("../data/input/test.png")
        self.assertEqual(s.getFitness(im2), 0)

        s = Sketch(Point(65, 65))
        self.assertEqual(s.getFitness(im2), 130382)

    ###################################################################
    def test_clone(self):
        s = Sketch.read("../data/input/test.txt")
        s2 = s.clone()
        s.triangles[0].coordinates = [18, 18, 10, 0, 10, 10]
        self.assertEqual(s2.triangles[0].coordinates, [0, 0, 10, 0, 10, 10])
        