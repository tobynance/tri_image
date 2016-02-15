import sys, datetime, Image
from unittest import TestCase

from triangular_image.evolver import Evolver, \
    MOVE_POINT, CHANGE_COLOR, CHANGE_OPACITY, MOVE, SCALE, ROTATE

from triangular_image.triangle import Triangle
from triangular_image.point import Point
from triangular_image.sketch import Sketch
from test.utils import withRandom
import triangular_image.utils as utils

#######################################################################
def slow(f):
    f.slow = True
    return f

#######################################################################
class TestEvolver(TestCase):
    ###################################################################
    def getEvolver(self):
        return Evolver(source_image=Image.open("../data/input/test.png"),
                    output_folder="../data/output/test_1",
                    num_triangles=2,
                    save_frequency=datetime.timedelta(seconds=2))

    ###################################################################
    def test_constructor(self):
        e = self.getEvolver()

    ###################################################################
    @withRandom
    def test_randomlyMoveTriangle(self):
        e = self.getEvolver()
        tri = utils.createRandomTriangles(e.size, 1)[0]
        e.randomlyMoveTriangle(tri, variance=20)

        ### the triangle should now have had the center of the triangle
        ### moved by some amount, limited to be between -variance, +variance
        self.assertEqual(tri.coordinates, [12, 14, 15, 17, 18, 20])

    ###################################################################
    @slow
    def test_evolve(self):
        e = self.getEvolver()
        e.run_time = datetime.timedelta(seconds=5)
        triangles = utils.createRandomTriangles(e.size, 2)
        triangles[0].color = (255, 0, 0)
        triangles[0].opacity = 255
        triangles[1].color = (0, 255, 0)
        triangles[1].opacity = 128
#        s = Sketch(Point(65, 65), triangles)
        s = Sketch.read("../data/input/test.txt")
        s.triangles[0].move(14, 24)
        s.triangles[1].move(6, 17)
        better = e.evolve(s)
        better.saveImage("../data/output/test_evolve.png")
        print "*******************************"
        print len(better.triangles)
        print better.triangles[0].coordinates
        print better.triangles[0].color
        print better.triangles[0].opacity
        print better.triangles[1].coordinates
        print better.triangles[1].color
        print better.triangles[1].opacity
        print "*******************************"
        self.assertTrue(better.getFitness(e.source_image) < s.getFitness(e.source_image))
