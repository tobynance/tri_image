import datetime
from tri_image.sketch import Sketch
from test.utils import withRandom, BaseTest
import tri_image.utils as utils


#######################################################################
def slow(f):
    f.slow = True
    return f


#######################################################################
class TestEvolver(BaseTest):
    ###################################################################
    def test_constructor(self):
        e = self.get_evolver()

    ###################################################################
    @withRandom
    def test_randomlyMoveTriangle(self):
        e = self.get_evolver()
        tri = utils.createRandomTriangles(e.size, 1)[0]
        e.randomlyMoveTriangle(tri, variance=20)

        # the triangle should now have had the center of the triangle
        # moved by some amount, limited to be between -variance, +variance
        self.assertEqual(tri.coordinates, [12, 14, 15, 17, 18, 20])

    ###################################################################
    @slow
    def test_evolve(self):
        e = self.get_evolver()
        e.run_time = datetime.timedelta(seconds=5)
        triangles = utils.createRandomTriangles(e.size, 2)
        triangles[0].color = (255, 0, 0)
        triangles[0].opacity = 255
        triangles[1].color = (0, 255, 0)
        triangles[1].opacity = 128
        s = Sketch.read(self._data("sketch01.txt"))
        s.triangles[0].move(14, 24)
        s.triangles[1].move(6, 17)
        better = e.evolve(s)
        better.saveImage(self._out("test_evolve.png"))
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
