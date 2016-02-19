import os
from io import BytesIO

from PIL import Image

from test.utils import BaseTest
from tri_image.triangle import Triangle
from tri_image.point import Point
from tri_image.sketch import Sketch

data_folder = os.path.join(os.path.dirname(__file__), "data")


#######################################################################
class TestSketch(BaseTest):
    ###################################################################
    def test_constructor(self):
        Sketch(Point(65, 65))
        Sketch(Point(65, 65), [1, 2, 3])

    ###################################################################
    def test_save(self):
        t1 = Triangle([0, 0, 10, 0, 10, 10], (255, 0, 0), 255)
        t2 = Triangle([37, 18, 22, 64, 3, 2], (0, 255, 0), 128)
        s = Sketch(Point(65, 65), [t1, t2])
        s.save_file(self._out("test.txt"))
        saved_file = open(self._out("test.txt")).read().strip()
        expected_file = open(self._data("sketch01.txt")).read().strip()
        self.assertEqual(saved_file, expected_file)

    ###################################################################
    def test_read(self):
        file_contents = open(self._data("sketch01.txt")).read().strip()
        s = Sketch.read(self._data("sketch01.txt"))
        self.assertEqual(s.size.x, 65)
        self.assertEqual(s.size.y, 65)
        self.assertEqual(len(s.triangles), 2)
        content = BytesIO()
        s.save_file_obj(content)
        saved_file = content.getvalue().strip()
        self.assertEqual(saved_file, file_contents)

    ###################################################################
    def test_read_file_obj(self):
        file_contents = open(self._data("sketch01.txt")).read().strip()
        s = Sketch.read_file_obj(BytesIO(file_contents))
        self.assertEqual(s.size.x, 65)
        self.assertEqual(s.size.y, 65)
        self.assertEqual(len(s.triangles), 2)
        content = BytesIO()
        s.save_file_obj(content)
        saved_file = content.getvalue().strip()
        self.assertEqual(saved_file, file_contents)

    ###################################################################
    def test_save_image(self):
        s = Sketch.read(self._data("sketch01.txt"))
        s.save_image(self._out("test.png"))
        im1 = Image.open(self._out("test.png"))
        im2 = Image.open(self._data("test.png"))
        self.assertEqual(list(im1.getdata()), list(im2.getdata()))

        # also works with file-like object
        content = BytesIO()
        s.save_image(content)
        im1 = Image.open(content)
        self.assertEqual(list(im1.getdata()), list(im2.getdata()))

    ###################################################################
    def test_fitness(self):
        s = Sketch.read(self._data("sketch01.txt"))
        im2 = Image.open(self._data("test.png"))
        self.assertAlmostEqual(s.get_fitness(im2), 200)

        s = Sketch(Point(65, 65))
        self.assertEqual(s.get_fitness(im2), 130382)

    ###################################################################
    def test_clone(self):
        s = Sketch.read(self._data("sketch01.txt"))
        s2 = s.clone()
        s.triangles[0].coordinates = [18, 18, 10, 0, 10, 10]
        self.assertEqual(s2.triangles[0].coordinates, [0, 0, 10, 0, 10, 10])
