from tri_image import utils
from tri_image.triangle import Triangle
from test.utils import with_random, BaseTest


#######################################################################
class TestUtils(BaseTest):
    ###################################################################
    def test_string_to_ints(self):
        self.assertEqual([1, 2, 3], utils.string_to_ints("1 2 3"))

    ###################################################################
    @with_random
    def test_create_random_triangles(self):
        e = self.get_evolver()
        items = utils.create_random_triangles(e.size, 2, utils.RGB)
        self.assertEqual(len(items), 2)
        self.assertTrue(isinstance(items[0], Triangle))
        self.assertEqual(items[0].coordinates, [1, 2, 3, 4, 5, 6])
        self.assertEqual(items[0].color, (7, 8, 9))
        self.assertEqual(items[0].opacity, 10)

        items = utils.create_random_triangles(e.size, 4, utils.RGB)
        self.assertEqual(len(items), 4)
        self.assertTrue(isinstance(items[0], Triangle))
