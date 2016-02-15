from tri_image import utils
from tri_image.triangle import Triangle
from test.utils import withRandom, BaseTest


#######################################################################
class TestUtils(BaseTest):
    ###################################################################
    def test_string_to_ints(self):
        self.assertEqual([1, 2, 3], utils.string_to_ints("1 2 3"))

    ###################################################################
    @withRandom
    def test_create_random_triangles(self):
        e = self.get_evolver()
        items = utils.createRandomTriangles(e.size, 2)
        self.assertEqual(len(items), 2)
        self.assertTrue(isinstance(items[0], Triangle))
        self.assertEqual(items[0].coordinates, [1, 2, 4, 5, 7, 8])
        self.assertEqual(items[0].color, (3, 6, 9))
        self.assertEqual(items[0].opacity, 10)

        items = utils.createRandomTriangles(e.size, 4)
        self.assertEqual(len(items), 4)
        self.assertTrue(isinstance(items[0], Triangle))
