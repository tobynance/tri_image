import sys, os, datetime, shutil
from PIL import Image, ImageDraw, ImageStat, ImageChops
import aggdraw
from unittest import TestCase

from triangular_image.application import Application

#######################################################################
class TestApplication(TestCase):
    ###################################################################
    def tearDown(self):
        if os.path.exists("../../data/output/test_1"):
            shutil.rmtree("../../data/output/test_1")

    ###################################################################
    def test_run(self):
        a = Application()
        best = a.run(source_image="test.png",
              output_folder="test_1",
              num_triangles=2,
              run_time=datetime.timedelta(seconds=2))

        base = "../../data/output/test_1/"
        self.assertTrue(os.path.exists(base + "final.png"))
        self.assertTrue(os.path.exists(base + "final.txt"))

        self.assertEqual(len(best.triangles), 2)

