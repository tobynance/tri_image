import os
import shutil
import tempfile
from unittest import TestCase

import datetime
from PIL import Image

from tri_image.evolver import Evolver
from tri_image.seeder import Seeder

data_folder = os.path.join(os.path.dirname(__file__), "data")


#######################################################################
class RandomNumber(object):
    def __init__(self):
        self.index = 0

    ###################################################################
    def __call__(self, low, high):
        self.index += 1
        return self.index


#######################################################################
def withRandom(function):
    #raise Exception
    def randomDecorator(*args):
        #raise Exception
        import random
        randint = random.randint
        random.randint = RandomNumber()
        try:
            retVal = function(*args)
        finally:
            random.randint = randint
        #raise Exception
        return retVal
    return randomDecorator


#######################################################################
class BaseTest(TestCase):
    ####################################################################
    def setUp(self):
        self.out_folder = tempfile.mkdtemp(prefix="test_seeder_")

    ####################################################################
    def tearDown(self):
        if self.out_folder:
            shutil.rmtree(self.out_folder, ignore_errors=True)

    ####################################################################
    def _out(self, filename):
        return os.path.join(self.out_folder, filename)

    ####################################################################
    def _data(self, filename):
        return os.path.join(data_folder, filename)

    ###################################################################
    def get_evolver(self):
        return Evolver(source_image=Image.open(self._data("test.png")),
                       output_folder=self._out("test_1"),
                       num_triangles=2,
                       save_frequency=datetime.timedelta(seconds=2))

    ###################################################################
    def get_seeder(self, input_image=os.path.join(data_folder, "test.png"), num_triangles=2):
        if isinstance(input_image, str):
            input_image = Image.open(input_image)
        return Seeder(source_image=input_image,
                      output_folder=os.path.join(self.out_folder, "test_1"),
                      num_triangles=num_triangles)
