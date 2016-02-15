import datetime
import os

from test.utils import BaseTest
from tri_image.application import Application


#######################################################################
class TestApplication(BaseTest):
    ###################################################################
    def test_run(self):
        a = Application()
        best = a.run(source_image=self._data("test.png"),
                     output_folder=self._out("test_1"),
                     num_triangles=2,
                     run_time=datetime.timedelta(seconds=2))

        base = "../../data/output/test_1/"
        self.assertTrue(os.path.exists(base + "final.png"))
        self.assertTrue(os.path.exists(base + "final.txt"))

        self.assertEqual(len(best.triangles), 2)

