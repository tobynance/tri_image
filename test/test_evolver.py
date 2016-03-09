from test.utils import with_random, BaseTest
import tri_image.utils as utils


#######################################################################
def slow(f):
    f.slow = True
    return f


#######################################################################
class TestEvolver(BaseTest):
    ###################################################################
    def test_constructor(self):
        self.get_evolver()

    ###################################################################
    @with_random
    def test_randomlyMoveTriangle(self):
        e = self.get_evolver()
        tri = utils.create_random_triangles(e.size, 1, utils.RGB)[0]
        self.assertEqual(tri.coordinates, [1, 2, 3, 4, 5, 6])
        e.randomly_move_triangle(tri, variance=20)

        # the triangle should now have had the center of the triangle
        # moved by some amount, limited to be between -variance, +variance
        self.assertEqual(tri.coordinates, [12, 14, 14, 16, 16, 18])
